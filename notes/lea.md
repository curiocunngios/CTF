---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - lea
  - assembly
  - memory
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

lea ::: lea stands for load effective address. lea {{loads effective address of source into destination}} <!--SR:!2000-01-01,1,250!2024-12-02,1,230-->


lea addr, dst ::: dst = addr {{AT &T}} <!--SR:!2024-12-02,1,230!2024-12-02,1,230-->
lea dst, addr ::: dst = addr {{Intel}}
```as
lea    0xe3(%rip),%rdi # 
```