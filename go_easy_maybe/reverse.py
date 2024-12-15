import sys 
'''
rbp_0x4 = 0x2 
i = 2

for(True): # or other unconditional jump
    if (rbp_0x4 >= 0x24): # jbe bigger or equal 
        break
    rbp_0x8 = 0x0
    while(True):
        break

the below would be more logical if they are arguments in for loop 
eax = rbp_0x4
eax = eax - 2
eax = eax & 0xFFFFFFFF # cdqe extending bits (?)
ecx = eax + f
'''



'''
    1151:	c7 45 fc 02 00 00 00 	mov    DWORD PTR [rbp-0x4],0x2
    1158:	eb 3b                	jmp    1195 <main+0x4c>
    115a:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    115d:	83 e8 02             	sub    eax,0x2
    1160:	48 98                	cdqe
    1162:	48 8d 15 17 2f 00 00 	lea    rdx,[rip+0x2f17]        # 4080 <f> # loads base address
    1169:	0f b6 0c 10          	movzx  ecx,BYTE PTR [rax+rdx*1] # accessing just a byte from the addr     
'''
# eax = i, eax -= 2, cdqe extends eax to be rax (signed extension)
i = 2 # mov    DWORD PTR (int) [rbp-0x4],0x2
'''
# for ( int eax = i - 2 ; i >= ; i++){
}
'''
f = bytearray(0x1000000) # uninitialized in actual source 
s = bytearray(0x1000000) # uninitialized in actual source 
data = bytes([
    0x4b, 0x26, 0x44, 0x2d, 0x53, 0x6f, 0x57, 0x01,
    0x58, 0xd9, 0x49, 0x81, 0x64, 0x2c, 0x86, 0x50,
    0x6a, 0xde, 0x86, 0x0c, 0xc0, 0xc7, 0xa8, 0xbd,
    0x24, 0x54, 0xd2, 0x6b, 0xa3, 0xb7, 0xc0, 0x94,
    0xc0, 0x81, 0xa0, 0xad, 0x80, 0x00, 0x00, 0x00
])

# If you need to see it as ASCII where printable:
i = 2
while (i <= 0x24):   # this is 1195 <main+0x4c> perhaps

    '''
    eax = i     # mov    eax,DWORD PTR [rbp-0x4] # 115a i think
    eax = i - 2 # sub    eax,0x2
    rax = eax   # cdqe (potentially for larger stuff lol idk)
    '''
    #lea    rdx,[rip+0x2f17] # 4080 <f>
    '''
    char/ int f[100] = ?
    char *rdx = f
    ecx = rdx + rax (f[i-2])
    '''
    #movzx  ecx,BYTE PTR [rax+rdx*1]

  # or bytes(100). Just creating byte array ~ char f[100]; 
    # uninitialized in actual source
    # value = f[rax]
    ecx = f[i - 2]
    '''
    actually

    # Assembly:          # Python equivalent:
    eax = i - 2         index = i - 2
    rax = eax           # (Python doesn't need explicit int->long conversion)
    rdx = &f            # (Python doesn't expose memory addresses)
    ecx = rdx[rax]      value = f[index]    # or directly: value = f[i-2]
    '''

    eax = f[i - 1]

    ecx = ecx + eax

    cl = ecx & 0xFF # lower 8 bits

    f[i] = cl
    i = i + 1

    

'''
1195:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
1198:	83 f8 24             	cmp    eax,0x24
119b:	76 bd                	jbe    115a <main+0x11>
'''


j = 0

while (j <= 0x24):


    '''
    11a6:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    11a9:	48 98                	cdqe 
    11ab:	48 8d 15 2e 2f 00 00 	lea    rdx,[rip+0x2f2e]        # 40e0 <s>
    11b2:	48 01 d0             	add    rax,rdx
    11b5:	48 89 c6             	mov    rsi,rax
    '''
    # >>> add    rax,rdx
    
    input = s[j] # rax = rax + rdx (addr of s[j])

    # eax = 0 # just calling conventioons perhaps 
    # input = sys.stdin.buffer.read(1)
    s[j] = int.from_bytes(sys.stdin.buffer.read(1), 'little')

    ecx = s[j] & 0xFF

    eax = f[j] & 0xFF

    ecx = eax + ecx # f and s stores bytes, so they can be added together

    cl = ecx & 0xFF

    s[j] = cl

    j = j + 1

k = 0x0
p = 0x0 
for i in range(0x24):
    print(f[i])
while (p <= 0x24):
    esi = s[p]
    
    rcx = p+0x24
    rdx = 0xdd67c8a60dd67c8b

    rax = rcx
    result = rax * rdx
    # print("result here:", hex(result))
    rax = result & 0xFFFFFFFFFFFFFFFF
    #print("rax here:", hex(rax))
    rdx = result >> 64
    #print("rdx here:", hex(rdx))
    rdx = rdx >> 5
    #print("rdx here:", hex(rdx))
    # print("rdx here:", hex(rdx))
    rax = rdx
    rax = (rax << 3) + rdx
    rax = (rax << 2) + rdx
    
    
    rdx = rcx - rax # & 0xFFFFFFFFFFFFFFFF
    #print(rdx)
    #print("rdx here:", hex(rdx))

    eax = s[rdx]
    esi = esi ^ eax 
    #     print(hex(eax))
    ecx = esi 
    cl = ecx & 0xFF
    #print("s[p] here:", hex(s[p]))
    s[p] = cl

    edx = s[p]
    #print("edx here:", hex(edx))
    rax = data[p]
    # print("edx here:", hex(edx))
    dl = edx & 0xFF
    al = rax & 0xFF
    #print("dl here:", dl)
    #print("al here:", al)
    if (dl == al):
        # exactly 37 times 
        k = k + 1
    
    p = p + 1


if (k == 0x25):
    print(":D")
else:
    print(":(")
    








