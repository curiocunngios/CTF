---
aliases:
  - Function parameter
tags:
  - flashcard/active/ctf/C
---

```
   0x08048704 <+265>:   sub    esp,0x4
   0x08048707 <+268>:   push   DWORD PTR [ebp-0x90]
   0x0804870d <+274>:   push   0x40
   0x0804870f <+276>:   lea    eax,[ebp-0x4c]
   0x08048712 <+279>:   push   eax
   0x08048713 <+280>:   call   0x8048460 <fgets@plt>
```

here which one is the first, second and third argument of fgets? And why?


Let's analyze the arguments being pushed onto the stack for the fgets call:

Third argument (pushed first):  
`[ebp-0x90]` - This is the FILE* stream pointer

Second argument (pushed second):  
`0x40` (64 in decimal) - This is the size/length

First argument (pushed third):  
`[ebp-0x4c]` - This is the buffer destination pointer

Remember that in x86, arguments are pushed onto the stack in reverse order (right to left according to the C function prototype). The fgets prototype is:

`char *fgets(char *str, int size, FILE *stream)`

The stack pushes happen in reverse order because the first argument needs to be closest to the top of the stack when the function starts executing. So the pushing sequence is:
1. Push stream (rightmost arg)
2. Push size (middle arg) 
3. Push buffer ptr (leftmost arg)

When fgets executes, it will pop these off in the correct order to get the arguments as defined in the prototype.



This is due to the x86 calling convention being used - specifically the cdecl calling convention which is standard in C on x86 Linux/Unix systems.

The key reasons for using the stack instead of registers:

1. Function Parameter Count Flexibility
- Registers are limited (ebx, ecx, edx etc.)
- Stack can handle any number of parameters
- Different functions can have different numbers of parameters

2. Register Preservation
- The caller may already be using those registers for other purposes
- Would need complex register saving/restoring
- Stack provides clean separation between caller and callee

3. Standardization
- By having a standard convention of using the stack, any function can call any other function reliably
- Compiler knows exactly where to find parameters
- Makes linking between separately compiled code possible

The stack approach creates a new "stack frame" for each function call with its own clean parameter space, rather than trying to coordinate register usage between different functions.

When you see code like this using registers directly, it's often using a different calling convention like fastcall or specific assembly optimizations, but cdecl with stack parameters is the standard C calling convention on x86.