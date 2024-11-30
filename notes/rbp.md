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

rbp is the {{base point}}::: Points to the base of the stack frame

memory layout:
```
High addresses
          │
          ▼
    ┌──────────────┐
    │ Return addr  │
    ├──────────────┤
RBP→│ Saved RBP    │ 
    ├──────────────┤
    │ Local vars   │
    │ (buffer[64]) │
RSP→└──────────────┘
          ▲
          │
Low addresses
```