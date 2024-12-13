---
aliases:
  - libc function calls 
  - libc call
tags:
  - flashcard/active/ctf
---

# Libc function calls
To call a libc function. We first call {{PLT}} then we either {{resolves function's libc address with dynamic linker}} or {{get the real address from GOT}}
Example
## Normal flow when calling puts("hello"):
- Code calls {{puts@plt}}
- First time:
puts@plt -> {{dynamic linker}} -> resolves {{real puts address}} -> stores in {{puts@got}}
- Future calls:
{{puts@plt -> checks puts@got}} -> jumps to 0x7ffff7a649c0 (real puts in libc) <!--SR:!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250-->


  
