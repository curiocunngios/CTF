---
aliases:
- stack space allocation
tags:
- flashcard/active/ctf
---

# Stack allocation 

Allocation of spaces for local variables can be done with {{one assembly instruction}}
```c
   char canary[CANARY_SIZE]; // canary, 4
   char buf[BUFSIZE]; // our input, 64 
   char length[BUFSIZE]; // input length, 64
   int count; // 4
   int x = 0; // 4
   memcpy(canary,global_canary,CANARY_SIZE); // canary = global_canary 
```
```as
sub    esp,0x94        ; Allocate stack space (148 bytes) for local variables
```
The extra spaces added are for some {{[alignment padding](./Stack%20alignment.md)}} and space for {{saved registers.}} <!--SR:!2024-12-17,3,248!2024-12-17,3,250!2024-12-17,3,248-->