aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - pwndbg
  - assembly 
  - buffer overflow
  - pwn
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

# LEGEND section
```
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
```

STACK ::: memory region for function calls which for examples stores {{function arguments, address of the instruction after function return, local variables, etc.}} and local variables in general

HEAP ::: Memory region for dynamically allocated stuff

CODE ::: memory that stores the executable codes 

WX ::: Writable and executable memory 

RODATA ::: Read only data

# Register section :::
shows the current state of registers

RBX  0x7fffffffdd28 —▸ 0x7fffffffe0c8 ◂— '/home/kali/Desktop/vuln_no_protection' :::

RBX holds the value 0x7fffffffdd28 which is a {{memory address}}

0x7fffffffdd28 contains another {{memory address 0x7fffffffe0c8}}

0x7fffffffe0c8 contains {{a string '/home/kali/Desktop/vuln_no_protection'}}


—▸ (right arrow)::: Points from a {{register or memory address}} to the {{memory address}} it contains. This is a {{dereference}} showing the next level of indirection. (?)
◂— (left arrow):::: Indicates the {{value}} stored at the {{memory address}} on the left.