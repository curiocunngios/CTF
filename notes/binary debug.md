---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - binary
  - binary exploitation
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

# Sets logging level - debug shows {{all I/O in binary details}}
```py
context.log_level = 'debug' 
```
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