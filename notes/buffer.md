---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - memory
  - buffer
  - buffer overflow
  - overflow
  - binary 
  - binary exploitation
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

```
Higher addr   0x7fffffffdc00 [saved RBP]     Created first
              0x7fffffffdbc0 [buffer start]   Created next
Lower addr    0x7fffffffdb80 [......]        Created last
              ↓
              Stack grows this way
```              

```
Higher addr   0x7fffffffdc00 [saved RBP]     Overwritten last
              0x7fffffffdbc8 ["AAAA...""]    Filled next
Lower addr    0x7fffffffdbc0 ["AAAA"]        Filled first
              ↑
              Buffer fills this way
```