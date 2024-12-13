---
aliases:
  - memory address
tags:
  - flashcard/active/ctf/yo
---
# Memory address
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
Above is a [user space](<User Space.md>) memory address in a {{64-bit system}}:
- Starting with 0x7f: In Linux x86_64, [user space](<User Space.md>) addresses typically start with 0x7f
- Many f's: Indicates this is in the {{higher end}} of virtual memory
- Last 12 bits (bc0): Specific {{offset}} within a page
```
0x7fff ffff dbc0
│     │     └── {{Offset within page}}
│     └──────── Middle bits
└──────────────  User space indicator (0x7f)
```
<!--SR:!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250-->

### Difference between address and data hexadecimal presentation
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
#### 0x414141
It represents data: `"AAA"`
- It's 3 bytes of {{actual content}}
- Read right to left as {{individual bytes}}: 41 41 41
- Each byte is {{meaningful (ASCII 'A')}}
#### 0x7fffffffdbc0
It is an address
- It's one {{complete 64-bit}} value
- It's not meant to be broken into {{individual meaningful bytes}}
- It represents a {{single location in memory}} <!--SR:!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250-->

Although you can technicailly look at it byte by byte
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

