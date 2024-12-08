---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - programming
tags:
  - flashcard/active/ctf/testing/temp
  - function/index
  - language/in/English
---


ord(<char>) ::: convert character to ASCII or Unicode value. 'A' becomes 65 <!--SR:!2024-12-09,1,230!2000-01-01,1,250-->

When does it print ASCII and when does it print Unicode?
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
