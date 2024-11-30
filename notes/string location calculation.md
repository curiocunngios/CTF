---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - calculation
  - memory 
  - offset
  - memory layout
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

```c
printf("Enter input:");
```

So the string, which is stored in {{rodata}} here should be loaded as the first parameter into the `printf` function from `libc`

1. load the memory address into `rax` with lea
2. But what's the address?
3. rip + <offset>
4. <offset> Calculated as follow:
5. all done by compilation during the compilation process 
6. then hardcoded into the instructions 

```
Memory layout after compilation:
0x40113e: lea rax, [rip (0x401145) + <offset> (0xebf..hardcoded)]
0x401145: mov instruction (next instruction after lea)
...
0x402004: "Enter input:" string

Offset calculation:
0x402004 (string location) - 0x40113e (next instruction) = 0xebf

```


```
0x40113e <vulnerable_function+8>     lea    rax, [rip + 0xebf]     
0x401145 <vulnerable_function+15>    mov    rdi, rax     
```