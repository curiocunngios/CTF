# discoveries
Here shows all the discoveries I have had from exploring the problem. In other words, the things I have learnt from this CTF challenge.
## 1. from ghidra's decompiled code:
```
write(1,&DAT_00102107,2);
```

```
                             DAT_00102107                                    XREF[1]:  FUN_00101791:0010184c(*)  
  00102107 24                        ??         24h    $
  00102108 20                        ??         20h     
  00102109 00                        ??         00h
```
This appears to be a write() syscall that prints a character sequence to stdout (file descriptor 1). Looking at the hex data at DAT_00102107, it's printing:

- 0x24 (ASCII '$') ( this goes into flashcard xD)
- 0x20 (ASCII space) (this goes into flashcard xD)

The length parameter is 2, so it will print exactly 2 bytes: "$ "

This is commonly seen in CTF challenges or shell programs where it's printing a prompt/shell indicator like "$ " before waiting for user input.

In decompiled code, when you see DAT_ prefixes in Ghidra, these usually refer to raw data segments in the binary, and in this case it's pointing to a string/character sequence that's embedded in the program.


For this case where it's printing a string prompt, the most suitable way to retype it in Ghidra would be as a `char[]`.

To retype in Ghidra:
1. Go to the DAT_00102107 location
2. Press 't' (for retype)
3. Enter `char[3]` or `char[2]` (depending if you want to include the null terminator)

After retyping, Ghidra showed something more readable:
```c
write(1, "$ ", 2);
```
`char[3]` is suggested because it includes the null byte (0x00) that appears after the string, which is typical for C-style strings, even though the write() is only using 2 bytes. This makes the data's purpose clearer in the decompilation.

Note that write() doesn't require null-terminated strings since it uses an explicit length parameter, but retyping as a char array makes the code's intent more obvious when analyzing.

## __isoc99_scanf
```c
iVar1 = __isoc99_scanf("%1d",&local_c);
```
This is commonly seen in menu-drive programs where user would have to chose from 0-9.   
This scanf call reads a single decimal digit from user input.   
Breaking it down:
- `%1d` - This format specifier means:
  - `%d` reads an integer
  - `1` limits the input to exactly 1 character/digit (0-9)
- `&local_c` - The input is stored in the variable local_c
- The return value `iVar1` will be:
  - 1 if successful read
  - 0 or negative if read failed

So this is basically reading a single digit number from the user. For example:
- If user enters "5", local_c will be 5
- If user enters "42", only "4" will be read
- If user enters "a", the scan will fail since it's not a digit

The `__isoc99_` prefix is just the internal name for the C99 standard version of scanf - functionally it's the same as regular `scanf`.

```c
if (0x13 < local_1c) {
LAB_001013cc:
      if (local_20 == 999) {
        puts("can not add now");
      }
```
`LAB_001013cc` shown in ghidra's decompiler just indicates the code block of 
```c
if (local_20 == 999) {
  puts("can not add now");
}
```
By the way, here is the assembly of it
```as
                             LAB_001013cc                                    XREF[1]:  001013c0(j)  
  001013cc 81 7d e8 e7 03 00 00      CMP        dword ptr [RBP + local_20],0x3e7
  001013d3 75 11                     JNZ        LAB_001013e6
  001013d5 48 8d 3d 2c 0c 00 00      LEA        RDI,[s_can_not_add_now_00102008]                 = "can not add now"
  001013dc e8 0f fd ff ff            CALL       <EXTERNAL>::puts                                 int puts(char * __s)
  001013e1 e9 38 01 00 00            JMP        LAB_0010151e
```
1. `CMP dword ptr [RBP + local_20],0x3e7`
   - Compares the value at `[RBP + local_20]` with `0x3e7` (999 in decimal)
