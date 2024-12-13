---
aliases:
  - libc addresses
  - libc addr
tags:
  - flashcard/active/ctf
---


# Libc Base Address
What is a libc base address. First think of libc like a big book of functions
- When the program {{loads this "book" into memory}}, it needs a starting point
- This {{starting point}} is called the "base address"
- Due to ASLR, this starting point {{changes every time}} you run the program <!--SR:!2024-12-14,1,230!2024-12-14,1,230!2024-12-14,1,230-->

### Example of base address with ASLR
```apache
Run 1: libc might load at 0x7ffff7000000
Run 2: libc might load at 0x7ffff7500000
Run 3: libc might load at 0x7ffff7800000
```

## Libc Function Address:
Each libc function has a {{fixed offset from the base address}} <!--SR:!2024-12-14,1,230-->

Example for system function:
```apache 
If system is at offset 0x45000 from libc base:
Run 1: system will be at 0x7ffff7000000 + 0x45000 = 0x7ffff7045000
Run 2: system will be at 0x7ffff7500000 + 0x45000 = 0x7ffff7545000
Run 3: system will be at 0x7ffff7800000 + 0x45000 = 0x7ffff7845000
```