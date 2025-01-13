# UwUSpirit
Author:

qwertyuiopp
Binary
Description
Solves 0

You... UwU!

awa... UwuwUUwuawauwUUwUwuQAQuwU...

UwU!!!


`nc phoenix-chal.firebird.sh 36036`


# Observations 

```c
index = UwUInt("UwU", 0, 0x10); // inputting an index, controlling the UwUUwUUwUUwU array
size = UwUInt("uWu", 0, 0x200); // how bytes to allocate for this particular chunk, size is between 0 - 0x200
```

the fact that the allowed chunk size, for each individual chunk of those indecies, is quite suspicious. But it is probably safe. Since the chunk size is big, we can probably not able to leak overflow and leak information of neighbour chunks 



```c
    puts("awa:");
    if (UwUUwUUwUUwU[index] != NULL) {
        puts(UwUUwUUwUUwU[index]);
    }
```

potentially leak something if `UwUUwUUwUUwU[index]`, which is our input, is never ended with null-terminator. Because puts prints until null terminator. So we might be able to leak information of the neighbour chunks


```c
// strcpy will keep copying until `\x00`. 
// If UwU_buf contains exactly 0x20 bytes without a null-terminator
// then it might overwrite the bonds beyond UUUwwUUU
strcpy(UUUwwUUU, UwU_buf);
```
this could probably be used for arw (?)


ahh... there's quite a lot that I am uncertain about, maybe I should move on to other pwn tasks lol



# stuff to consider when no further progress can be made 

1.    Potential heap consolidation attacks since you can free chunks
2.     The ability to allocate chunks of varying sizes could be used for heap feng shui
3.     The NULL pointer checks only prevent double-free but not use-after-free




# Attempt 1:
1. test with the behaviour of the program to find something really interesting
2. able to leak some addresses
If I can't complete these 2 goals in like the following 1 hour, then i am going to move on to some other pwn tasks


```
pwndbg> tele 0x5561ac8d3a00 100
00:0000│  0x5561ac8d3a00 ◂— 0
01:0008│  0x5561ac8d3a08 ◂— 0x31 /* '1' */
02:0010│  0x5561ac8d3a10 ◂— 0x6363636363636363 ('cccccccc')
... ↓     3 skipped
06:0030│  0x5561ac8d3a30 ◂— 0x4141414141414141 ('AAAAAAAA')
07:0038│  0x5561ac8d3a38 ◂— 0xe1
08:0040│  0x5561ac8d3a40 —▸ 0x7f5100eb1b20 (main_arena+96) —▸ 0x5561ac8d3b40 ◂— 0
09:0048│  0x5561ac8d3a48 —▸ 0x7f5100eb1b20 (main_arena+96) —▸ 0x5561ac8d3b40 ◂— 0
0a:0050│  0x5561ac8d3a50 ◂— 0x4141414141414141 ('AAAAAAAA')
```

wondering if there are some ways to fill `0xe1` up with up to 8 bytes so that `0x7f5100eb1b20` can be printed

`puts` has successfully printed something it shouldn't:
`awa:ccccccccccccccccccccccccccccccccAAAAAAAA\xe1`
I feel like being quite close to leaking a libc address. It is right after `0x0000000\xe1` but the null-bytes blocked `puts` there
here `\xe1` is the metadata, i.e. the size of that particular chunk

### immediate random thoughts
probably can use strcpy to fill that up?



# reason why `0x4545454545454545` was before `0x00000000000000e1`
```
0x561002708a10:	0x6363636363636363	0x6363636363636363
0x561002708a20:	0x6363636363636363	0x6363636363636363
0x561002708a30:	0x4545454545454545	0x00000000000000e1
0x561002708a40:	0x00007f4901d74b20	0x00007f4901d74b20
0x561002708a50:	0x4545454545454545	0x4545454545454545
0x561002708a60:	0x4545454545454545	0x4545454545454545
```

First, the reason why `0x00000000000000e1` became `e0` from `0x100` is that, 0x20 was allocated to a new chunk, and `0x4545454545454545` 8 bytes of `E` in the 0x100 bytes of `E` buffer still remains there

Now the questions become: how to make it become fully occupied with 8 bytes??? So that `puts` can keep printing stuff until the null bytes of `0x00007f4901d74b20` and leak the libc address

