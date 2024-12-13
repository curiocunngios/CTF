---
aliases:
  - GOT hijacking address leak 
  - libc function address leak
tags:
  - flashcard/active/ctf
---
# GOT leak 
Flow of GOT leak, using puts(puts_got) as example:

```apache
1. We make puts print the contents of its own GOT entry
2. Instead of puts printing a string, we give it address 0x601018 (puts_got)
3. puts reads from 0x601018 and prints what's there: 0x7ffff7a649c0
4. 0x7ffff7a649c0 is the actual address of puts in libc!
```

# After GOT leak
typical code
??
```py
puts = int.from_bytes(r.recvuntil(b'\x7f'), 'little')

libc.address = puts - libc.sym['puts']

log.info(hex(libc.address))
```
<!--SR:!2024-12-16,3,250-->

## binary exploitation functions
```py
libc.sym[<symbol>] 
```
??
gets the offset of a symbol (function/variable) within the libc binary. Output is int <!--SR:!2024-12-17,3,230-->

```py
log.info(<many printable things>) 
```
??
pwntools' logging function to print information, used for debugging <!--SR:!2024-12-17,3,230-->

```py
hex()
```
converts the number to hexadecimal string 

## More functions for debugging
```py
pause()
```
??
- Temporarily stops script execution
- Prints "[*] Paused (press any key to continue)" and wait for users input before continuing
- To check things in debugger or verify state before proceeding <!--SR:!2024-12-16,3,250-->

## Reading address
```py
int.from_bytes(r.recvuntil(b'\x7f'), 'little')
```
??
- receive bytes until '\x7f', what libc addresses typically end with e.g. `\xf0\xa7\xe4\xf7\xff\x7f`
- convert to backwards `0x7ffff7e4a7f0 ` and to int for typical libc base address calculation('little'specifies little-endian byte order) <!--SR:!2024-12-16,3,250--> 

#### Example  
```py
If puts prints: \xf0\xa7\xe4\xf7\xff\x7f
recvuntil gets: \xf0\xa7\xe4\xf7\xff\x7f
int.from_bytes converts to: 0x7ffff7e4a7f0 (in little-endian)
```


