---
aliases:
  - Saved registers
tags:
  - flashcard/active/ctf
---

# Saved registers

When a function starts, it may need to {{use registers that the calling function is using}} <!--SR:!2024-12-17,3,250-->

- These registers' values must be preserved for {{future return to the calling function}}
- They're saved on stack at {{function start (prologue)}}
- Restored before {{function returns (epilogue)}}
```nasm
; Prologue example
push ebp      ; Save old base pointer
mov ebp, esp  ; Create new stack frame
push ebx      ; Save ebx if we'll use it
```
<!--SR:!2024-12-17,3,248!2024-12-17,3,245!2024-12-17,3,243-->

  