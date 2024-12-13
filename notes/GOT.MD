---
aliases:
  - Global offset table
tags:
  - flashcard/active/ctf
---

# GOT
GOT stands for **Global Offset Table** ==stores the real addresses of functions== i.e. the function addresses in the {{libc library.}}
When puts is called first time and after {{dynamic linker resolves the real addresses}}, that address would then be stored in GOT <!--SR:!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250-->

## Storage
- Before first call:
GOT[printf] stores {{address of "resolver" code}}
- After first call:
GOT[printf] stores {{actual printf address in libc (0x7ff123456789)}} which is {{calculated with offset of printf + base address of libc which could be randomized by ALRS}} <!--SR:!2024-12-15,1,223!2024-12-17,3,263!2024-12-17,3,263-->