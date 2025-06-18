# Sign extension 

Sign extension (sometimes abbreviated as sext, particularly in mnemonics) is the operation, in computer arithmetic, of {{increasing the number of bits}} of a binary number while {{preserving the number's sign (positive/negative) and value}}. This is done by {{appending digits to the most significant side of the number}}, following a procedure {{dependent on the particular signed number representation used}}. In x86_64 architecture it is {{Two's Complement}} and the assembly cdqe instruction is specifically for {{Two's Complement sign extension.}}

For example, if six bits are used to represent the number "00 1010" (decimal positive 10) and the sign extends operation increases the word length to 16 bits, then the new representation is simply "0000 0000 0000 1010". Thus, both the value and the fact that the value was positive are maintained.

If ten bits are used to represent the value "11 1111 0001" (decimal negative 15) using two's complement, and this is sign extended to 16 bits, the new representation is "1111 1111 1111 0001". Thus, by padding the left side with ones, the negative sign and the value of the original number are maintained.
```
1111 1111 1111 0001 - 1 = 1111 1111 1111 0000(sub 1)
0000 0000 0000 1111 = -15 (flipping)
```

In the Intel x86 instruction set, for example, there are two ways of doing sign extension:

    using the instructions cbw, cwd, cwde, and cdq: convert the byte to word, word to doubleword, word to extended doubleword, and doubleword to quadword, respectively (in the x86 context a byte has 8 bits, a word 16 bits, a doubleword and extended doubleword 32 bits, and a quadword 64 bits);
    using one of the sign extended moves, accomplished by the movsx ("move with sign extension") family of instructions.

https://en.wikipedia.org/wiki/Sign_extension


## In Two's complement 
0xFFFFFFFF00000000 in binary is:
```apache
1111 1111 1111 1111 1111 1111 1111 1111 0000 0000 0000 0000 0000 0000 0000 0000 (64 bits)
```
So when we extend a negative 32-bit number (sign bit = 1) to 64 bits, we {{fill the upper 32 bits with {{`1`s}}:
```apache
Before: 1xxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx (32-bit negative number)
After:  1111 1111 1111 1111 1111 1111 1111 1111 1xxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx (64-bit)

Before: 0xxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx (32-bit positive number)
After:  0000 0000 0000 0000 0000 0000 0000 0000 0xxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx (64-bit)
```

Example python code 
```
def sign_extend_32_to_64(value):
    if value & 0x80000000:
        return value | 0xFFFFFFFF00000000
    return value & 0xFFFFFFFF
```
If the 31st bit (sign bit) is 1, {{extend with 1s}}, else extend with 0s
`0x80000000` {{acts as a mask}} to check what the sign bit is:
```basic
Positive number (0x70000000):
0111 0000 ... (rest are zeros)  [Original]
1000 0000 ... (rest are zeros)  [AND mask]
0000 0000 ... (rest are zeros)  [Result = 0, so positive]

Negative number (0x90000000):
1001 0000 ... (rest are zeros)  [Original]
1000 0000 ... (rest are zeros)  [AND mask]
1000 0000 ... (rest are zeros)  [Result ≠ 0, so negative]
```

Assembly example:
```as
mov    eax,DWORD PTR [rbp-0x4]  # Load 32-bit value from memory
sub    eax,0x2                  # Subtract 2
cdqe                           # Sign extend to 64 bits
```

### How does 0 fillings work 
```
64-bit value before:
0000 0000 0000 0000 0000 0000 0000 0101  (unknown upper bits)

0xFFFFFFFF in 64 bits is:
0000 0000 0000 0000 1111 1111 1111 1111

When we do AND (&):
???? ???? ???? ???? 0000 0000 0000 0101  (original)
0000 0000 0000 0000 1111 1111 1111 1111  (mask)
----------------------------------------
0000 0000 0000 0000 0000 0000 0000 0101  (result)
```
The key is that 0xFFFFFFFF in a 64-bit context is {{automatically zero-extended:}}
```
0xFFFFFFFF = 0x00000000FFFFFFFF

So when we write:
value & 0xFFFFFFFF

It's actually:
value & 0x00000000FFFFFFFF
```


### Zero-extensions
2. `byte_value & 0xFF`:
```python
# Let's see it bit by bit:
# 0xFF in binary:        0000 0000 0000 0000 0000 0000 1111 1111
# Some value:            xxxx xxxx xxxx xxxx xxxx xxxx 1010 1100
# After AND (&):         0000 0000 0000 0000 0000 0000 1010 1100

# Example with negative byte:
value = -50  # in binary representation larger than 8 bits
print(bin(value))  # might show many bits
# After masking:
unsigned_byte = value & 0xFF  # keeps only lowest 8 bits
print(bin(unsigned_byte))     # only 8 bits remain

# Concrete example:
value = -50
print(f"Original: {bin(value)}")
# Might show: -0b110010
masked = value & 0xFF
print(f"Masked:   {bin(masked)}")
# Shows: 0b11001110 (206 in decimal)
```

The `& 0xFF` operation:
1. 0xFF is 8 ones in binary (11111111)
2. AND operation keeps only the rightmost 8 bits
3. All bits beyond 8th position become 0
4. Result is always 0-255, which is unsigned byte range

This ensures unsigned interpretation because:
- Removes any sign bits
- Limits value to 8 bits
- Forces value into 0-255 range




