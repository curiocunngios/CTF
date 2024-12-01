---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - reverse engineering 
  - memory
  - memory address 
  - pwn
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

## Memory address example
```
0x7fff ffff dbc0

Reading from left to right:
7    = 0111  First nibble (4 bits)
f    = 1111
f    = 1111
f    = 1111
f    = 1111
f    = 1111
f    = 1111
d    = 1101
b    = 1011
c    = 1100
0    = 0000
```
This is a memory address in a {{64-bit system}}:

    Starting with 0x7f: In Linux x86_64, user space addresses typically start with 0x7f
    Many f's: Indicates this is in the {{higher end}} of virtual memory
    Last 12 bits (bc0): Specific {{offset}} within a page

## Memory layout (typical 64-bit linux)
```
0x000000000000 - 0x00007fffffff: Lower half (kernel space)
0x800000000000 - 0x7fffffffffff: Upper half (user space)
                        ↑
                        Your address is here
```                        

```
0x7fff ffff dbc0
│     │     └── {{Offset within page}}
│     └──────── Middle bits
└──────────────  User space indicator (0x7f)
```

### address vs data
```
Address      vs      Data
0x7fffffffdbc0      0x414141
│                   │
└── One complete    └── Three separate
    memory pointer      bytes of data

Like:
Street address      vs      Content
"1234 Main St"          "AAA"
(one complete       (three separate
 address)            characters)
```

0x414141 represents data (your "AAA" input):

- {{It's 3 bytes of actual content}}
- Read right to left as {{individual bytes}}: 41 41 41
- Each byte is meaningful (ASCII 'A')

0x7fffffffdbc0 is an address:

- It's one {{complete 64-bit}} value
- It's not meant to be broken into {{individual meaningful bytes}}
- It represents a {{single location in memory}}

Although you can technicailly it byte by byte
```
c0 = 11000000
db = 11011011
ff = 11111111
ff = 11111111
ff = 11111111
ff = 11111111
7f = 01111111
```

But it is pointless

