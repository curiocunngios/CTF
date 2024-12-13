---
aliases:
  - object linking
tags:
  - flashcard/active/ctf
---
# object linking
```
Source code → Assembly → Object file → Executable
(example.c) → (example.s) → (example.o) → (example)
```
## PLT and GOT
PLT and GOT used for dynamically linking libraries {{are inject in the linking process of of the compilation process}}
```
PLT/GOT sections are added during linking stage:
source.c → preprocessor → compiler → assembler → linker
                                                  ↑
                                          Adds PLT/GOT here
```
<!--SR:!2024-12-18,4,270-->
