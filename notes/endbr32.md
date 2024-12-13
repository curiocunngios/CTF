---
aliases:
  - linux executable in binary 
  - linux exe in binary 
tags:
  - flashcard/active/ctf
---

# endbr32

endbr32 stands for {{END Branch 32-bit}} is a {{CPU instruction}} that's part of Intel's Control-flow Enforcement Technology (CET) <!--SR:!2024-12-17,3,250!2024-12-15,1,230--> 

## location of endbr32
??
It is first found at the [function prologue](<start of function.md>)
```
►    0x8049281 <vuln>       endbr32           ; Says "This is a valid entry point"
     0x8049285 <vuln+4>     push   ebp        ; Normal function prologue
     0x8049286 <vuln+5>     mov    ebp, esp
```
<!--SR:!2024-12-18,4,270-->

## What does endbr32 do
endbr32
- Marks valid {{indirect branch targets}}
- Prevents attackers from {{jumping to middle of functions. Specifically, CPU would stop the jump}}
- Part of {{control-flow protection}} mechanism
- prevent {{ROP}} attacks <!--SR:!2024-12-15,1,230!2024-12-18,4,270!2024-12-15,1,230!2024-12-18,4,270-->



### Modern Context of endbr32:
endbr32 is:
- Common in {{newer binaries}}
- Part of modern compiler {{security features}}
- Can be disabled with {{compiler flags}} if needed
- Often seen with other protections like canaries <!--SR:!2024-12-15,1,230!2024-12-15,1,230!2024-12-17,3,250--> 
