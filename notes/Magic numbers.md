---
aliases:
  - Magic number 
  - ELF magic number
tags:
  - flashcard/active/ctf
---

# Magic numbers in linux
the {{first few bytes of a file}} that identify its type is called the magic number in linux
For example:
```
PNG: 89 50 4E 47 0D 0A 1A 0A
PDF: 25 50 44 46
ELF: 7F 45 4C 46
```
<!--SR:!2024-12-15,1,230-->

### Motivation
WE can identify file types {{by the number without extension}} <!--SR:!2024-12-18,4,270-->