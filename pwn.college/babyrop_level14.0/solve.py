from pwn import *
p = remote('localhost', 1337)

offset = 0x60
s = '''
b * challenge+388
'''
gdb.attach(p, s)
payload = flat(
	b'A'* 0x58,
	
)
p.send(payload)
p.interactive()
