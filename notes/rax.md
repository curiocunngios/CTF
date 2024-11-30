---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - assembly
  - memory
  - stack
  - pointers
  - stack frame
  - registers
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

sometimes EAX = 0 before printf 

- clears out the lower 32 bits (least significant) for RAX 
  
```
RAX (64-bit):
[               RAX (64 bits)               ]
[       EAX (32 bits)      ][  unused      ]
[   AX (16)   ][         ][  unused      ]
[ AH (8) ][ AL (8) ][         ][  unused      ]


Before:
RAX: [XXXX XXXX XXXX XXXX] (64 bits, X = unknown value)
     [XXXX XXXX][XXXX XXXX]
     
After mov eax, 0:
RAX: [0000 0000 XXXX XXXX]
     [0000 0000][XXXX XXXX]
                ↑
                Lower 32 bits zeroed
```
- required by the calling convention of x64 before variadic functions which are {{functions with variable arguments like printf}}
- 0 refers to the number of vector registers which is for {{floating point}} arguments

