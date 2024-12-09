---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - memory
  - memory layout
  - GOT hijacking
tags:
  - flashcard/active/ctf/hi
  - function/index
  - language/in/English
---

# After GOT leak  
typical code  
??
```py
puts = int.from_bytes(r.recvuntil(b'\x7f'), 'little')

libc.address = puts - libc.sym['puts']

log.info(hex(libc.address))
``` 
## binary exploitation functions  
libc.sym[\<symbol\>] ::: gets the offset of a symbol (function/variable) within the libc binary. Output is int <!--SR:!2024-12-12,3,250!2024-12-12,3,250-->

log.info(\<many printable things>) ::: pwntools' logging function to print information, used for debugging <!--SR:!2024-12-12,3,250!2024-12-12,3,250-->

hex() ::: converts the number to hexadecimal string <!--SR:!2024-12-13,4,270!2024-12-12,3,250-->

## More functions for debugging  

pause()
??
- Temporarily stops script execution
- Prints "[*] Paused (press any key to continue)" and wait for users input before continuing
- To check things in debugger or verify state before proceeding <!--SR:!2024-12-12,3,250-->

## Reading address  
```py
int.from_bytes(r.recvuntil(b'\x7f'), 'little')
```
??
- receive bytes until '\x7f', what libc addresses typically end with e.g. `\xf0\xa7\xe4\xf7\xff\x7f`
- convert to backwards `0x7ffff7e4a7f0 ` and to int for typical libc base address calculation('little'specifies little-endian byte order) 

#### Example  
```py
If puts prints: \xf0\xa7\xe4\xf7\xff\x7f
recvuntil gets: \xf0\xa7\xe4\xf7\xff\x7f
int.from_bytes converts to: 0x7ffff7e4a7f0 (in little-endian)
```