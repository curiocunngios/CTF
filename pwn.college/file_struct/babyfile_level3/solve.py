from pwn import *

# Set up connection
#context.log_level = 'debug'
p = process('./babyfile_level3')  # or remote connection
s = '''
b * fread
'''


payload = p64(1) 


p.sendline(payload)

p.interactive()
