---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - memory
  - memory layout
  - GOT hijacking
tags:
  - flashcard/active/ctf/testing
  - function/index
  - language/in/English
---

# After GOT leak
typical code
??
```py

``` 
This part handles address leaks:
1. recvuntil(b'\x7f') waits for a byte that's typically in libc addresses
2. [-6:] takes last 6 bytes (addresses are 6 bytes + null padding)
3. ljust(8, b'\x00') adds null padding to make 8 bytes
4. u64() converts bytes to integer
puts_leak = u64(r.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))

Alternative way to handle leaks:
puts = int.from_bytes(r.recvuntil(b'\x7f'), 'little')