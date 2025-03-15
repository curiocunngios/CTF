from pwn import * 

binary = './a.out'
p = process(binary)

s = '''
start
b 28
c
'''
p = gdb.debug(binary, s)
p.interactive()
