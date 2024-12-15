data = bytes([
    0x4b, 0x26, 0x44, 0x2d, 0x53, 0x6f, 0x57, 0x01,
    0x58, 0xd9, 0x49, 0x81, 0x64, 0x2c, 0x86, 0x50,
    0x6a, 0xde, 0x86, 0x0c, 0xc0, 0xc7, 0xa8, 0xbd,
    0x24, 0x54, 0xd2, 0x6b, 0xa3, 0xb7, 0xc0, 0x94,
    0xc0, 0x81, 0xa0, 0xad, 0x80, 0x00, 0x00, 0x00
])

result = ""
for i in range(36):
    '''
    rcx = i+0x24
    rdx = 0xdd67c8a60dd67c8b

    rax = rcx
    yes = rax * rdx
    # print("result here:", hex(result))
    rax = yes & 0xFFFFFFFFFFFFFFFF
    #print("rax here:", hex(rax))
    rdx = yes >> 64
    #print("rdx here:", hex(rdx))
    rdx = rdx >> 5
    # print("rdx here:", hex(rdx))
    rax = rdx
    rax = (rax << 3) + rdx
    rax = (rax << 2) + rdx
    
    '''
    # rdx = rcx - rax # & 0xFFFFFFFFFFFFFFFF
    #eax = data[i + 36]
    if i == 0:
        hi = data[i] ^ data[i]
    else:
        hi = data[i] ^ data[i]
    #print(type(chr(hi)))
    #print(type(result))
    result += chr(hi)

print(result)
