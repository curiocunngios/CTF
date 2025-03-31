from pwn import * 

binary = './rop-thirteen'

p = process(binary)
s = '''
b * main
'''

p.sendline("SSSSS")

gdb.attach(p, s)



payload = flat(
	b'B' * 8,
	b'B' * 0x8
)

p.sendline(payload)


p.interactive()
