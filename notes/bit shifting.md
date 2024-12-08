---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
tags:
  - flashcard/active/ctf/
  - function/index
  - language/in/English
---

# Bit shift

The bit shift are {{sometimes considered bitwise operations}}, because they treat a value as a {{series of bits}} rather than as a numerical quantity. In these operations, the digits are {{moved, or shifted, to the left or right}}. 

Registers in a computer processor have a fixed width, so some bits will be "shifted out" of the register at one end, while the same number of bits are "shifted in" from the other end; the differences between bit shift operators lie in how they determine the values of the shifted-in bits. 

## In python 
`<<` ::: left shift
```py
num = 65  # 'A'
print(bin(num))     # '0b1000001'
print(bin(num << 8))# '0b100000100000000'

# 65 in binary:        0000 0000 0100 0001
# After << 8:          0100 0001 0000 0000
# = 65 * 2^8 = 65 * 256 = 16640


x = 65  # 'A'
print(bin(x)[2:].zfill(16))          # 0000000001000001
print(bin(x << 1)[2:].zfill(16))     # 0000000010000010
print(bin(x << 2)[2:].zfill(16))     # 0000000100000100
print(bin(x << 8)[2:].zfill(16))     # 0100000100000000

# Better visualization of shifting:
# Original: 0000 0000 0100 0001
# << 1:     0000 0000 1000 0010
# << 2:     0000 0001 0000 0100
# << 8:     0100 0001 0000 0000


x = 65  # 'A'
print(f"Original:    {bin(x)[2:]}         ({len(bin(x)[2:])} bits)")          # 1000001
print(f"<< 1:        {bin(x << 1)[2:]}    ({len(bin(x << 1)[2:])} bits)")    # 10000010
print(f"<< 2:        {bin(x << 2)[2:]}    ({len(bin(x << 2)[2:])} bits)")    # 100000100
print(f"<< 8:        {bin(x << 8)[2:]}    ({len(bin(x << 8)[2:])} bits)")    # 100000100000000

# Output:
# Original:    1000001     (7 bits)
# << 1:        10000010    (8 bits)
# << 2:        100000100   (9 bits)
# << 8:        100000100000000  (15 bits)
```

The number of bits actually grows as needed to represent the larger number. This is because:

- Each left shift effectively multiplies the number by 2
- Larger numbers need more bits to represent them
- Python integers can grow to any size needed


`>>` ::: right shift
```py
x = 65
print(bin(x)[2:].zfill(8))       # 01000001
print(bin(x >> 1)[2:].zfill(8))  # 00100000  (each bit moved right 1 position)
print(bin(x >> 2)[2:].zfill(8))  # 00010000  (each bit moved right 2 positions)

# Visually:
# Original:   0100 0001
# >> 1:       0010 0000
# >> 2:       0001 0000
```
