
**Sign Bit**
In computer science, the sign bit is a bit in a signed number representation that indicates the {{sign of a number}}. Although only signed numeric data types have a sign bit, it is invariably located in {{the most significant bit position}}, so the term may be used interchangeably with "most significant bit" in some contexts.

Almost always, if the sign bit is 0, the number is {{non-negative (positive or zero)}}. If the sign bit is 1 then the number is negative. Formats other than two's complement integers allow a {{signed zero}}: distinct "positive zero" and "negative zero" representations, the latter of which does not correspond to the mathematical concept of a negative number.

When using a complement representation, to convert a signed number to a wider format the {{additional bits must be filled with copies of the sign bit}} in order to preserve its numerical value, a process called {{sign extension or sign propagation.}}


In computer numbers, the leftmost bit tells us if a number is positive or negative:
- If sign bit is 0: number is positive
- If sign bit is 1: number is negative

Example in 8 bits for simplicity:
```
 0111 1111 = 127  (positive, sign bit is 0)
 0000 0001 = 1    (positive, sign bit is 0)
 0000 0000 = 0    (positive, sign bit is 0)
 1000 0000 = -128 (negative, sign bit is 1)
 1111 1111 = -1   (negative, sign bit is 1)
```

**Why 0x80000000?**
```
0x80000000 = 1000 0000 0000 0000 0000 0000 0000 0000
```
This number has a 1 only in the sign bit position (31st bit). When we AND any number with this:
- If result is non-zero, the original number had a 1 in sign bit (was negative)
- If result is zero, the original number had a 0 in sign bit (was positive)

**Examples**
```
Positive number (0x70000000):
0111 0000 ... (rest are zeros)  [Original]
1000 0000 ... (rest are zeros)  [AND mask]
0000 0000 ... (rest are zeros)  [Result = 0, so positive]

Negative number (0x90000000):
1001 0000 ... (rest are zeros)  [Original]
1000 0000 ... (rest are zeros)  [AND mask]
1000 0000 ... (rest are zeros)  [Result ≠ 0, so negative]
```

This is how computers represent and work with positive and negative numbers in binary. The sign bit system is called "Two's Complement" and it's the standard way computers handle signed integers.


https://en.wikipedia.org/wiki/Sign_bit