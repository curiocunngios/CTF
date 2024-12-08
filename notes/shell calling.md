---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - shell
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

```py
next(libc.search(b'/bin/sh'))
libc.sym['system']
```

sym[] accesses symbols (functions, variables) in the binary
If no libc, we'd need to calculate offsets manually based on leaks

search() finds byte patterns in the binary
next() gets the first match
If no libc, we'd need hardcoded offsets