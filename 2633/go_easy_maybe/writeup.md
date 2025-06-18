# initial observation:
- starts program 
- program waits for input
- input stuff
- certain amount of inputs leads to `:(` emoji

# Inpsecting assembly source
This would be the extreme details into the assembly instructions of the binary
- skip the rest of the sections and go straight to main since it's where the program actually starts and do stuff 

## typical function prologue
```as
    1149:	55                   	push   rbp
    114a:	48 89 e5             	mov    rbp,rsp
    114d:	48 83 ec 10          	sub    rsp,0x10
```
- Saving `old rbp` to restore later when `leave` is executed 
- points `rbp` to where `rsp` is, to set up the **new base pointer** for the frame
- allocate 16 bytes for **local variables**

### Setting up a variable 
there are several lines in the code, for example, one right after function prologue is something like the following:
```as
1151:	c7 45 fc 02 00 00 00 	mov    DWORD PTR [rbp-0x4],0x2
```
which {{basically like making a variable}} in C. Tecnically, it is just moving the value `0x2`, which is **an integeer** denoted by **DWORD PTR** beside the memory reference. The variable is put into the location that is exactly 4 bytes below `rbp`. I am not exactly sure but I guess it was the instruction `48 83 ec 10          	sub    rsp,0x10` that took up the previous 4 bytes. The integer value (DWORD PTR) itself would also take 4 bytes. That is why the next time we see something similar 
- `119d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0`, it is then in the location 4 more bytes below `rbp`

