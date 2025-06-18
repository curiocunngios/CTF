# ret2libc 

- hijack a libc function's GOT entry and write it as `system()` or `execve()`
- feed in the parameter ("/bin/sh")

## address of `system()`

To get the address of `system()`, we need to 
- get correct libc version for the proper function offset
- leak a libc address 
- calculate libc base address
- elf.sym['system']

## leaking libc addresses 

To leak a libc function address, we can 
- print out the address in GOT in some way
```
[0x555555558060] atoi@GLIBC_2.2.5 -> 0x5555555550c0 ◂— endbr64
```
for example, print it out like 
```c
puts(0x555555558060), printf(0x555555558060), printf(“%s”, 0x555555558060)
```
  - return addresses that aren't overwritten (?)

# Format string specifiers 
```
"%6$p"  # Often libc or binary addresses
"%7$p"  # 
"%8$p"  # 
"%9$p"  # Often __libc_start_main+243
"%10$p" # 
"%11$p" # Often __libc_start_main+243 or stack addresses
"%12$p" # 
"%13$p" # Often stack canary location
```

```py
# Example format string exploit
payload = b"%7$s"    # Read GOT entry
payload += p64(elf.got['puts']) # Address of puts GOT entry
```
- look around the stack for any address that happen to be in libc 
  - pointers to special data structions inside libc (fastins or heaps, etc.) 
```py
# Common stack offsets to find libc addresses
payload = b"%9$p"  # Often contains libc address
payload = b"%11$p" # Common location for __libc_start_main+xxx
```

## Calling `system()`

When we succuessfully get to `system()`. We need to be able to call it with `/bin/sh` being the first argument 

libc contains the string actually : `next(libc.search('/bin/sh’))`


- we need to change rdi to the string 
- or change the value rdi points to, to become the string                               