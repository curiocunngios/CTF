from pwn import * 
from pwnlib.util.misc import run_in_new_terminal 

binary = './MercuryBlast'
context.binary = binary 

r = remote('localhost', 1337)
sleep(1)

pid = pidof('MercuryBlast')[0]

run_in_new_terminal(f'gdb -p {pid}')



r.interactive()