# more discoveries and attack plan
```
pwndbg> x/32gx &UUUwwUUU
0x55f3429f5060 <UUUwwUUU>:	0x4b4b4b4b4b4b4b4b	0x4b4b4b4b4b4b4b4b
0x55f3429f5070 <UUUwwUUU+16>:	0x4b4b4b4b4b4b4b4b	0x4b4b4b4b4b4b4b4b
0x55f3429f5080 <UwUUwUUwUUwU>:	0x000055f352d052a0	0x000055f352d053b0
0x55f3429f5090 <UwUUwUUwUUwU+16>:	0x000055f352d054c0	0x000055f352d055d0
0x55f3429f50a0 <UwUUwUUwUUwU+32>:	0x000055f352d056e0	0x0000000000000000
0x55f3429f50b0 <UwUUwUUwUUwU+48>:	0x0000000000000000	0x0000000000000000
0x55f3429f50c0 <UwUUwUUwUUwU+64>:	0x0000000000000000	0x0000000000000000
0x55f3429f50d0 <UwUUwUUwUUwU+80>:	0x0000000000000000	0x0000000000000000
0x55f3429f50e0 <UwUUwUUwUUwU+96>:	0x0000000000000000	0x0000000000000000
0x55f3429f50f0 <UwUUwUUwUUwU+112>:	0x0000000000000000	0x0000000000000000
0x55f3429f5100:	0x0000000000000000	0x0000000000000000
```
`UUUwwUUU` is right next to the array, can we do something about it? But there's no address leaking to defeat PIE at this point, probably not.....?

Since the free function `QAQ` allows us to free uninitialized data, probably a good plan is to overflow `UUUwwUUU` to `UwUUwUUwUUwU` array and free it to create a fake chunk?


but
```c
int main() {

	char UwU_buf[0x20] = {0};
    long long int UwU_num = 0;

    setup();

    while (1) {
        
        UwU_menu(); 
        UwU_num =  read(0, UwU_buf, 0x20);
        if (UwU_buf[UwU_num-1] == '\n')
            UwU_buf[UwU_num-1] = '\0';

        if (strcmp(UwU_buf, "UwU") == 0) UwU();
        else if (strcmp(UwU_buf, "awa") == 0) awa();
        else if (strcmp(UwU_buf, "QAQ") == 0) QAQ();

        // program just exits if the input matches what's in UUUwwUUU
        else if (strcmp(UwU_buf, UUUwwUUU) == 0) {
            puts("UUUwwUUU!");
            exit(0);
        }

        // copies input to UUUwwUUU if input does not match either of the above three
        // could maybe be used to arw
        else {
            puts("UwU...");    
            // strcpy will keep copying until `\x00`. 
            // If UwU_buf contains exactly 0x20 bytes without a null-terminator
            // then it might overwrite the bonds beyond UUUwwUUU
            strcpy(UUUwwUUU, UwU_buf);
        }
    }
	return 0;
}
```
```c
        UwU_num =  read(0, UwU_buf, 0x20);
        if (UwU_buf[UwU_num-1] == '\n')
            UwU_buf[UwU_num-1] = '\0';

```
here it seems like it's not allowing to use strcpy to overflow, using `sendafter` instead of `sendlineafter` to prevent adding `\n` does not work as well.

But I wonder if it is really not working or is it just the strcpy also copied null-bytes from the stack to `UUUwwUUU`.
```
0x55f9fde3e060 <UUUwwUUU>:	0x4747474747474742	0x4747474747474747
0x55f9fde3e070 <UUUwwUUU+16>:	0x4747474747474747	0x4747474747474747
0x55f9fde3e080 <UwUUwUUwUUwU>:	0x0000000000000000	0x0000000000000000 <----- still null without `\n`
```

