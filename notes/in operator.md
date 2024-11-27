---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - python
  - operator
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

`in` Operator in python ::: check if something is inside of something 

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