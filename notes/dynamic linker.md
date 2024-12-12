---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
tags:
  - flashcard/active/ctf/hi
  - function/index
  - language/in/English
---

## Dynamic linker
When program starts, binary has external functions like puts() but doesn't know their real addresses Dynamic linker (ld.so) is {{responsible for "linking" these at runtime}}. It first checks the address of a function in {{libc}} and proceed to {{write it to GOT}} so that dynamic linker does not have to be used multiple times <!--SR:!2024-12-12,1,230!2024-12-12,1,230!2024-12-15,4,270-->


