---
aliases:
  - Libc file missing
  - no libc 
  - libc missing
tags:
  - flashcard/active/ctf/yo
---

# No libc file provided
Without libc, we need to:
- Use {{function address leaks to identify libc version}}
- Calculate {{offsets manually or use databases}}
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
<!--SR:!2024-12-17,3,250!2024-12-17,3,250-->