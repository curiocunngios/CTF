---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - dynamic linking
  - PLT
  - GOT
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---
PLT (procedure linkage table) and GOT (Global offsets table) used for dynamically linking libraries 

::: are inject in the linking process of of the compilation process

::: they are added to the executable file (seemed to be a section in the .s file and if we go back to the .s file)
Source code → Assembly → Object file → Executable
(example.c) → (example.s) → (example.o) → (example)

PLT/GOT sections are added during linking stage:
source.c → preprocessor → compiler → assembler → linker
                                                  ↑
                                          Adds PLT/GOT here


#flashcard what GOT stores
Before first call:
GOT[printf] ::: address of "resolver" code

After first call:
GOT[printf] ::: actual printf address in libc (0x7ff123456789) which is {{calculated with offset of printf + base address of libc which could be randomized by ALRS}}



1. In libc file:
   Start of libc (0) ----[offset: 0x522d0]----> printf function

2. In memory address calculation:
   Base address ---[offset]---> target location
