---
aliases:
  - function prologue
  - Start of stack frame
tags:
  - flashcard/active/ctf/yo
  - function/index
  - language/in/English
---


# Function Prologue  
??  
```
0x40118b: push   rbp        # Save old base pointer on stack
0x40118c: mov    rbp,rsp    # Set up new base pointer for this frame
```

## The stack operation
How does stack looks like from before prologue to after prologue  
??  
```
Before prologue:
        [old rbp]
        [......] (other data e.g. cosmetic point arguments)
        [old return addr]  <- RSP (call <addr> pushes rip here)
        [......]

After push rbp:
        [old return addr]
        [old rbp]         <- RSP
        [......]

After mov rbp,rsp:
        [old return addr]
        [old rbp]         <- RBP, RSP
        [......]
```

- RBP value is saved below the return address to be {{restored later when go back to the function call location}}




