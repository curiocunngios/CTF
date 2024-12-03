aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - pwndbg
  - assembly 
  - buffer overflow
  - pwn
  - command
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

# x command 

{{Examine memory}} in format <format> starting at
address <address> 

x/[number][format] <address>

number: how many units to display
format:
- x = {{hex}} (default)
- d = {{decimal}}
- s = {{string}}
- i = {{instruction}}
- c = {{character}}

## If you enter "AAA"
pwndbg> x/s $rsp          # {{Print as string: "AAA"}}  
pwndbg> x/3x $rsp         # {{Print 3 hex bytes: 0x41 0x41   0x41}}  
pwndbg> x/3c $rsp         # {{Print 3 chars: 'A' 'A' 'A'}}  
pwndbg> x/1wx $rsp        # {{Print one word (4 bytes) in hex:0x00414141}}  


# break <location (memory addr, func name, etc.)>
create a {{breakpoint}} {{which the program would stop there during runtime}}

