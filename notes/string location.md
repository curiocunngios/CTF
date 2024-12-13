---
aliases:
  - string location calculation 
tags:
  - flashcard/active/ctf
---

```c
printf("Enter input:");
```
The string `"Enter input"` is stored in {{.rodata}}. It should be loaded as the first parameter into the `printf` function from `libc`
- load the memory address `rip + <offset>` into `rax` with lea
- <offset> calculated {{during the compilation process}} and then {{hardcoded into the instructions}}
```
Memory layout after compilation:
0x40113e: lea rax, [rip (0x401145) + <hardcoded-offset>]
0x401145: mov rdi, rax 
...
0x402004: "Enter input:" string

Offset calculation:
0x402004 (string location) - 0x401145 (next instruction) = 0xebf
```
<!--SR:!2024-12-18,4,270!2024-12-15,1,230!2024-12-18,4,270-->


