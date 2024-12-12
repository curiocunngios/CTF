---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - memory
  - memory region
  - binary exploitation
tags:
  - flashcard/active/ctf/hi
  - function/index
  - language/in/English
---

# The fs/gs segment register
The fs/gs segment register is a {{special memory region}} that is {{specifically designated for security purposes}}. <!--SR:!2024-12-15,4,270!2024-12-12,1,230-->

fs/gs segement register is a memory region that:
?   
- Is set up by the OS when program starts
- Is not easily accessible through normal memory reads
- Can only be accessed through specific instructions

Since this memory region is protected and safe, [stack canary values](canary.md) used for protecting buffer overflow is usually stored in fs:0x28 of this region 

