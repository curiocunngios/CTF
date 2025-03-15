from pwn import * 

binary = './a.out'
p = process(binary)

s = '''
start
b 1
c
'''
p = gdb.debug(binary, s)
p.interactive()
