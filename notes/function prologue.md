---
aliases:
  - Function's start 
  - Stack frame's start
  - Beginning of frame
tags:
  - flashcard/active/ctf
---


# Function Prologue assembly instruction
??
```
0x40118b: push   rbp        # Save old base pointer on stack
0x40118c: mov    rbp,rsp    # Set up new base pointer for this frame
```
<!--SR:!2024-12-15,1,230-->

## The stack operation
How does stack looks like from before prologue to after prologue
??
```
Before prologue:
        [old rbp]
        [......]                       <--- (other data e.g. cosmetic point arguments)
        [old return addr]  <--- RSP (call <addr> pushes next instruction here)
        [......]

After push rbp:
        [old return addr]
        [old rbp]                 <--- RSP
        [......]

After mov rbp,rsp:
        [old return addr]
        [old rbp]                <--- RBP, RSP
        [......]
```
<!--SR:!2024-12-18,4,274-->

- RBP value is saved below the return address to be {{restored later during `leave` instruction}} <!--SR:!2024-12-18,4,270--> 

### Assembly instructions in details

`push` Item :: Pushes Item to the top of the frame <!--SR:!2024-12-18,4,270-->
`push` is equivalent to
??
```as
sub rsp, 1    ; Item to be appended in the top slot, allocate space 
mov rsp, Item ; Move Item to the top slot
Item can be address, value, registers, instruction, etc. (Basically anything).
```
<!--SR:!2024-12-18,4,270-->

