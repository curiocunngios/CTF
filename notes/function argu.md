# Purposes of void arguments


### vuln is void
```
► 0x80493d8 <main+102>    call   vuln                        <vuln>
        arg[0]: 0xf7fc0400 —▸ 0xf7d68000 ◂— 0x464c457f
        arg[1]: 0
        arg[2]: 0
        arg[3]: 0x3e8
```
Just like in the previous gets() case, these aren't actually arguments - they're just values that happen to be on the stack when vuln() is called. pwndbg shows them but they're not used as arguments.


```
call   vuln
arg[0]: 0xf7fc0400 —▸ 0xf7d68000 ◂— 0x464c457f   # ELF magic number (0x7f 'ELF')
arg[1]: 0
arg[2]: 0
arg[3]: 0x3e8
```



These values are likely:

1. 0xf7fc0400: Points to the ELF header of a loaded library/binary (notice 0x464c457f is '.ELF' in hex)
2. The zeros and 0x3e8 (1000 in decimal): Could be:
- Local variables from main()
- Environment setup values
- Runtime initialization values
Leftover stack data


Even though pwndbg labels them as "arg[X]", they're not actually arguments because:

1.  vuln() is declared with no parameters
2. The calling convention wouldn't use them
3. They're just the next few stack values after the call instruction