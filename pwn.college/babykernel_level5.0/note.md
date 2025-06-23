---
aliases:
  - typical functions of C
tags:
  - flashcard/active/ctf/kerC
---

Let me break down `(void (*)(void))0xffffffffc00008ed` piece by piece:

## The Cast: `(void (*)(void))`

This is a **type cast** that tells the compiler to treat the following value as a specific type of function pointer.

**Breaking down the function pointer type:**
- `void` (first one) = **return type** - the function returns nothing
- `(*)` = **pointer indicator** - this is a pointer to a function
- `(void)` (second one) = **parameter list** - the function takes no parameters

So `void (*)(void)` means: {{"a pointer to a function that takes no parameters and returns void"}}


## What the entire expression does:
```c
(void (*)(void))0xffffffffc00008ed
```
This takes the raw integer `0xffffffffc00008ed` and **casts it** to a {{function pointer type}}. It's essentially saying:
*"Treat this memory address as if it points to a function that takes no parameters and returns void"*

## Example usage:

```c
// Create a function pointer and assign the casted address
void (*win)(void) = (void (*)(void))0xffffffffc00008ed;

// Now you can call it like a regular function
win();  // This jumps execution to address 0xffffffffc00008ed
```
