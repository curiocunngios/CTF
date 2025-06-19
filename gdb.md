# Setting breakpoints:

```py
s = '''

set $mybase = (unsigned long)&challenge - 0x1a64
b * $mybase + 0x01db6 
b * challenge
b * challenge+1354

'''

# 0x01db6 is the offset found in ghidra
```
