---
aliases:
  - Memory
tags:
  - flashcard/active/ctf/yo
  - notes/tbc
---
# Memory
Memory is divided into two main spaces:
- **[Kernel space ](<kernal space.md>)**
- **[User Space](<User Space.md>)**
Visual representation (64-bit):
```
0xFFFFFFFFFFFFFFFF   ────────────
                    │Kernel Space│
0xffff800000000000  ├────────────┤
                    │            │
                    │            │
0x00007FFFFFFFFFFF  │ User Space │
                    │            │
0x0000000000000000  └────────────┘
```
## Memory layout (typical 64-bit linux)
```
0x000000000000 - 0x00007fffffff: Lower half (kernel space)
0x800000000000 - 0x7fffffffffff: Upper half (user space)
                        ↑
                        Your address is here
```
<!--SR:!2024-12-17,3,250!2024-12-17,3,250-->