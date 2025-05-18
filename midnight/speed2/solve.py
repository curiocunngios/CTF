from pwn import *

binary = './sp33d2'
p = process(binary)

s = '''
b * free
b * malloc
'''



p.sendline(b"1")

p.sendline(b"A" * 0x4)

gdb.attach(p, s)


p.interactive()
