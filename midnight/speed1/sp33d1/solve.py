from pwn import * 

s = '''
b * main
'''


binary = './run.sh'
p = process(binary)


gdb.attach(p, s)
p.sendline(b"A" * 0x30)


p.interactive()
