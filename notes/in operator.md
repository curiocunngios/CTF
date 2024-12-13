---
aliases:
  - in Operator
tags:
  - flashcard/active/ctf
---

# `in` operator in python
`in` Operator in python checks {{if something is inside of something.}}
Examples:
```py
# String examples
text = "Hello World"
print("Hello" in text)      # True
print("hello" in text)      # False (case sensitive)
print("xyz" in text)        # False

# List examples
numbers = [1, 2, 3, 4, 5]
print(3 in numbers)         # True
print(6 in numbers)         # False

# Bytes examples (what we're using)
result = b"You win!\r\n"
print(b"win" in result)     # True
print(b"lose" in result)    # False

# Common uses
if "error" in response:
    print("Something went wrong")

if "success" not in message:
    print("Operation failed")
```
<!--SR:!2024-12-18,4,270-->