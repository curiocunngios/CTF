---
aliases:
  - shellcode
tags:
  - flashcard/active/ctf
---

```py
next(libc.search(b'/bin/sh'))
libc.sym['system']
```
- sym[] {{accesses symbols (functions, variables)}} in the binary.
- search() {{finds byte patterns in the binary}}
- next() {{gets the first matchS}} <!--SR:!2024-12-17,3,250!2024-12-15,1,230!2024-12-15,1,230-->