## investigating strcpy vulnerability
I guess getting to know what's happening in strcpy in the context of this program would be the key to solving the challenge. But the behaviour of it seems to be quite weird. I am pretty much stuck at this point
testing exploit:
```py
gdb.attach(p, s)
payload = 'X' * 0x20 # fill the buffer completely 
p.sendafter('> ', payload) 

for i in range(6):
    add(i, 0x100, b'A'*0x100)  # No null terminator
```
Look at the following
```
   0x55f6cdbb1833 <main+87>     lea    rax, [rbp - 0x30]     RAX => 0x7ffd7f9110b0 ◂— 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
   0x55f6cdbb1837 <main+91>     mov    edx, 0x20             EDX => 0x20
   0x55f6cdbb183c <main+96>     mov    rsi, rax              RSI => 0x7ffd7f9110b0 ◂— 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
   0x55f6cdbb183f <main+99>     mov    edi, 0                EDI => 0
   0x55f6cdbb1844 <main+104>    call   read@plt                    <read@plt>
 
 ► 0x55f6cdbb1849 <main+109>    mov    qword ptr [rbp - 0x38], rax          [0x7ffd7f9110a8] <= 4
   0x55f6cdbb184d <main+113>    mov    rax, qword ptr [rbp - 0x38]          RAX, [0x7ffd7f9110a8] => 4
   0x55f6cdbb1851 <main+117>    sub    rax, 1                               RAX => 3 (4 - 1)
   0x55f6cdbb1855 <main+121>    movzx  eax, byte ptr [rbp + rax - 0x30]     EAX, [0x7ffd7f9110b3] => 0xa
   0x55f6cdbb185a <main+126>    cmp    al, 0xa                              0xa - 0xa     EFLAGS => 0x246 [ cf PF af ZF sf IF df of ]
   0x55f6cdbb185c <main+128>    jne    main+143                    <main+143>
──────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────
00:0000│ rsp 0x7ffd7f9110a0 ◂— 0
01:0008│-038 0x7ffd7f9110a8 ◂— 0x20 /* ' ' */
02:0010│ rsi 0x7ffd7f9110b0 ◂— 'UwU\nXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
03:0018│-028 0x7ffd7f9110b8 ◂— 'XXXXXXXXXXXXXXXXXXXXXXXX'
... ↓        2 skipped
06:0030│-010 0x7ffd7f9110d0 ◂— 0
07:0038│-008 0x7ffd7f9110d8 ◂— 0xcad72a3627cb6800
```
`UwU\nXXXXXXXXXXXXXXXXXXXXXXXXXXXX`: - not so sure what is this, seems like it is copying `UwU\n` which is from the next input to `rsi`
```
 ► 0x55f6cdbb187c <main+160>    call   strcmp@plt                  <strcmp@plt>
        s1: 0x7ffd7f9110b0 ◂— 0x5858585800557755 /* 'UwU' */
        s2: 0x55f6cdbb2281 ◂— 0x75577500557755 /* 'UwU' */
```
then somehow the program is going to identify these two to be the same and proceed to `UwU`

