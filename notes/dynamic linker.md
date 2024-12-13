---
aliases:
  - dynamic linker
tags:
  - flashcard/active/ctf
  - notes/tbc
---

## Dynamic linker
- When program starts, binary has external functions like puts() but doesn't know their real addresses.  
- Dynamic linker (ld.so) is {{responsible for "linking" these at runtime}}. It first checks the address of a function in {{libc}} and proceed to {{write it to GOT}} so that dynamic linker does not have to be used multiple times <!--SR:!2024-12-18,4,270!2024-12-18,4,270!2024-12-18,4,270--> 


