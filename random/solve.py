from pwn import *

# Simple payload
payload = b"A" * 0x10

# Start the process with the payload as argument
p = gdb.debug(['./a.out', payload], '''b * main ''')

p.interactive()
