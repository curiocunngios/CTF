```
[0x804a028] fflush@GLIBC_2.0 -> 0xf7b72e00 (fflush) ◂— push ebp
```

above is a got entry, my question is. FOr format string attack (or potentially other got hijacking techn iques) why can't we directly overwrite 0xf7b72e00 to make it point to something else, but have to overwrite 0x804a028? When I overwrite 0xf7b72e00 directly, it shows 
```
► 0xf7b5aca7 <printf_positional+3511>    mov    byte ptr [esi], al     [fflush] <= 0x23
   0xf7b5aca9 <printf_positional+3513>    jmp    printf_positional+1235      <printf_positional+1235>
    ↓
   0xf7b5a3c3 <printf_positional+1235>    mov    edx, dword ptr [ebp + 0x14]     EDX, [0xffffbee8] => 0xffffce63 ◂— 0x303030 /* '000' */
   0xf7b5a3c6 <printf_positional+1238>    mov    eax, dword ptr [ebp + 0x18]     EAX, [0xffffbeec] => 0xffffce66 ◂— 0x83f9f700
   0xf7b5a3c9 <printf_positional+1241>    sub    esp, 4                          ESP => 0xffffbddc (0xffffbde0 - 0x4)
   0xf7b5a3cc <printf_positional+1244>    add    ebp, 0x34                       EBP => 0xffffbf08 (0xffffbed4 + 0x34)
   0xf7b5a3cf <printf_positional+1247>    sub    eax, edx                        EAX => 3 (0xffffce66 - 0xffffce63)
   0xf7b5a3d1 <printf_positional+1249>    push   eax
   0xf7b5a3d2 <printf_positional+1250>    push   edx
   0xf7b5a3d3 <printf_positional+1251>    push   edi
   0xf7b5a3d4 <printf_positional+1252>    call   __printf_buffer_write       <__printf_buffer_write>
```


You can't directly overwrite 0xf7b72e00 because:

1. Memory Protection: The address 0xf7b72e00 is in the libc space which is typically marked as read-only memory. You'll get a segmentation fault trying to write there.

2. GOT Table Purpose: The GOT (Global Offset Table) entry at 0x804a028 is specifically designed to be writable. It's a table in the writable data segment that holds pointers to the actual function implementations.

The process works like this:
- Program calls fflush
- Looks up fflush in PLT
- PLT checks GOT entry at 0x804a028
- GOT entry (0x804a028) points to actual fflush implementation (0xf7b72e00)

We overwrite the GOT entry (0x804a028) because:
- It's in writable memory
- It's the redirection point that the program uses to find the actual function
- Changing it will redirect the program flow when it tries to call that function

This is why format string attacks typically target GOT entries rather than the actual function addresses in libc.


