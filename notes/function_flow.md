aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - pwndbg
  - assembly 
  - registers
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

# Example of `main` function in C
```
   0x000000000040118b <+0>:     push   rbp
   0x000000000040118c <+1>:     mov    rbp,rsp
   0x000000000040118f <+4>:     mov    eax,0x0
   0x0000000000401194 <+9>:     call   0x401136 <vulnerable_function>
   0x0000000000401199 <+14>:    mov    eax,0x0
   0x000000000040119e <+19>:    pop    rbp
   0x000000000040119f <+20>:    ret
```
## The assembly 
```
# Function Prologue
0x40118b: push   rbp        # Save old base pointer on stack
0x40118c: mov    rbp,rsp    # Set up new base pointer for this frame

# Function Body
0x40118f: mov    eax,0x0    # Zero out eax before function call
0x401194: call   0x401136   # Call vulnerable_function
0x401199: mov    eax,0x0    # Set return value to 0 (return 0)

# Function Epilogue
0x40119e: pop    rbp        # Restore old base pointer
0x40119f: ret              # Return to caller
```

## The stack operation

```
Before prologue:
        [old return addr]  <- RSP
        [......]

After push rbp:
        [old return addr]
        [old rbp]         <- RSP
        [......]

After mov rbp,rsp:
        [old return addr]
        [old rbp]         <- RBP, RSP
        [......]

During vulnerable_function call:
        [old return addr]
        [old rbp]         <- RBP
        [return to 0x401199]  # Return address to main+14
        [...vulnerable_function's stack frame...]

After epilogue:
        [old return addr]  <- RSP
        [......]
```

## Before `main` starts

```
High address
        [return to _start]     <- RSP points here
        [...other data...]
Low address
```
## After `push` rbp

```
High address
        [return to _start]
        [{{old rbp value}}]        <- {{RSP points here}} 
        [...other data...]
Low address
```

intention:
- {{save the RBP value}} to perhaps use it later so we push it on top of the frame
- keep track of {{where each functions's  stack frame begins}}



