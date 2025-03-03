from pwn import *
import time 

binary = './babyrop_level9.0_patched'
elf = ELF(binary)
libc = ELF('./libc.so.6')
context.binary = binary
p = process(binary)

gdb.attach(p, '''
b * 0x4150e0
b * challenge+286
b * challenge+481
''')

payload = flat(
	b'A' * 8,
)
p.sendline(payload)
p.interactive()
