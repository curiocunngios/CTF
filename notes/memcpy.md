---
aliases:
- memcopy
tags: 
- flashcard/active/ctf
---

# memcpy
Example usage:
```c
memcpy(canary, global_canary, CANARY_SIZE)
```
works like {{`canary = global canary`}} while CANARY_SIZE tells how bytes to copy <!--SR:!2024-12-14,1,230-->

## Compiler optimization
For small, fixed sizes copy, compiler replaces {{with direct moves}} <!--SR:!2024-12-14,1,226-->

Function call overhead {{would be more expensive}} than direct mov. {{Single CPU instruction (mov) is faster than function call}} <!--SR:!2024-12-14,1,226!2024-12-14,1,230-->

### Example replacement with direct `mov`
```as
; This is actually the memcpy of canary!
0x080494a9 <+32>:    mov    eax,0x804c054   
0x080494af <+38>:    mov    eax,DWORD PTR [eax]  
0x080494b1 <+40>:    mov    DWORD PTR [ebp-0x10],eax  ; Store into local canary
```
1. `mov    eax,0x804c054` ; {{loads address of global_canary}}
2. `mov    eax,DWORD PTR [eax] ` ; gets value of global_canary
3. `mov    DWORD PTR [ebp-0x10],eax`  ; Store into local canary <!--SR:!2024-12-14,1,226-->

