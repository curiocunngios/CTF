---
aliases:
  - debugging
tags:
  - flashcard/active/ctf
---

# Binary exploitation debugging

Sets logging level - debug shows all I/O in binary details
??
```py
context.log_level = 'debug' 
```
<!--SR:!2024-12-15,1,230-->

## Example use
```py
context.log_level = 'debug' # Sets logging level - debug shows all I/O
r.sendline(b"Hello")
# Shows:
# [DEBUG] Sent 6 bytes:
#     b'Hello\n'

r.recv()
# Shows:
# [DEBUG] Received 10 bytes:
#     b'Response\n'
```