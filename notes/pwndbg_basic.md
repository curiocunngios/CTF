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
- shows the current state of registers

> RBX  0x7fffffffdd28 `—▸` 0x7fffffffe0c8 `◂—` '/home/kali/Desktop/> vuln_no_protection' :::
>
> RBX holds the value 0x7fffffffdd28 which is a {{memory address}}
>
> 0x7fffffffdd28 contains another {{memory address 0x7fffffffe0c8}}
>
> 0x7fffffffe0c8 contains {{a string '/home/kali/Desktop/vuln_no_protection'}}


> `—▸` (right arrow) ::: Points from a {{register or memory address}} to the {{memory address}} it contains. This is a {{dereference}} showing the next level of indirection. (?)  
> `◂—` (left arrow) ::: Indicates the {{value}} stored at the {{memory address}} on the left.


> RCX 0x403e00 (__do_global_dtors_aux_fini_array_entry) `—▸` 0x401100 (__do_global_dtors_aux) `◂—` endbr64 ::: 

in above example, 0x403e00 is associated with {{the destructors for global variables}} designed to destroy the global objects when the {{program exits}}

endbr64 ::: is ssome sort of markers (CET) for valid control flow to prevent control flow attacks like ROP (return oriented programming)


# DISASM section

::: 

- asssembly code in the middle 

- memory address and offset from the function start of each instructions inside a function on LHS

0x401156 <vulnerable_function+32>
│        │                    │
│        │                    └─ Offset from function start (in bytes)   |
│        └─ Function name
└─ Absolute address of the instruction in memory

```
0x401136: function start
0x401156: this instruction
0x401156 - 0x401136 = 32 (0x20) bytes
```


- prevent exactly what has happened to the registers on RHS

```
RAX => 0x402004 ◂— 'Enter input: '
RDI => 0x402004 ◂— 'Enter input: '
EAX => 0
RAX => 0x402012 ◂— 0x6520756f59007325 /* '%s' */

```