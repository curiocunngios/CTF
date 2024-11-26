---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - Linux
  - url
  - web
  - URL encoding 
  - encoding
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

# URL encoding 

URL encoding can be used to {{bypass the sanitization of some common characters like `/` that perform LFI }}
Space ::: %20
/    ::: %2F
\    ::: %5C
?    ::: %3F

```
Original path: ../../../etc/passwd
URL encoded:   ..%2F..%2F..%2Fetc%2Fpasswd

It's like saying:
.. / .. / .. /etc/passwd
   │    │    │
   These slashes are encoded to %2F
```
