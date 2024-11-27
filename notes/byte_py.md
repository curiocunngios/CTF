---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - python 
  - byte
  - bit
  - data type
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

```py

# both of the below are the same
byte = b'hello'  

byte_2 = b"hello"

# imagine each character as a sequence of 0 and 1, that's the byte type

# each character are integers ranged from 0 - 255, the 8-bit unsigned integer range

# A bytes object representing ASCII characters
byte_str = b"hello"

# Each character is stored as its ASCII value
print(byte_str)        # Output: b'hello'
print(list(byte_str))  # Output: [104, 101, 108, 108, 111]


# b'A' is the same as b'\x41' (because 65 in hexadecimal is 41)
print(b'A' == b'\x41')  # Output: True
```

