---
aliases:
  - python byte operation
  - python byte 
tags:
  - flashcard/active/ctf
---
# Byte data type
byte type can be imagined as in each character is a {{sequence of 0 and 1}} ranged from {{0 - 255}} which is the {{8-bit unsigned integer}} range. 

Each character are stored as {{its ASCII value.}}
Example:
```py
>>> byte = b'hello'
>>> print(byte)
b'hello'
>>> print(list(byte))
[104, 101, 108, 108, 111]

# b'A' is the same as b'\x41' (because 65 in hexadecimal is 41)
print(b'A' == b'\x41')  # Output: True
```


## Declaration of byte type 
`byte = b'hello'` is equivalent to :: `byte_2 = b"hello"` 


