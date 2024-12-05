# The purposes of 

```
0x804934e <vuln+22>    sub    esp, 0xc              ESP => 0xffffce44 (0xffffce50 - 0xc)
   0x8049351 <vuln+25>    lea    eax, [ebp - 0x6c]     EAX => 0xffffce5c —▸ 0xf7def103 (_IO_file_overflow+227) ◂— add esp, 0x10
```

# is:


```
sub    esp, 0xc              # Make space for function argument(s)
lea    eax, [ebp - 0x6c]     # Calculate buffer address
```

Specifically:

- sub esp, 0xc allocates 12 bytes on stack for argument(s)
- Standard x86 calling convention requires stack to be 16-byte aligned
Making space for upcoming push eax
- lea eax, [ebp - 0x6c] gets the address of the buffer
- Buffer starts 0x6c (108) bytes below EBP
- This will be the argument for gets() - where to store input
LEA (Load Effective Address) calculates address without reading memory

So this is setting up the stack frame for a function call with one argument (the buffer address where gets() will store input).




```
add    esp, 0x10    # Clean up stack after gets() call
                    # Restores ESP to what it was before args were pushed

sub    esp, 0xc     # Prepare stack space for next function call (puts)
                    # Aligns stack and makes space for argument
```


More specifically:

add esp, 0x10:
- Removes the space used for gets() arguments and alignment
- 0x10 (16) bytes to maintain proper stack alignment
sub esp, 0xc:
- Allocates 12 bytes for puts() argument
- Will be followed by push eax (4 bytes)
- Total 16 bytes again for alignment (0xc + 4 = 0x10)


The compiler generates these adjustments to:

- Maintain proper stack alignment (16 bytes)
- Clean up after function calls
- Prepare stack space for next function call