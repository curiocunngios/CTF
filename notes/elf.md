---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - linux
  - binary
tags:
  - flashcard/active/ctf/testing/temp
  - function/index
  - language/in/English
---

ELF ::: binary format for Linux executables. 

The ELF object helps [parse](./parsing.md) the binary,
giving access to sections (.text, .bss, etc), symbols, and other binary information
elf = ELF("program")
```py
elf = ELF("program")
print(elf.symbols)        # Get all function names and addresses
print(elf.got)           # Get GOT table entries
print(elf.plt)           # Get PLT table entries
print(elf.sections)      # Get sections like .text, .bss
```
