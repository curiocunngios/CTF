---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - assembly
  - reverse engineering
tags:
  - flashcard/active/ctf/testing/temp
  - function/index
  - language/in/English
---

#### Basics
Memory operand :: A location in memory that is used as a source or destination for data operations


#### Basic instructions 
`mov` destination, source ::: Used to copy data from one location to another
`mov` destination, source is equivalent to
??
```as
destination = source

Destination: register or memory location    
: register, immediate value, or memory location      
```
<!--SR:!2024-12-09,1,232-->

`lea` destination, source ::: Used to compute the address of a memory operand and store it in a register  
`lea` destination, source is equivalent to
??
```as
destination = source

Destination: A register to store the computed address.    
Source: A memory operand or an address calculation.    
```
<!--SR:!2024-12-10,3,250-->

`call` addr ::: used to call a {{subroutine (function)}} and transfer control to its starting address
`call` is equivalent to
??
```as
push rip  ; Set up address of next instruction of the current frame to the base of next frame {{so that it can jump back}}
```
<!--SR:!2024-12-09,1,232-->

`push` Item::: Pushes Item to the top of the frame <!--SR:!2000-01-01,1,250!2024-12-12,4,270-->
`push` is equivalent to   
??
```as
add rsp, 1    ; Item to be appended in the top slot, allocate space 
mov rsp, Item ; Move Item to the top slot
```
Item can be {{address, value, registers, instruction, etc. basically anything}}

#### Function epilogue
`leave` ::: Preparing to leave a stack frame by cleaning it up and restoring base pointer of previous frame 
`leave` is equivalent to   
??
```as 
mov rbp, rsp  ; {{like closing the stack frame}} 
pop rbp       ; {{normally used for restore previous base pointer}} 
```

`ret` ::: Return to the frame's caller <!--SR:!2024-12-09,1,229!2000-01-01,1,250-->
`ret` is equivalent to  
??
```as
pop rip ; Return address goes to rip. {{rip = an address = jump to that address}}
```



