---
aliases:
  - gadgets
  - instruction sequences
tags:
  - flashcard/active/ctf
---

# Gadgets 
Gadgets is a machine instruction **sequences** that are already present in the machine's memory, it's not finding a single instruction that does both operations. <!--SR:!2024-12-14,1,230-->
Each gadget typically ends in **a return instruction (ret)** and is located in a subroutine (function) within the existing program and/or shared library code.
Example:
```as
pop rdi    ; take value from stack → put in rdi
ret        ; take next value from stack → jump there
```
<!--SR:!2024-12-14,1,230-->

## gadgets location
??
Using terminal
```bash
# Using ROPgadget tool
ROPgadget --all --binary program | grep "pop rdi"
# This searches the program's code for useful instruction sequences
```
Using pwntools
```py
elf = ELF("program")
rop = ROP(elf)
print(rop.rdi)    # Finds pop rdi; ret
print(rop.rsi)    # Finds pop rsi; ret
print(rop.dumps()) # Shows all found gadgets
```
<!--SR:!2024-12-14,1,230-->

The output of ROPgadget is the {{starting address of the sequences of instructions}}
For example, output would be {{0x400868}}
```as
0x400868: leave          ; First instruction
0x400869: ret           ; Second instruction
```


When ROPgadget reports this as 0x400868: leave; ret, it means:

- If you jump to 0x400868, you'll execute {{both instructions in sequence}}
- It's reporting the starting address (0x400868) of the useful sequence <!--SR:!2024-12-14,1,230-->


