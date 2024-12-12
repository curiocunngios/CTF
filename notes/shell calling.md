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

sym[] accesses symbols (functions, variables) in the binary
If no libc, we'd need to calculate offsets manually based on leaks

search() finds byte patterns in the binary
next() gets the first matchS
If no libc, we'd need hardcoded offsets