---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - tools
tags:
  - flashcard/active/ctf/testing
  - function/index
  - language/in/English
---

#### Pwndbg Commands
Basic Commands :::  
??
- `continue` / `c`: {{Continue execution}}
- `next` / `n`: {{Step over}}
- `step` / `s`: {{Step into}}
- `finish`: {{Run until current function returns}}
- `break` / `b`: {{Set breakpoint}}
- `info registers` / `i r`: {{Show registers}}

Memory Examination :::
`x/[count][format][size] address` command formats:  
??
- Count: {{number of items to display}}
- Format: 
  - `x`: {{hex}}
  - `d`: {{decimal}}
  - `s`: {{string}}
  - `i`: {{instruction}}
- Size:
  - `b`: {{byte (1)}}
  - `h`: {{halfword (2)}}
  - `w`: {{word (4)}}
  - `g`: {{giant (8)}}

Common x command usage :: Examples of examining memory  
??
```text
x/wx $esp     # Examine word in hex at esp
x/20i $rip    # Show next 20 instructions
x/s $rdi      # Examine string at rdi
x/gx $rbp-0x8 # Examine 8-byte value in hex at rbp-0x8
```
### Pwntools Python
Basic Connection :: Establishing connection to target  
??  
```py
from pwn import *

# Local binary
p = process('./binary')

# Remote target
r = remote('address', port)

# Debug with GDB
p = gdb.debug('./binary', '''
    break main
    continue
''')
```

ELF Manipulation :: Loading and analyzing binaries  
??  
```py
# Load binary
elf = ELF('./binary')

# Get address of function/symbol
main_addr = elf.symbols['main']
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']

# Find ROP gadgets
rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address
```

Common I/O Operations :::  
??  
```py
# Receiving
data = p.recv()          # Receive available data
data = p.recvline()      # Receive until newline
data = p.recvuntil(b':') # Receive until delimiter
data = p.recvall()       # Receive everything until EOF

# Sending
p.send(payload)          # Send data
p.sendline(payload)      # Send data with newline
p.sendafter(b':', payload) # Send after receiving delimiter
```

Packing/Unpacking :: Converting between bytes and integers  
??  
```py
# Pack integers to bytes (little-endian)
p64(0x1234)  # => b'\x34\x12\x00\x00\x00\x00\x00\x00'
p32(0x1234)  # => b'\x34\x12\x00\x00'

# Unpack bytes to integers
u64(b'AAAAAAAA')  # => 0x4141414141414141
u32(b'AAAA')      # => 0x41414141
```

ROP Chain Building :: Creating Return-Oriented Programming chains  
??  
```
# Basic ROP
rop = ROP(elf)
rop.raw(pop_rdi)    # Add gadget address
rop.raw(bin_sh)     # Add /bin/sh address
rop.raw(system)     # Add system() address

# Alternative method
rop.system(bin_sh)  # Automatically builds system('/bin/sh')

# Convert to bytes
payload = rop.chain()
```


Format String Exploitation :: Writing to arbitrary memory  
??  
```py
# Read from address
payload = b'%7$s' + p64(target_addr)

# Write to address
payload = fmtstr_payload(offset, {
    target_addr: target_value
})
```

Shellcode Generation :: Creating shellcode for different architectures  
??  
```py
vmmap              # Show memory regions
search -8 0x1234   # Search for value in memory
telescope $rsp 20  # Show 20 qwords from rsp
stack 20          # Show 20 entries of stack
```

## Common Exploits Pattern
Buffer Overflow Basic Pattern :::  
??  
```py
payload = b'A' * offset    # Padding
payload += p64(ret_addr)   # Return address
payload += p64(pop_rdi)    # ROP gadget
payload += p64(bin_sh)     # /bin/sh address
payload += p64(system)     # system() address
```

Finding Offset :: Determine buffer overflow offset  
??  
```py
# Method 1: Pattern create
cyclic(100)               # Create pattern
cyclic_find(0x6161616161) # Find offset

# Method 2: Manual
payload = flat(['A'*8, 'B'*8, 'C'*8, 'D'*8])
```