2. `JNZ LAB_001013e6`
   - Jump if Not Zero (if the comparison wasn't equal)
   - If the value is not 999, it jumps to `LAB_001013e6`
3. If the value IS 999 (doesn't jump), it:
   - Loads the address of string "can not add now" into RDI
   - Calls puts() to print the error message
   - Jumps to LAB_0010151e (proceeds to the code below)
# calloc
```c
local_18 = calloc(0x20,1)
```
This calloc() call allocates memory with these specifications:

- First argument (0x20) = 32 in decimal: number of elements
- Second argument (1): size of each element in bytes
- Total allocation size = 32 * 1 = 32 bytes
- The allocated memory is initialized to zero (all bytes set to 0)

The key difference between calloc() and malloc() is that:
- calloc() initializes all bytes to zero
- malloc() leaves the memory uninitialized with whatever garbage values were there

So `local_18 = calloc(0x20,1)` is equivalent to:
```c
local_18 = malloc(32);
memset(local_18, 0, 32);
```

In heap exploitation context, this means:
- You get a 32-byte chunk
- The chunk will be zeroed out
- The pointer to this chunk is stored in local_18
- If allocation fails, local_18 will be NULL

# Stripped binary 
```
0000000000001180 <.text>:
    1180:	f3 0f 1e fa          	endbr64
    1184:	31 ed                	xor    ebp,ebp
    1186:	49 89 d1             	mov    r9,rdx
    1189:	5e                   	pop    rsi
    118a:	48 89 e2             	mov    rdx,rsp
    118d:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
    1191:	50                   	push   rax
    1192:	54                   	push   rsp
    1193:	4c 8d 05 d6 07 00 00 	lea    r8,[rip+0x7d6]        # 1970 <exit@plt+0x800>
    119a:	48 8d 0d 5f 07 00 00 	lea    rcx,[rip+0x75f]        # 1900 <exit@plt+0x790>
    11a1:	48 8d 3d e9 05 00 00 	lea    rdi,[rip+0x5e9]        # 1791 <exit@plt+0x621>
    11a8:	ff 15 32 2e 00 00    	call   QWORD PTR [rip+0x2e32]        # 3fe0 <exit@plt+0x2e70>
    11ae:	f4                   	hlt
    11af:	90                   	nop
    11b0:	48 8d 3d 59 2e 00 00 	lea    rdi,[rip+0x2e59]        # 4010 <exit@plt+0x2ea0>
    11b7:	48 8d 05 52 2e 00 00 	lea    rax,[rip+0x2e52]        # 4010 <exit@plt+0x2ea0>
    11be:	48 39 f8             	cmp    rax,rdi
    11c1:	74 15                	je     11d8 <exit@plt+0x68>
    ...
    ...
    ...
```

```
─────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]─────────────────────────────────────────
   0x7ffff7fdc27a    je     0x7ffff7fdc4d5              <0x7ffff7fdc4d5>
 
   0x7ffff7fdc280    mov    rdx, qword ptr [rsp + 0x18]     RDX, [0x7fffffffd8c8] => 0x100
   0x7ffff7fdc285    mov    r11, qword ptr [rsp + 0x20]     R11, [0x7fffffffd8d0] => 1
   0x7ffff7fdc28a    mov    qword ptr [rax + 0x28], rax     [0x7ffff7ffe1b8] <= 0x7ffff7ffe190 ◂— 0
   0x7ffff7fdc28e    mov    rsi, rbp                        RSI => 0x7ffff7ff4342 ◂— 0x706e203d3d206900
 ► 0x7ffff7fdc291    lea    r9, [rax + rdx + 0x480]         R9 => 0x7ffff7ffe710 ◂— 0
   0x7ffff7fdc299    mov    rdx, r11                        RDX => 1
   0x7ffff7fdc29c    mov    qword ptr [rax + 0x2d0], r9     [0x7ffff7ffe460] <= 0x7ffff7ffe710 ◂— 0
   0x7ffff7fdc2a3    lea    rdi, [r9 + 0x20]                RDI => 0x7ffff7ffe730 ◂— 0
   0x7ffff7fdc2a7    lea    rax, [r9 + 8]                   RAX => 0x7ffff7ffe718 ◂— 0
   0x7ffff7fdc2ab    mov    qword ptr [rsp + 0x18], r9      [0x7fffffffd8c8] <= 0x7ffff7ffe710 ◂— 0
──────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffd8b0 ◂— 0
01:0008│     0x7fffffffd8b8 —▸ 0x7ffff7ff4342 ◂— 0x706e203d3d206900
02:0010│     0x7fffffffd8c0 ◂— 0x20000000
03:0018│     0x7fffffffd8c8 ◂— 0x100
04:0020│     0x7fffffffd8d0 ◂— 1
05:0028│     0x7fffffffd8d8 ◂— 0x2000000000000000
06:0030│     0x7fffffffd8e0 ◂— 0
07:0038│     0x7fffffffd8e8 —▸ 0x7ffff7ff3018 ◂— 0xfffdec49fffdec81
────────────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────────────
 ► 0   0x7ffff7fdc291 None
   1   0x7ffff7fd1d2f None
   2   0x7ffff7febc3b None
   3   0x7ffff7fd104c None
   4   0x7ffff7fd0108 None
   5              0x1 None
   6   0x7fffffffdfe1 None
   7              0x0 None
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> heap
Can't find GLIBC version required for this command to work, maybe is because GLIBC is not loaded yet.
If you believe the GLIBC is loaded or this is a statically linked binary. Please set the GLIBC version you think the target binary was compiled (using `set glibc <version>` command; e.g. 2.32) and re-run this command
```

```

void FUN_00101381(void)

{
  char local_21;
  int local_20;
  int local_1c;
  void *local_18;
  void *local_10;
  
  local_20 = 999;
  local_1c = 0;
  do {
    if (0x13 < local_1c) {
LAB_001013cc:
      if (local_20 == 999) {
        puts("can not add now");
      }
      else {
        local_18 = calloc(0x20,1);
        *(void **)(&DAT_00104040 + (long)local_20 * 8) = local_18;
        **(undefined4 **)(&DAT_00104040 + (long)local_20 * 8) = 0;
        *(int *)(*(long *)(&DAT_00104040 + (long)local_20 * 8) + 4) = DAT_0010403c;
        DAT_0010403c = DAT_0010403c + 1;
        puts("Enter the message size for the user : ");
        __isoc99_scanf(&DAT_0010203f,&local_21);
        if (local_21 < '\x01') {
          puts("Bye hacker");
                    /* WARNING: Subroutine does not return */
          exit(0);
        }
        *(char *)(*(long *)(&DAT_00104040 + (long)local_20 * 8) + 8) = local_21;
        local_10 = calloc((long)local_21,1);
        puts("Input message content >>");
        FUN_001012ae(local_10,(int)local_21);
        *(void **)(*(long *)(&DAT_00104040 + (long)local_20 * 8) + 0x18) = local_10;
      }
      return;
    }
    if (*(long *)(&DAT_00104040 + (long)local_1c * 8) == 0) {
      local_20 = local_1c;
      goto LAB_001013cc;
    }
    local_1c = local_1c + 1;
  } while( true );
}
```
When a binary is stripped, it means that symbols (including function names) are removed to reduce size and make reverse engineering more difficult.

In this case:
- objdump and pwndbg look at the actual binary symbols, which are stripped
- Ghidra performs analysis and reconstructs functions based on the code patterns, then assigns synthetic names like `FUN_00101381`

The functions are still there in the code, but their names and symbols are removed. Ghidra helps by:
- Identifying function boundaries
- Creating meaningful decompiled C code
- Assigning placeholder names (FUN_*)
- Reconstructing the control flow

This is why when debugging with pwndbg, raw addresses instead of function names are shown.

# pwndbg with stripped binaries
To effectively use pwndbg with a stripped binary:

1. Use breakpoints with addresses rather than function names:
```bash
b *0x1381    # Break at function start
b *0x13cc    # Break at specific location
```

2. Map Ghidra's analysis to pwndbg:
- Use Ghidra to identify important addresses
- Set breakpoints at those addresses in pwndbg
- Keep a reference of Ghidra's FUN_* names and their corresponding addresses


# 
```
        *(void **)(&DAT_00104040 + (long)local_20 * 8) = local_18;
        **(undefined4 **)(&DAT_00104040 + (long)local_20 * 8) = 0;
        *(int *)(*(long *)(&DAT_00104040 + (long)local_20 * 8) + 4) = DAT_0010403c;
        DAT_0010403c = DAT_0010403c + 1;
```
Let me break this down:

1. `(&DAT_00104040 + (long)local_20 * 8)` 
   - `DAT_00104040` appears to be a base memory address
   - This is calculating an offset from that base address by multiplying `local_20` by 8 (likely because pointers are 8 bytes on 64-bit systems)

2. `(void **)(&DAT_00104040 + (long)local_20 * 8) = local_18;`
   - This is storing the pointer `local_18` (which was allocated by calloc) into an array of pointers
   - Think of it as: `array[local_20] = local_18;`

3. `**(undefined4 **)(&DAT_00104040 + (long)local_20 * 8) = 0;`
   - This is dereferencing the pointer we just stored and setting its first 4 bytes to 0
   - Think of it as: `array[local_20]->first_4_bytes = 0;`

4. `*(int *)(*(long *)(&DAT_00104040 + (long)local_20 * 8) + 4) = DAT_0010403c;`
   - This is setting the next 4 bytes (offset of 4) of the allocated memory to the value of `DAT_0010403c`
   - Think of it as: `array[local_20]->second_4_bytes = DAT_0010403c;`

In simpler terms, this code is:
1. Allocating a 32-byte (0x20) chunk of memory
2. Storing the pointer to this memory in an array
3. Setting the first 4 bytes of the allocated memory to 0
4. Setting the next 4 bytes to some value (`DAT_0010403c`)

This looks like part of a heap-based CTF challenge, possibly dealing with heap memory management or exploitation.


I clicked on them and they shows nothing
```
                             DAT_00104040                                    XREF[27]: FUN_00101381:001013aa(*), 
                                                                                       FUN_00101381:001013b1(*), 
                                                                                       FUN_00101381:00101406(*), 
                                                                                       FUN_00101381:00101422(*), 
                                                                                       FUN_00101381:00101440(*), 
                                                                                       FUN_00101381:001014b2(*), 
                                                                                       FUN_00101381:0010150b(*), 
                                                                                       FUN_00101520:0010157d(*), 
                                                                                       FUN_00101520:00101584(*), 
                                                                                       FUN_00101520:001015b0(*), 
                                                                                       FUN_00101520:001015b7(*), 
                                                                                       FUN_00101520:001015e2(*), 
                                                                                       FUN_00101520:001015e9(*), 
                                                                                       FUN_00101621:00101670(*), 
                                                                                       FUN_00101621:00101677(*), 
                                                                                       FUN_00101621:001016a3(*), 
                                                                                       FUN_00101621:001016aa(*), 
                                                                                       FUN_00101621:001016c7(*), 
                                                                                       FUN_00101621:001016ce(*), 
                                                                                       FUN_00101621:001016e7(*), [more]
  00104040 00                        ??         00h
  00104041 00                        ??         00h
  00104042 00                        ??         00h
  00104043 00                        ??         00h
  00104044 00                        ??         00h
  00104045 00                        ??         00h
  00104046 00                        ??         00h
  00104047 00                        ??         00h
  00104048 00                        ??         00h
  00104049 00                        ??         00h
  0010404a 00                        ??         00h
  0010404b 00                        ??         00h
  0010404c 00                        ??         00h
  0010404d 00                        ??         00h
  0010404e 00                        ??         00h
  0010404f 00                        ??         00h
  00104050 00                        ??         00h
  00104051 00                        ??         00h
  00104052 00                        ??         00h
  00104053 00                        ??         00h
  00104054 00                        ??         00h
  00104055 00                        ??         00h
```

These look like a global array of pointers used to manage heap chunks. 

1. `DAT_00104040` appears to be a global array of pointers, where:
- Each entry is 8 bytes (pointer size on 64-bit)
- Used to store pointers to allocated chunks
- Size seems to be 0x13 (19) entries based on the earlier checks

1. The operations:
```c
*(void **)(&DAT_00104040 + (long)local_20 * 8) = local_18;
```
This stores the pointer `local_18` (returned from calloc) into the array at index `local_20`

```c
**(undefined4 **)(&DAT_00104040 + (long)local_20 * 8) = 0;
```
This sets the first 4 bytes of the allocated chunk to 0

```c
*(int *)(*(long *)(&DAT_00104040 + (long)local_20 * 8) + 4) = DAT_0010403c;
```
This sets the next 4 bytes to the value of DAT_0010403c (likely an ID or counter)

The structure probably looks like this:
```c
struct chunk {
    int field1;     // Set to 0
    int field2;     // Set to DAT_0010403c
    char size;      // Message size at offset 8
    char pad[3];    // Padding
    void *content;  // Message content pointer at offset 0x18
};

struct chunk *chunks[20];  // DAT_00104040 array
```

This is a common pattern in heap challenges where the program maintains an array of pointers to dynamically allocated structures.


## In details

1. For `**(undefined4 **)` - it's dereferencing twice:
- First * gets the pointer stored in the array
- Second * dereferences that pointer as a 4-byte (undefined4) value
- Setting it to 0 affects the first 4 bytes of where that pointer points

### To create this structure in Ghidra:

a. Go to the Data Type Manager (Window > Data Type Manager)
b. Create a new structure:
```
- Right click on the program name
- New > Structure
- Name it (e.g., "chunk")
```

c. Add fields:
```
- Click "Add" for each field
- Set appropriate types and sizes:
  * field1: int
  * field2: int
  * size: char
  * pad: char[3]
  * content: pointer
```

d. Apply the structure:
```
- Go to where the pointer is used
- Right-click on the variable
- Select "Data Type" 
- Choose your created structure
```

Example in Ghidra's Data Type Manager:
```c
struct chunk {
    int field1;     /* offset: 0x0 */
    int field2;     /* offset: 0x4 */
    char size;      /* offset: 0x8 */
    char pad[3];    /* offset: 0x9 */
    void *content;  /* offset: 0x18 */
} /* size: 0x20 */
```

After creating and applying the structure, Ghidra's decompilation should become clearer, showing struct member accesses instead of raw pointer arithmetic.

You can verify the offsets in pwndbg:
```bash
pwndbg> x/24x allocated_chunk_address
```


# The task involves a bit too much reverse engineering so I am going to leave this alone for a while
