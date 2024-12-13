---
aliases:
  - ord
tags:
  - flashcard/active/ctf
---

# ord(\<char\>)
It {{convert character to ASCII or Unicode value}}. 'A' becomes 65
```python
# ASCII example
print(ord('A'))  # 65 (ASCII)
print(bin(ord('A')))  # '0b1000001' (7 bits)

# Unicode example
print(ord('π'))  # 960 (Unicode)
print(bin(ord('π')))  # '0b1111000000'

# How to check:
char = 'A'
if ord(char) <= 127:
    print("ASCII")
else:
    print("Unicode")
```
<!--SR:!2024-12-16,2,230-->
