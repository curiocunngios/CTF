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
`Space` :: `%20` <!--SR:!2024-12-15,1,230-->
`/`    :: `%2F` <!--SR:!2024-12-18,4,270-->
`\`    :: `%5C` <!--SR:!2024-12-15,1,230-->
`?`    :: `%3F` <!--SR:!2024-12-15,1,230-->
Example:
```
Original path: ../../../etc/passwd
URL encoded:   ..%2F..%2F..%2Fetc%2Fpasswd
```