with
```py
gdb.attach(p, s)
payload = 'X' * 0x20 # fill the buffer completely 
p.sendafter('> ', payload) 
payload2 = p64(0xdeadbeef) # fill the buffer completely 
p.sendafter('> ', payload2) 
```
it shows something like this after copying `0xdeadbeef` to `UUUwwUUU`
```
   0x55d0e8f14936 <main+346>    call   strcpy@plt                  <strcpy@plt>
 
 ► 0x55d0e8f1493b <main+351>    jmp    main+77                     <main+77>
    ↓
   0x55d0e8f14829 <main+77>     mov    eax, 0                  EAX => 0
   0x55d0e8f1482e <main+82>     call   UwU_menu                    <UwU_menu>
 
   0x55d0e8f14833 <main+87>     lea    rax, [rbp - 0x30]
   0x55d0e8f14837 <main+91>     mov    edx, 0x20               EDX => 0x20
   0x55d0e8f1483c <main+96>     mov    rsi, rax
──────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────
00:0000│ rsp 0x7ffd51ead910 ◂— 0
01:0008│-038 0x7ffd51ead918 ◂— 8
02:0010│ rsi 0x7ffd51ead920 ◂— 0xdeadbeef
03:0018│-028 0x7ffd51ead928 ◂— 'XXXXXXXXXXXXXXXXXXXXXXXX'
... ↓        2 skipped
06:0030│-010 0x7ffd51ead940 ◂— 0
07:0038│-008 0x7ffd51ead948 ◂— 0xe7821dc246713800
────────────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────────────
 ► 0   0x55d0e8f1493b main+351
   1   0x7fddcd021d68 __libc_start_call_main+120
   2   0x7fddcd021e25 __libc_start_main+133
   3   0x55d0e8f141e5 _start+37
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> x/32gx &UUUwwUUU
0x55d0e8f17060 <UUUwwUUU>:	0x58585800deadbeef	0x5858585858585858
0x55d0e8f17070 <UUUwwUUU+16>:	0x5858585858585858	0x5858585858585858
0x55d0e8f17080 <UwUUwUUwUUwU>:	0x0000000000000000	0x0000000000000000
```
so i guess it is pretty much impossible to make it overflow into `UwUUwUUwUUwU`....(?)
```py
payload = b'X' * 0x20  
p.send(payload)        

p.recvuntil(b'UwU...') 

p.sendline(b'UwU')  

gdb.attach(p, s)

for i in range(6):
    add(i, 0x100, b'A'*0x100)

p.interactive()
```
will do the following: 
```
 ► 0x563c0106b936 <main+346>    call   strcpy@plt                  <strcpy@plt>
        dest: 0x563c0106e060 (UUUwwUUU) ◂— 0x5858585858585858 ('XXXXXXXX')
        src: 0x7ffe55c01730 ◂— 'U\n0\n256\nAAAAAAAAAAAAAAAAAAAAAAAA'
 
   0x563c0106b93b <main+351>    jmp    main+77                     <main+77>
    ↓
   0x563c0106b829 <main+77>     mov    eax, 0     EAX => 0
   0x563c0106b82e <main+82>     call   UwU_menu                    <UwU_menu>
 
   0x563c0106b833 <main+87>     lea    rax, [rbp - 0x30]
   0x563c0106b837 <main+91>     mov    edx, 0x20             EDX => 0x20
   0x563c0106b83c <main+96>     mov    rsi, rax
   0x563c0106b83f <main+99>     mov    edi, 0                EDI => 0
   0x563c0106b844 <main+104>    call   read@plt                    <read@plt>
 
   0x563c0106b849 <main+109>    mov    qword ptr [rbp - 0x38], rax
   0x563c0106b84d <main+113>    mov    rax, qword ptr [rbp - 0x38]
──────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────
00:0000│ rsp 0x7ffe55c01720 ◂— 0
01:0008│-038 0x7ffe55c01728 ◂— 0x20 /* ' ' */
02:0010│ rsi 0x7ffe55c01730 ◂— 'U\n0\n256\nAAAAAAAAAAAAAAAAAAAAAAAA'
03:0018│-028 0x7ffe55c01738 ◂— 'AAAAAAAAAAAAAAAAAAAAAAAA'
... ↓        2 skipped
06:0030│-010 0x7ffe55c01750 ◂— 0
07:0038│-008 0x7ffe55c01758 ◂— 0x5f8ab0a25fe0b700

```
'U\n0\n256\nAAAAAAAAAAAAAAAAAAAAAAAA' is actually the `add` line in the python script

```
pwndbg> x/32gx &UUUwwUUU
0x555a13e8a060 <UUUwwUUU>:	0x0a3635320a300a55	0x4141414141414141
0x555a13e8a070 <UUUwwUUU+16>:	0x4141414141414141	0x4141414141414141
0x555a13e8a080 <UwUUwUUwUUwU>:	0x0000555a30d9d200	0x0000000000000000
0x555a13e8a090 <UwUUwUUwUUwU+16>:	0x0000000000000000	0x0000000000000000
0x555a13e8a0a0 <UwUUwUUwUUwU+32>:	0x0000000000000000	0x0000000000000000
0x555a13e8a0b0 <UwUUwUUwUUwU+48>:	0x0000000000000000	0x0000000000000000
0x555a13e8a0c0 <UwUUwUUwUUwU+64>:	0x0000000000000000	0x0000000000000000
0x555a13e8a0d0 <UwUUwUUwUUwU+80>:	0x0000000000000000	0x0000000000000000
0x555a13e8a0e0 <UwUUwUUwUUwU+96>:	0x0000000000000000	0x0000000000000000
0x555a13e8a0f0 <UwUUwUUwUUwU+112>:	0x0000000000000000	0x0000000000000000
0x555a13e8a100:	0x0000000000000000	0x0000000000000000
0x555a13e8a110:	0x0000000000000000	0x0000000000000000
0x555a13e8a120:	0x0000000000000000	0x0000000000000000
0x555a13e8a130:	0x0000000000000000	0x0000000000000000
0x555a13e8a140:	0x0000000000000000	0x0000000000000000
0x555a13e8a150:	0x0000000000000000	0x0000000000000000
```

and then somehow `AAAAA...` seems to be copied back to UUUwwUUU
```
 ► 0x563c0106b936 <main+346>    call   strcpy@plt                  <strcpy@plt>
        dest: 0x563c0106e060 (UUUwwUUU) ◂— 'U\n0\n256\nAAAAAAAAAAAAAAAAAAAAAAAA'
        src: 0x7ffe55c01730 ◂— 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
```