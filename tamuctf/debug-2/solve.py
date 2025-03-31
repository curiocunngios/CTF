from pwn import * 

binary = './debug-2_patched'
elf = ELF(binary)
libc = ELF('./libc.so.6')


p = process(binary)
#p = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_debug-1")
s = '''
b * modify+260
b * debug+268
'''

p.sendline("1")


gdb.attach(p, s)
payload = flat(
	b'A' * 1
	#p64(0x404000+4),
	#p64(0xdeadbeef)


)
p.send(payload)



p.interactive()
