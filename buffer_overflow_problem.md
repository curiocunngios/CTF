```
pwndbg> x/6gx $rbp-0x10
0x7fffffffdcf0: 0x00676e6968746f6e      0x00007fffffffdca0
0x7fffffffdd00: 0x4141414141414141      0x4141414141414141
0x7fffffffdd10: 0xabfefefefefefefe      0x00007ffff7ddcd00
```

the overflow skipped over `0x00007fffffffdca0` completely 



Looking at the code and memory layout, that value at $rbp-0x8 (0x00007fffffffdca0) is preserved because it's being actively used by the program - it's the result of the strstr call stored as a local variable:
```
mov    QWORD PTR [rbp-0x8],rax     # Stores strstr result at [rbp-0x8]
```

Memory layout:
```
[rbp-0x60]  Buffer start (where gets writes)
...
[rbp-0x10]  "nothing" string
[rbp-0x8]   strstr result (0x00007fffffffdca0) <- This gets preserved
[rbp]        Saved rbp (overwritten with 0x4141414141414141)
[rbp+0x8]    Return address (overwritten with 0x4141414141414141)
```

The value 0x00007fffffffdca0 stays because:

It points to where "UwUUwU" is found in your input (start of buffer)
It's written after gets by the strstr call  
Your overflow with "A"s comes before this value is written
The sequence is:

gets writes your input (overflow with "A"s)
strstr runs and writes 0x00007fffffffdca0 to [rbp-0x8]
That's why you see this value preserved despite the overflow
If you put enough "A"s before "UwUUwU" in your input, you might see this value change because strstr would find the pattern at a different location.