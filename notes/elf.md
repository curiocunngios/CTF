---
aliases:
  - linux executable in binary 
  - linux exe in binary 
tags:
  - flashcard/active/ctf/hi
---

ELF ::: binary format for Linux executables. <!--SR:!2024-12-15,4,270!2024-12-15,4,270-->

The ELF object `elf = ELF("program")` in pwntools helps {{[parse](./parsing.md)}}the binary,
giving access to {{sections (.text, .bss, etc), symbols}}, and other binary information
```py
elf = ELF("program")
print(elf.symbols)        # Get all function names and addresses
print(elf.got)           # Get GOT table entries
print(elf.plt)           # Get PLT table entries
print(elf.sections)      # Get sections like .text, .bss
```
<!--SR:!2024-12-15,4,270!2024-12-12,1,230-->
