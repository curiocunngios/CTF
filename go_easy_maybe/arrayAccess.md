# Array access 
about the array access in assembly:
```as
    115a:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    115d:	83 e8 02             	sub    eax,0x2
    1160:	48 98                	cdqe
    1162:	48 8d 15 17 2f 00 00 	lea    rdx,[rip+0x2f17]        # 4080 <f> # loads base address
    1169:	0f b6 0c 10          	movzx  ecx,BYTE PTR [rax+rdx*1] # accessing just a byte from the addr  
```
- `mov    eax,DWORD PTR [rbp-0x4]` gets the {{array index}} ready. Specifically {{int(dword ptr, 4 bytes 32-bit) idx at address `rbp-0x4`}}
- `sub    eax,0x2` changes just the value of {{eax but not rbp_0x4}} 
- `cdqe` prepares the index for {{64-bit memory access}} by extending the sign from {{32-bit to 64-bit}} while preserving the sign by appending same {{31st sign}} since it's Two's complement
- `lea    rdx,[rip+0x2f17]` gets the base address of the array into rdx
- `movzx  ecx,BYTE PTR [rax+rdx*1]`, `rax+rdx*1` is like s[rax] retriving just one byte from the address and copied to ecx with zero-extension treating it as {{unsigned}}
- Together, these instructions likely represent C code like:
```c
f[]; // global array/string declared somewhere
// ...
c = f[idx - 2]; // where index is in rax
```


## Scaling factor 
`rax+rdx*1`
Let me explain both questions:

1. `rax+rdx*1` - Scaling Factor:
- The scaling factor is primarily for array access with different data types:
  - Scale 1: for bytes (uint8_t, char) - each element is 1 byte
  - Scale 2: for shorts (uint16_t) - each element is 2 bytes
  - Scale 4: for ints (uint32_t) - each element is 4 bytes
  - Scale 8: for longs/pointers (uint64_t) - each element is 8 bytes

Example:
```python
# With array of bytes (scale 1):
arr = bytearray([0x11, 0x22, 0x33, 0x44])
index = 2
value = arr[index]  # equivalent to arr + index*1
# Gets 0x33

# With array of shorts (scale 2):
arr = array('H', [0x1122, 0x3344])  # 16-bit values
index = 1
value = arr[index]  # equivalent to arr + index*2
# Gets 0x3344
```

If you used wrong scale:
```python
# If trying to read shorts with scale 1:
arr = array('H', [0x1122, 0x3344])
wrong_addr = base_addr + index*1  # would read wrong byte
# Might get 0x22 or 0x11 instead of 0x1122
```

