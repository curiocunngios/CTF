---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - binary
tags:
  - flashcard/active/ctf/testing/temp
  - function/index
  - language/in/English
---

Without libc, we need to:
- Leak function addresses (like puts)
- Use those leaks to identify libc version
- Calculate offsets manually or use databases


Instead of libc.sym['system'], we'd use offsets:
```py
system_offset = 0x528f0  # Example offset
system_addr = libc_base + system_offset
```

Instead of next(libc.search(b'/bin/sh')):
```py
binsh_offset = 0x1a7e43  # Example offset
binsh_addr = libc_base + binsh_offset
```