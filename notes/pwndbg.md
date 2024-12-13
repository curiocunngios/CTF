---
aliases:
  - pwndbg command
  - gdb command
tags:
  - flashcard/active/ctf
---


# pwndbg Commands

## Basic Commands
pwndbg :: A GDB plug-in that enhances debugging experience, particularly for low-level software development, hardware hacking, and exploit development. 

find text in manual using regex :: `apropos <regex>` (e.g., `apropos register`) 

## Loading and Running
Command to load a binary into gdb :: `file <filename>` (e.g., `file ./a.out`) 

run the loaded binary :: `run` or `r` 

## Breakpoints
set a breakpoint at an address:
??
- `break * <address>` (e.g., `b * 0x5555555551ee`)
- `break * <func name> + offset` (e.g., `b * getflag + 10`) 

Command to list all breakpoints :: `info breakpoint` or `bl` 

delete breakpoints :: `delete <breakpoint_number>` or just `delete` to remove all 

## Memory and Registers
Format for examining memory (`x` command) :: `x/<n><s><f> <address>` 
- n = number of units
- s = size (b=1, h=2, w=4, g=8 bytes)
- f = format (x=hex, u=unsigned, d=decimal, s=string, i=instruction)

view register information :: `info register` 

## Navigation
Difference between `ni` and `si`:
??
- `ni`: Next instruction, executes function calls at full speed
- `si`: Step into instruction, follows into function calls 

continue execution :: `continue` or `c` 

## Stack Operations
Command to show stack frame info :: `backtrace` 

navigate stack frames:
??
- `up`: Move to newer frames
- `down`: Move to older frames 

## Advanced Features
Command to check binary security options :: `checksec` 

view memory mapping :: `vmmap` 

Command to show stack data with custom count/offset :: `stack <count> <offset>` (e.g., `stack 30 3`) 

enable instruction recording :: `record` 
- Enables reverse debugging commands:
- `rsi` (reverse step into)
- `rni` (reverse next instruction)