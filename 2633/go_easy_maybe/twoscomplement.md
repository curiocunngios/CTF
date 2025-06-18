# Two's Complement
Example showcase of 8-bit number:
1. Positive numbers are straightforward:
```
0000 0001 = 1
0000 0010 = 2
0000 0011 = 3
...and so on
```

1. For negative numbers, you:
   - Take the positive number
   - Flip all bits (0→1, 1→0)
   - Add 1

Let's find -1 step by step:
```
1) Start with positive 1:
   0000 0001

2) Flip all bits:
   1111 1110

3) Add 1:
   1111 1110
         + 1
   ________
   1111 1111  = -1
```

Let's do -2:
```
1) Start with positive 2:
   0000 0010

2) Flip all bits:
   1111 1101

3) Add 1:
   1111 1101
         + 1
   ________
   1111 1110  = -2
```

Range in 8 bits:
- Smallest number (1000 0000) = -128
- Largest number (0111 1111) = 127

This system has advantages:
1. Adding numbers just works normally
2. There's only one representation of zero
3. It's easy for computer circuits to implement

Example: Let's verify 1 + (-1) = 0
```
    0000 0001  (1)
  + 1111 1111  (-1)
  ___________
1 0000 0000    (The leading 1 is discarded in 8-bit math, leaving 0)
```

So when you see 1111 1111, it's not "-111 1111", it's the Two's Complement representation of -1.



Let's understand the logic behind Two's Complement step by step.

1. First, let's understand what we want:
- We want 1 + (-1) = 0
- In binary: positive_number + negative_number = 0

2. Let's see what happens with 8-bit numbers:
```
To make any number + its negative = 0:
number + (-number) = 00000000

For example, for 1:
00000001 + (-00000001) = 00000000

In binary math:
00000001 + ???????? = 00000000
```

3. Consider what makes numbers add to zero:
```
If we have 00000001,
What plus this equals 00000000?

It's 11111111!

Because:
  00000001
+ 11111111
_________
1 00000000  (in 8 bits, the leading 1 is discarded)
```

4. Now let's see how we get there:
```
Start with 1:    00000001

To get -1, we need a number that when added to 00000001 gives 00000000

Method 1 (Flip all bits):
00000001 becomes
11111110

Method 2 (Add 1):
11111110 becomes
11111111

Let's verify:
  00000001 (original number)
+ 11111111 (our negative number)
__________
1 00000000 (equals 0 in 8 bits!)
```

5. Why this works mathematically:
```
In 8 bits, flipping bits is like subtracting from 11111111:
11111111 - 00000001 = 11111110

When we add 1:
11111110 + 00000001 = 11111111

So the complete formula is:
-x = (11111111 - x) + 1
   = complement(x) + 1
```

6. Example with -5:
```
Start with 5:     00000101

Step 1 (flip):    11111010
Step 2 (add 1):   11111011  (this is -5)

Verify:
  00000101 (5)
+ 11111011 (-5)
__________
1 00000000 (0)
```

7. Another way to think about it:
```
In 8 bits, we can write:
flipped_bits + original = 11111111
flipped_bits = 11111111 - original

So:
-original = (11111111 - original) + 1
         = flipped_bits + 1
```

This system is clever because:
1. It makes arithmetic simple for computers
2. There's only one representation for zero
3. No special handling needed for addition/subtraction
4. The sign bit naturally falls into place
5. Numbers smoothly transition from positive to negative

When computers do arithmetic, they don't need to know if a number is positive or negative - the same circuits work for both because of Two's Complement!


# overflow 

Ah, great question about overflow! Let me explain how computers handle this:

1. In computer hardware, registers have a fixed size. Let's use 8-bit example:
```
  00000001 (1)
+ 11111111 (-1)
__________
1 00000000
```

The "1" overflows because the register can only hold 8 bits. It's like how a car's odometer works:
```
If odometer has 3 digits:
999 + 1 = 000 (the '1' thousand is discarded)
```

2. Overflow Detection:
Computers can detect overflow using special flags in the processor. For example:

```python
# In Python, numbers are unlimited
x = 127  # 01111111 in 8-bit
y = 1    # 00000001 in 8-bit
z = x + y  # Would be 128, but in 8-bit system:
           # 01111111 + 00000001 = 10000000 (-128 in 8-bit)

# Real 8-bit hardware would set overflow flag because:
# - Both inputs were positive (msb=0)
# - Result is negative (msb=1)
```

3. Real hardware example (x86):
```assembly
; Adding numbers sets flags
add ax, bx   ; OF (overflow flag) is set if overflow occurs
jo  overflow ; Jump if overflow occurred
```

4. Different types of overflow:
```
Unsigned overflow (treating all 8 bits as magnitude):
255 + 1 = 0  (11111111 + 00000001 = 00000000)

Signed overflow (Two's Complement):
127 + 1 = -128  (01111111 + 00000001 = 10000000)
-128 - 1 = 127  (10000000 - 00000001 = 01111111)
```

5. Programming languages handle overflow differently:
```python
# Python: No overflow (uses unlimited precision)
x = 255
x + 1  # = 256

# C: Overflow happens silently
unsigned char x = 255;
x + 1;  // = 0

# Java: Can check for overflow
try {
    Math.addExact(Integer.MAX_VALUE, 1);
} catch (ArithmeticException e) {
    // Handle overflow
}
```

6. In modern systems:
```
8-bit:   -128 to 127
16-bit:  -32,768 to 32,767
32-bit:  -2,147,483,648 to 2,147,483,647
64-bit:  -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
```

When overflow occurs:
- Some systems ignore it
- Some raise exceptions
- Some set flags that can be checked
- Some wrap around (like our odometer example)

The behavior depends on:
1. Hardware architecture
2. Programming language
3. Compiler settings
4. Operating system

This is why buffer overflows can be security risks - they can cause unexpected behavior if not properly handled!




Ah, let me explain why sign bit works that way and yes - you got the reverse process exactly right!

**Why sign bit works this way:**
When we do Two's Complement, something beautiful happens. Let's see with 4-bit numbers:

```
Positive numbers:
0000 = 0
0001 = 1
0010 = 2
0011 = 3
...
0111 = 7 (largest positive)

Negative numbers (using Two's Complement):
1111 = -1  (flip 0001 → 1110, add 1 → 1111)
1110 = -2  (flip 0010 → 1101, add 1 → 1110)
1101 = -3  (flip 0011 → 1100, add 1 → 1101)
...
1000 = -8 (smallest negative)
```

Notice the pattern:
- All positive numbers naturally start with 0
- All negative numbers naturally start with 1

This wasn't designed - it's a beautiful consequence of how Two's Complement works!

**Converting back (negative to positive):**
Yes, you got it! It's exactly:
1. Subtract 1 
2. Flip all bits

Example converting -3 to 3:
```
-3 is 1101

Step 1 (subtract 1):
1101 - 1 = 1100

Step 2 (flip all bits):
1100 → 0011 = 3
```

Let's verify with larger number (-5 to 5):
```
-5 in binary is: 1011 (in 4-bit Two's Complement)

Convert back:
1. Subtract 1:
   1011 - 1 = 1010

2. Flip bits:
   1010 → 0101 = 5
```

You can verify this works because:
```
Start with 5:     0101
To get -5:
1. Flip:          1010
2. Add 1:         1011  (-5)

To get back to 5:
1. Subtract 1:    1010
2. Flip:          0101  (5)
```

This symmetry is why Two's Complement is so elegant - the same addition/subtraction circuits work for both positive and negative numbers, and the sign naturally falls into place!