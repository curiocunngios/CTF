aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - pwndbg
  - assembly 
  - registers
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

# push, pop, call, and ret
- `%rsp` points to {{top of the stack}}. `%rbp` points to {{bottom of the current stack/function frame}}. The stack grows in {{negative direction (by decreasing rsp).}}
- `push` and `pop` are used for {{adding and removing data on the stack.}}
- `push` **reg_or_const** is similar to :::
```as
sub rsp, 8
mov [rsp], reg_or_const
```
**reg_or_const**
- `pop` **reg** is similar to :::
```as
mov reg, [rsp]
add rsp, 8
```

- The stack size can also change by 2 if explicitly specified (push (???)
word, pop word), but not 4 or 1
- call address is sort of like push next(rip), then jmp labe