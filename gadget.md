A "gadget" is just a small sequence of assembly instructions ending in ret that we can use. The pop rdi; ret gadget is typically found in the existing program code, and looks like:

```as
pop rdi    ; take value from stack → put in rdi
ret        ; take next value from stack → jump there
```


```
Shellcode:
- Custom code we write and inject
- Needs executable stack/memory (blocked by NX)
- Example:
  \x31\xc0\x50\x68\x2f\x2f... (machine code for execve("/bin/sh"))

Gadget:
- Existing code pieces in the program
- Already in executable memory (part of the program!)
- Example:
  0x40052: pop rdi; ret    (found in program's code)
```

Where to find gadgets
```bash
# Using ROPgadget tool
ROPgadget --binary program | grep "pop rdi"
# This searches the program's code for useful instruction sequences
```



