---
aliases:
  - pwndbg command
  - gdb command
tags:
  - flashcard/active/ctf
---


# pwndbg Commands

## Memory and Registers
Format for {{examining memory}} (`x` command) :: `x/<n><s><f> <address>` <!--SR:!2024-12-17,3,250-->
- n = number of units
- s = size {{(b=1, h=2, w=4, g=8 bytes)}}
- f = format {{(x=hex, u=unsigned, d=decimal, s=string, i=instruction)}} <!--SR:!2024-12-17,3,250!2024-12-17,3,250-->

view register information :: `info register` <!--SR:!2024-12-17,3,250-->

### More of x command
instructions have different lengths and x command {{shows chunks with fixed length}}. Therefore, not all instructions after one can be shown using x command
```
0x40113a:    48 83 ec 40          sub    rsp, 0x40              # 4 bytes
0x40113e:    48 8d 05 bf 0e 00 00 lea    rax, [rip + 0xebf]    # 7 bytes
0x401145:    48 89 c7             mov    rdi, rax               # 3 bytes
0x401148:    b8 00 00 00 00       mov    eax, 0                 # 5 bytes
```
<!--SR:!2024-12-17,3,250-->

### break <location (memory addr, func name, etc.)>
create a {{breakpoint}} {{which the program would stop there during runtime}} <!--SR:!2024-12-17,3,250!2024-12-17,3,250-->

Command to list all breakpoints :: `info breakpoint` or `bl` <!--SR:!2024-12-17,3,250-->

delete breakpoints :: `delete <breakpoint_number>` or just `delete` to remove all <!--SR:!2024-12-17,3,250-->

### Navigation
Difference between `ni` and `si`:
??
- `ni`: Next instruction, executes function calls at full speed
- `si`: Step into instruction, follows into function calls <!--SR:!2024-12-17,3,250-->

continue execution :: `continue` or `c` <!--SR:!2024-12-17,3,250-->

## Stack Operations
Command to show stack frame info :: `backtrace` <!--SR:!2024-12-16,2,230-->

navigate stack frames:
??
- `up`: Move to newer frames
- `down`: Move to older frames <!--SR:!2024-12-17,3,250--> 

## Advanced Features
Command to check binary security options :: `checksec` <!--SR:!2024-12-16,2,230-->

view memory mapping :: `vmmap` <!--SR:!2024-12-18,4,270-->

Command to show stack data with custom count/offset :: `stack <count> <offset>` (e.g., `stack 30 3`) <!--SR:!2024-12-26,12,270-->

enable instruction recording :: `record` <!--SR:!2024-12-17,3,250-->
- Enables reverse debugging commands:
- `rsi` (reverse step into)
- `rni` (reverse next instruction)