---
aliases:
  - pwndbg information presentation
tags:
  - flashcard/active/ctf
---

#### LEGEND section
```
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
```
- STACK :: memory region for function calls which for examples stores {{function arguments, address of the instruction after function return, local variables, etc.}} and local variables in general <!--SR:!2024-12-17,3,250-->
- HEAP :: Memory region for dynamically allocated stuff <!--SR:!2024-12-17,3,248-->
- CODE :: memory that stores the executable codes <!--SR:!2024-12-17,3,237-->
- WX :: Writable and executable memory <!--SR:!2024-12-17,3,248-->
- RODATA :: Read only data <!--SR:!2024-12-17,3,248-->

#### Register section
It shows the {{current state of registers}}
```
RBX  0x7fffffffdd28 —▸ 0x7fffffffe0c8 ◂— '/home/kali/Desktop/> vuln_no_protection'
```
- `—▸` points from a {{register or memory address}} to the {{memory address}} it contains. This is a {{dereference}} showing the next level of indirection. (?)
- `◂—` indicates the {{value}} stored at the {{memory address}} on the left.
- RBX holds the value `0x7fffffffdd28` which is a {{memory address}}
- `0x7fffffffdd28` contains another {{memory address 0x7fffffffe0c8}}
- `0x7fffffffe0c8` contains {{a string '/home/kali/Desktop/vuln_no_protection'}} <!--SR:!2024-12-17,3,237!2024-12-17,3,237!2024-12-17,3,237!2024-12-17,3,237!2024-12-17,3,237!2024-12-17,3,237!2024-12-17,3,237!2024-12-17,3,237!2024-12-17,3,237-->

Example:
```
RCX 0x403e00 (__do_global_dtors_aux_fini_array_entry) —▸ 0x401100 (__do_global_dtors_aux) ◂— endbr64
```
- `0x403e00` is associated with {{the destructors for global variables}} designed to destroy the global objects when the {{program exits}}
- `endbr64` {{prevents program to start at beginning}} but not jumping to middle <!--SR:!2024-12-17,3,248!2024-12-17,3,248!2024-12-17,3,248-->


#### DISASM section
- asssembly code {{in the middle}}
- memory address and offset from the function start of each instructions inside a function {{on left hand side}}
```as
0x401156 <vulnerable_function+32>
│        │                    │
│        │                    └─ Offset from function start (in bytes)   |
│        └─ Function name
└─ Absolute address of the instruction in memory
```
<!--SR:!2024-12-17,3,248!2024-12-17,3,248-->

#### STACK section 

```
00:0000│ rbp rsp 0x7fffffffdc00 —▸ 0x7fffffffdc10 ◂— 1
01:0008│+008     0x7fffffffdc08 —▸ 0x401199 (main+14) ◂— mov eax, 0
02:0010│+010     0x7fffffffdc10 ◂— 1
03:0018│+018     0x7fffffffdc18 —▸ 0x7ffff7ddbd68 (__libc_start_call_main+120)
```
both RBP and RSP pointing to {{0x7fffffffdc00}}
```
XX:YYYY│+ZZZ     Address      —▸ Content/Reference
│       │         │            │
│       │         │            └─ What's stored at this address
│       │         └─ Actual memory address
│       └─ Offset from stack top in hex
└─ Stack slot number
```
<!--SR:!2024-12-17,3,237-->

#### BACKTRACE section
```
► 0         0x40113a vulnerable_function+4    # Current function
  1         0x401199 main+14                  # Called from main
  2   0x7ffff7ddbd68 __libc_start_call_main+120  # libc startup
  3   0x7ffff7ddbe25 __libc_start_main+133
  4         0x401071 _start+33
```
- Top entry (►) is {{current function}}
- Each subsequent entry shows {{where the function above was called from}}
- Reading bottom-up shows program execution flow:
```
    _start (program entry)
    __libc_start_main (C runtime setup)
    main
    vulnerable_function (current)
```
<!--SR:!2024-12-17,3,248!2024-12-17,3,248-->