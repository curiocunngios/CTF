# Array access 
about the array access in assembly:
```as
    11cc:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    11cf:	48 98                	cdqe
    11d1:	48 8d 15 08 2f 00 00 	lea    rdx,[rip+0x2f08]        # 40e0 <s>
    11d8:	0f b6 0c 10          	movzx  ecx,BYTE PTR [rax+rdx*1]
```
- `mov    eax,DWORD PTR [rbp-0x8]` gets the {{array index}} ready. Specifically {{int(dword ptr, 4 bytes 32-bit) idx at address `rbp-0x8`}}
- `cdqe` prepares the index for {{64-bit memory access}} by extending the sign from {{32-bit to 64-bit}} while preserving the sign by appending same {{31st sign}} since it's Two's complement
- `lea    rdx,[rip+0x2f08]` gets the base address of the array into rdx
- `movzx  ecx,BYTE PTR [rax+rdx*1]`, `rax+rdx*1` is like s[rax] retriving just one byte from the address and copied to ecx with zero-extension treating it as {{unsigned}}
- Together, these instructions likely represent C code like:
```c
f[]; // global array/string declared somewhere
// ...
c = f[idx]; // where index is in rax
```





