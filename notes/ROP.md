---
aliases:
  - Return oriented programming 
tags:
  - flashcard/active/ctf
---

# Return oriented programming
Problem: We can't execute new code (NX)
Solution: Reuse existing code pieces!
```smali
Example - calling system("/bin/sh"):
[buffer fill     ] 
[pop rdi gadget  ] <- Return here first
["/bin/sh" addr  ] <- Gets popped into rdi
[system addr     ] <- Then return here
```
It's like building with Lego:
- Can't create new blocks (NX)
- But can {{arrange existing blocks (gadgets)}}
```py
from pwn import *
pop_rdi = 0x40052  # Found using ROPgadget

# Build ROP chain
payload = b"A" * 40                  # Buffer fill
payload += p64(pop_rdi)             # Use existing code
payload += p64(binsh_addr)          # "/bin/sh" string
payload += p64(system_addr)         # system() function

# This uses existing code to run:
# system("/bin/sh")
```
<!--SR:!2024-12-15,1,230-->