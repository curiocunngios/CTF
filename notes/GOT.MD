---
aliases:
  - Global offset table
tags:
  - flashcard/active/ctf
---


GOT stands for **Global Offset Table** ==stores the real addresses of functions== i.e. the function addresses in the {{libc library.}}
When puts is called first time and after {{dynamic linker resolves the real addresses}}, that address would then be stored in GOT <!--SR:!2024-12-14,1,230!2024-12-14,1,230!2024-12-14,1,230!2024-12-14,1,230-->
