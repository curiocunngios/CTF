---
aliases:
  - assembly instructions
  - assembly
  - x84-64
tags:
  - flashcard/active/ctf
  - notes/tbc
---

#### Basics
Memory operand :: A location in memory that is used as a source or destination for data operations <!--SR:!2024-12-13,1,228-->


#### Basic instructions 
`mov` dest, src :: Copy data from `src` to `dest` location to another <!--SR:!2024-12-13,1,228-->
`mov` dest, src is equivalent to
??
```as
dest = src

dest: register or memory location    
src : register, immediate value, or memory location      
```
<!--SR:!2024-12-13,1,228-->


`lea` dest, src :: Compute the address of a memory operand and store it in a register <!--SR:!2024-12-13,1,228-->
`lea` dest, src is equivalent to
??
```as
dest = src

dest: A register to store the computed address.    
src: A memory operand or an address calculation.    
```
<!--SR:!2024-12-13,1,228-->


`call` addr :: call a subroutine (function) and transfer control to its starting address <!--SR:!2024-12-13,1,230-->
`call` is equivalent to
??
```as
push rip  ; Set up address of next instruction of the current frame to the base of next frame {{so that it can jump back}}
```
<!--SR:!2024-12-13,1,228-->







