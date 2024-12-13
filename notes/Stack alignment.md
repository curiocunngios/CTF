---
aliases:
  - alignment padding 
  - stack padding 
  - memory padding
tags:
  - flashcard/active/ctf
---

# Stack alignment

Memory addresses should be {{multiples of certain values}} (usually 16 bytes on x86_64) for performance
```
Example: If you need 10 bytes, it might allocate 16 to keep aligned
0x1000: [used][used][used]....[pad][pad] (16 bytes total)
```
<!--SR:!2024-12-17,3,250-->