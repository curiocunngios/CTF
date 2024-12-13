---
aliases:
  - pipe Operator
  - `|` opeartor
tags:
  - flashcard/active/ctf
---

# PLT
PLT stands for {{Procedure Linkage Table}} is like a {{"jump table"}}
- When your program calls puts(), it first goes through this table. {{puts@plt}}
- It is like the {{"entrance" to the puts function}}
- Then it directs the program to {{GOT}} or {{dynamic linker to resolves function addresses libc}}
