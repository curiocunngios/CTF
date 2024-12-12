---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - protection
  - binary exploitation
  - binary 
  - memory
tags:
  - flashcard/active/ctf/hi
  - function/index
  - language/in/English
---

Stack Canary ::: a security mechanism to detect buffer overflows <!--SR:!2024-12-12,1,230!2024-12-15,4,270-->

## How does Stack Canary prevents buffer overflow  
?

- Random value placed between buffer and return address
- Value checked before function returns
- If changed, program terminates

## Visualization of canary
```
Memory layout:
[buffer]
[canary]     <- Random value
[saved rbp]
[ret addr]
```

Stack canary random values usually starts with {{null-byte `0x00`}}. It is random {{per program execution}} and is stored in a [protection region](<fsgs segment register.md>), specifically at {{fs:0x28 on x86_64 Linux.}} <!--SR:!2024-12-15,4,270!2024-12-12,1,230!2024-12-14,3,250-->

## The canary operations in assembly instructions

```as
; Setting up canary
mov    rax, QWORD PTR fs:0x28    ; Get canary from fs:0x28
mov    QWORD PTR [rbp-0x8], rax  ; Store on stack

; Checking canary
mov    rax, QWORD PTR [rbp-0x8]  ; Get canary from stack
xor    rax, QWORD PTR fs:0x28    ; Compare with original
je     .L2                       ; If equal, continue
call   __stack_chk_fail@plt      ; If not, terminate
```

## How was canary initialized  
? 
- OS/loader initializes the canary value during program startup
- Stores it in thread-local storage (accessed via fs:0x28)
- Functions then copy this value from fs:0x28 to their stack frame


Creation of canary  
?
```json
Program Start:
[OS/loader] --> [sets canary in fs:0x28]

Function Entry:
[copy from fs:0x28] --> [stack frame]

Function Exit:
[compare stack value with fs:0x28]
```