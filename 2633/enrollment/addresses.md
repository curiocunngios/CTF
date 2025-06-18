# stack addresses
Inside stack addresses (0x7fff... range), you typically find:

1. Local variables
```c
int x = 5;         // Value stored directly
char buf[20];      // Buffer/array
char *ptr;         // Pointers
```

2. Function parameters
```c
void func(int a, char *b)  // Parameters stored on stack
```

3. Return addresses 
- Stored when a function is called
- Used to return to caller

4. Saved registers
- Saved rbp (base pointer)
- Other callee-saved registers

5. Stack canaries
- When stack protection is enabled

6. Function pointers
```c
void (*fp)();  // Function pointer variable
```

7. Pointers to other memory regions:
- Heap addresses (0x5... range)
- Global variables
- .data section addresses
- .text section addresses

Example stack frame layout:
```
High addresses
[   local vars   ]
[    canary     ]
[  saved rbp    ]
[ return addr   ]
[  parameters   ]
Low addresses
```


# .text addresses
```
```
0000000000001532 <main>:
    1532:	f3 0f 1e fa          	endbr64
    1536:	55                   	push   rbp
```

how can these addresses be called? instruction address ? .text section address? .data address? stack addresses?
```
These are `.text` section addresses, also commonly called:
- Instruction addresses
- Program addresses
- Virtual addresses (when ASLR is enabled)
- Code addresses

They are NOT:
- Stack addresses (which typically start with 0x7fff...)
- Heap addresses (which typically start with 0x5... or 0x6...)
- .data section addresses (which would be in a different section but still within the program's memory space)

In this case, 0x1532 is the offset within the .text section where the `main` function begins. When the program is loaded:
1. With ASLR off: These addresses get a fixed base address added (like 0x400000)
2. With ASLR on: These addresses get a randomized base address added

So the actual runtime address might be something like:
- 0x400000 + 0x1532 = 0x401532 (no ASLR)
- 0x555555554000 + 0x1532 = 0x555555555532 (with ASLR)