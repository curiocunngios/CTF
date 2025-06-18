# hexdump 
 In computing, a hex dump is a textual {{hexadecimal view}} of (often, but not necessarily binary) {{computer data}}, from memory or from a computer file or storage device. Looking at a hex dump of data is usually done in the context of either debugging, reverse engineering or digital forensics. Interactive editors that provide a similar view but also manipulating the data in question are called hex editors.

In a hex dump, each byte (8 bits) is {{represented as a two-digit hexadecimal number}}. Hex dumps are commonly {{organized into rows of 8 or 16 bytes}}, sometimes separated by whitespaces. Some hex dumps have the hexadecimal memory address at the beginning.

Some common names for this program function are hexdump, hd, od, xxd and simply dump or even D. 

## Example hexdump in xxd
```xxd
00002000: 0100 0200 2535 6300 2538 6300 3a29 003a  ....%5c.%8c.:).:
```
which all the above characters are within the 8-bits unsinged integer range and presentable by {{ASCII}}
. means {{non-printable character}}, which includes:
- `0x01` at raw address `0x2000`, {{Start of Heading (SOH) - control character}}
- `0x00` at raw address `0x2001`, {{null terminator}}
- `0x02`at raw address `0x2002`,  {{Start of Text (STX) - control character}}
- `0x00` at raw address `0x2003`, {{null terminator}}
- `0x25 0x35 0x63 0x00` at raw address `0x2004`, {{%5c., scanf arguments. Which would be stored in rdi/rsi/etc. and passed into function scanf when it is called}}
In the above case, 0100 0200 just happened to be {{version number}}
```
01 00 = Major version (1)
02 00 = Minor version (2)
```

## Similar inspection in pwndbg
```
pwndbg> x/s 0x555555556004
0x555555556004: "%5c"
```
We can see that at the runtime address `0x555555556004` found in `DISAS` of `main` function also shows the 1st scanf argument `%5c` in this example
Original assembly
```as
lea    rax,[rip+0x2ed0]        # 4028 <input.0>                          
mov    rsi,rax              # <input.0> (unintialized in .bss segment) goes into rsi
lea    rax,[rip+0xea2]        # 2004 <_IO_stdin_used+0x4> %5c receives 5 character
mov    rdi,rax
```
so it's something like {{scanf(%5c, x)}}