### loop 
- There are in total 3 loops in the program 
- The loops can be translated to while loop in python
- They are all written with a similar pattern as follow:
#### Loop start with unconditional jump
```as
1158:	eb 3b                	jmp    1195 <main+0x4c>
```
The "jump" probably goes to the area where the loop checks condition. For example,
`i <= 24` in `while(i <= 24)`.
As `1195` in the above example go straight to comparing stuff:
```as
    1195:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    1198:	83 f8 24             	cmp    eax,0x24
    119b:	76 bd                	jbe    115a <main+0x11>  
```
You may wonder why do we need to move `DWORD PTR [rbp-0x4]` inside eax before comparing.
Because:
- **x86 architecture can't directly compare a memory location with an immediate value** in a single instruction.
- Performance: Even if it were possible, doing memory operations is **slower than** register operations. By loading into eax first:
1. The value is in a {{fast-access register}}
2. Can be reused without additional memory reads if needed
3. More efficient {{for the CPU's pipeline}}

`119b:	76 bd                	jbe    115a <main+0x11> `
- this line is one of the main components of the loop
- `jbe` means "Jump if below or equal" 
- Therefore, if the variable `rbp_0x4` <= `0x24`, the program jumps right back to `115a`, which is `115a:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]` the actual starting line of the function

The program has in total 3 loops and the other two has the exact same written pattern and even comparsion value
- Second loop 
```as
Variable definition before loop:
119d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0

Loop starts:
11a4:	eb 5b                	jmp    1201 <main+0xb8>

Comparison area:
1201:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
1204:	83 f8 24             	cmp    eax,0x24
1207:	76 9d                	jbe    11a6 <main+0x5d>
```

- Third loop 
```as
Variable definition before loop:
1209:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
1210:	c7 45 f0 00 00 00 00 	mov    DWORD PTR [rbp-0x10],0x0

Loop starts:
1217:	e9 8e 00 00 00       	jmp    12aa <main+0x161>

Comparison area:
12aa:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
12ad:	83 f8 24             	cmp    eax,0x24
12b0:	0f 86 66 ff ff ff    	jbe    121c <main+0xd3>
```

#### Array accessing
The program has been making use of specifically 2 arrays to perform some operations
We can tell that they are most probably array from the following observations:
Assembly instructions:
```as
115a:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
115d:	83 e8 02             	sub    eax,0x2
1160:	48 98                	cdqe
1162:	48 8d 15 17 2f 00 00 	lea    rdx,[rip+0x2f17]        # 4080 <f> # loads base address
1169:	0f b6 0c 10          	movzx  ecx,BYTE PTR [rax+rdx*1] # accessing just a byte from the addr  
```
- `lea    rdx,[rip+0x2f17] ; rax+rdx*1`: **base address + offset** pattern. Where `lea` first loads the base address of the array i.e. `f[0]` into `rdx` 
- Then, offset `rax` which was **extended from eax** using cdqe is also added inside the memory reference to access a certain slot of the array 
- In this case it is something like `f[rbp_0x4 - 2]`
- `*1` in `[rax+rdx*1]` is the **scaling factor** which is primarily for array access with {{different data types}}
  - Scale 1: for bytes (uint8_t, char) - each element is 1 byte
  - Scale 2: for shorts (uint16_t) - each element is 2 bytes
  - Scale 4: for ints (uint32_t) - each element is 4 bytes
  - Scale 8: for longs/pointers (uint64_t) - each element is 8 bytes
- `# 4080 <f>` is likely the {{actual name of the variable}} declared in the original c program
 
`<f>` in this case specifically refers to this segment in the .data section
```
4080 00010000 00000000 00000000 00000000  ................
4090 00000000 00000000 00000000 00000000  ................
40a0 00000000 00                          .....
```
which can be represent as the following in python:
```py
f = bytearray([
    0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00
]) 
```

The array addressing can be split into 2 parts:
- Offset calculation
```as
mov    eax,DWORD PTR [rbp-0x4]  # load i
sub    eax,0x2                  # i-2
```
which setups the exact position to read
- Array reading 
```as
movzx  ecx,BYTE PTR [rax+rdx*1]
```
which `BYTE PTR` indicates that we are **reading a single byte** 

#### bits, register extension
Before accessing an array, `cdqe` was used to extend `eax` from being 32-bits to being `rax` having 64-bits
- It is used because of the requirement of x86_64 (64-bit) architecture on memory addressing, which {{requires to use 64-bit registers on memory addressing}}, even if you're only accessing a small memory area that could fit in 32 bits.
- This is likely because of the memory model of x86_64 since a {{flat 64-bit address space}} is used

With the knowledge we learnt from the previous array accessing, we can easily tell that the following
```as
    115a:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    115d:	83 e8 02             	sub    eax,0x2
    1160:	48 98                	cdqe
    1162:	48 8d 15 17 2f 00 00 	lea    rdx,[rip+0x2f17]        # 4080 <f> # loads base address
    1169:	0f b6 0c 10          	movzx  ecx,BYTE PTR [rax+rdx*1] # accessing just a byte from the addr

    116d:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    1170:	83 e8 01             	sub    eax,0x1
    1173:	48 98                	cdqe
    1175:	48 8d 15 04 2f 00 00 	lea    rdx,[rip+0x2f04]        # 4080 <f>
    117c:	0f b6 04 10          	movzx  eax,BYTE PTR [rax+rdx*1] 
```
are just 
```py
ecx = f[rbp_0x4-2]

eax = f[rbp_0x4-1]
```

Later:
```as
    1180:	01 c1                	add    ecx,eax


    1182:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    1185:	48 98                	cdqe
    1187:	48 8d 15 f2 2e 00 00 	lea    rdx,[rip+0x2ef2]        # 4080 <f>
    118e:	88 0c 10             	mov    BYTE PTR [rax+rdx*1],cl
    1191:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
```
is like 
```c
// Fibonacci sequence
f[rbp_0x4] = f[rbp_0x4 - 2] + f[rbp_0x4 - 1] // from previous assignment
```
The two numbers in the array are added together, put into `ecx`, then again put into array `f` at index `rbp_0x4` vai `cl`, the lower **8-bits** of `ecx` which stores the previous addition value

We use 8-bit registers (like `cl`, `al`, `dl`) when storing into an array of bytes because:

1. **Size Matching**:
   - If the array is declared as bytes (like `unsigned char` in C or `bytearray` in Python), {{each element is 8 bits}}
   - Using larger registers would try to {{write too many bits}}
   ```c
   unsigned char f[];  // each element is 8 bits
   ```

2. **Memory Conservation**:
   - If we only need to store values 0-255, using more than 8 bits would waste memory
   - `mov BYTE PTR [rax+rdx*1],cl` {{writes exactly one byte}}

3. **Overflow Handling**:
   - Using `cl` (lower 8 bits) automatically handles overflow
   - If the addition in `add ecx,eax` produces a value > 255
   - Only the lower 8 bits are stored, effectively doing {{a `& 0xFF` operation}}

Example:
```as
ecx = 200 (11001000 in binary)
eax = 100 (01100100 in binary)
add ecx,eax  -> 300 (100101100 in binary)

When stored in cl (8 bits):
300 -> 44 (00101100 in binary)
```
like doing:
```c
result = (200 + 100) & 0xFF
// 300 & 255 = 44
```
- fitting something into a register that only stores 8-bits may cause information lost, which sometimes is intentional, if not it is important to ensure it certainly fits 

#### First loop 
Short conclusion of everything above, the first loop and a bit before that is something like this:
```py
i = 0x2 # i = 2
while (i <= 0x24):
    f[i] = (f[i - 2] + f[i - 1]) & 0xFF # cl register

    i = i + 1
```
#### Second loop 
```py
j = 0x0
while (j <= 0x24):
    s[j] = int.from_bytes(sys.stdin.buffer.read(1), 'little') # scanf(%c, s[j])

    s[j] = (s[j] + f[j]) & 0xFF
    j = j + 1
```
- `s[j] = int.from_bytes(sys.stdin.buffer.read(1), 'little')` simulates `scanf(%c, s[j])`

Corresponding assembly instruction:

```as
    11a4:	eb 5b                	jmp    1201 <main+0xb8>

    11a6:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    11a9:	48 98                	cdqe 
    11ab:	48 8d 15 2e 2f 00 00 	lea    rdx,[rip+0x2f2e]        # 40e0 <s>                   ; gets base address of s, s[0]   
    11b2:	48 01 d0             	add    rax,rdx
    11b5:	48 89 c6             	mov    rsi,rax                                              ; becomes 2nd argument for scanf function call 

    11b8:	48 8d 05 45 0e 00 00 	lea    rax,[rip+0xe45]        # 2004 <_IO_stdin_used+0x4>   ; gets %c (read from hexdump)
    11bf:	48 89 c7             	mov    rdi,rax                                              ; becomes 1st argument for scanf function call
    11c2:	b8 00 00 00 00       	mov    eax,0x0                                              ; calling convention for variadic functions
    11c7:	e8 74 fe ff ff       	call   1040 <__isoc99_scanf@plt>                            ; scanf is called 
```

```py
    s[j] = (s[j] + f[j]) & 0xFF
    j = j + 1
```
is just similar to the one in first loop:
```as
11cc:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    11cf:	48 98                	cdqe
    11d1:	48 8d 15 08 2f 00 00 	lea    rdx,[rip+0x2f08]        # 40e0 <s>
    11d8:	0f b6 0c 10          	movzx  ecx,BYTE PTR [rax+rdx*1]


    11dc:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    11df:	48 98                	cdqe
    11e1:	48 8d 15 98 2e 00 00 	lea    rdx,[rip+0x2e98]        # 4080 <f>
    11e8:	0f b6 04 10          	movzx  eax,BYTE PTR [rax+rdx*1]

    11ec:	01 c1                	add    ecx,eax

    11ee:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    11f1:	48 98                	cdqe
    11f3:	48 8d 15 e6 2e 00 00 	lea    rdx,[rip+0x2ee6]        # 40e0 <s>
    11fa:	88 0c 10             	mov    BYTE PTR [rax+rdx*1],cl

    11fd:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
```

#### Third loop 
- Weird encoding 
```
121c:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
121f:	48 98                	cdqe
1221:	48 8d 15 b8 2e 00 00 	lea    rdx,[rip+0x2eb8]        # 40e0 <s>
1228:	0f b6 34 10          	movzx  esi,BYTE PTR [rax+rdx*1]
122c:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
122f:	48 98                	cdqe
1231:	48 8d 48 24          	lea    rcx,[rax+0x24]
1235:	48 ba 8b 7c d6 0d a6 	movabs rdx,0xdd67c8a60dd67c8b
123c:	c8 67 dd 
123f:	48 89 c8             	mov    rax,rcx
1242:	48 f7 e2             	mul    rdx
1245:	48 c1 ea 05          	shr    rdx,0x5
1249:	48 89 d0             	mov    rax,rdx
124c:	48 c1 e0 03          	shl    rax,0x3
1250:	48 01 d0             	add    rax,rdx
1253:	48 c1 e0 02          	shl    rax,0x2
1257:	48 01 d0             	add    rax,rdx
125a:	48 29 c1             	sub    rcx,rax
125d:	48 89 ca             	mov    rdx,rcx
```
I don't understand what exactly does it do, I translate it to python code directly as follow:
```py
rcx = k + 0x24
mul = rcx * 0xdd67c8a60dd67c8b
rax = mul & 0xFFFFFFFFFFFFFFFF
rdx = (mul >> 64) & 0xFFFFFFFFFFFFFFFF
rdx = rdx >> 5
rax = rdx
rax = rax << 3 
rax = rax + rdx 
rax = rax << 2 
rax = rax + rdx 
rcx = rcx - rax
rdx = rcx & 0xFFFFFFFF
```
And...
```as
1260:	48 8d 05 79 2e 00 00 	lea    rax,[rip+0x2e79]        # 40e0 <s>
1267:	0f b6 04 02          	movzx  eax,BYTE PTR [rdx+rax*1]

126b:	31 c6                	xor    esi,eax
126d:	89 f1                	mov    ecx,esi

126f:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
1272:	48 98                	cdqe
1274:	48 8d 15 65 2e 00 00 	lea    rdx,[rip+0x2e65]        # 40e0 <s>
127b:	88 0c 10             	mov    BYTE PTR [rax+rdx*1],cl

127e:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
1281:	48 98                	cdqe
1283:	48 8d 15 56 2e 00 00 	lea    rdx,[rip+0x2e56]        # 40e0 <s>
128a:	0f b6 14 10          	movzx  edx,BYTE PTR [rax+rdx*1]

128e:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
1291:	48 98                	cdqe
1293:	48 8d 0d a6 2d 00 00 	lea    rcx,[rip+0x2da6]        # 4040 <data>
129a:	0f b6 04 08          	movzx  eax,BYTE PTR [rax+rcx*1]


129e:	38 c2                	cmp    dl,al
12a0:	75 04                	jne    12a6 <main+0x15d>
12a2:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
12a6:	83 45 f0 01          	add    DWORD PTR [rbp-0x10],0x1
```
is something like:
```py
s[k] = s[k] ^ s[rdx]    # esi was set to be s[k] earlier
                        # direct index access with lea    rax,[rip+0x2e79] ; movzx  eax,BYTE PTR [rdx+rax*1]

dl = s[k] & 0xFF
al = data[k] & 0xFF

if (dl == al):
    count = count + 1
k = k + 1
```


## Lastly
`count` i..e the number of correct matching characters determine where we go in here
```py
if (count == 0x25):
    print(":D")
else:
    print(":(")
```