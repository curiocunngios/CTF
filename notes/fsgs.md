---
aliases:
  - fs/gs 
  - fs/gs segment registers
tags:
  - flashcard/active/ctf
---

# The fs/gs segment register
The fs/gs segment register is a {{special memory region}} that is {{specifically designated for security purposes}}. <!--SR:!2024-12-17,3,250!2024-12-18,4,270--> 

fs/gs segement register is a memory region that:
- Is set up by the OS when {{program starts}}
- Is not {{easily accessible}} through normal memory reads
- Can only be {{accessed through specific instructions}} <!--SR:!2024-12-15,1,230!2024-12-17,3,250!2024-12-17,3,250--> 

Since this memory region is protected and safe, [stack canary values](canary.md) used for protecting buffer overflow is usually stored in fs:0x28 of this region 

