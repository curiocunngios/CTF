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

## MOre of x command
instructions have different lengths and x command {{shows chunks with fixed length}}. Therefore, not all instructions after one can be shown using x command
```
0x40113a:    48 83 ec 40          sub    rsp, 0x40              # 4 bytes
0x40113e:    48 8d 05 bf 0e 00 00 lea    rax, [rip + 0xebf]    # 7 bytes
0x401145:    48 89 c7             mov    rdi, rax               # 3 bytes
0x401148:    b8 00 00 00 00       mov    eax, 0                 # 5 bytes
```

```
sub rsp, 0x40
48 83 ec 40
│  │  │  │
│  │  │  └─ immediate value (0x40)
│  │  └──── opcode extension (ec = subtract)
│  └────── REX.W prefix (48 = 64-bit operand)
└───────── REX prefix

lea rax, [rip + 0xebf]
48 8d 05 bf 0e 00 00
│  │  │  │  │  │  │
│  │  │  └──┴──┴──┴── 32-bit displacement (0xebf)
│  │  └── ModR/M byte
│  └──── opcode (8d = lea)
└────── REX.W prefix

mov rdi, rax
48 89 c7
│  │  │
│  │  └─ ModR/M byte (c7 = register addressing)
│  └──── opcode (89 = mov)
└────── REX.W prefix

mov eax, 0
b8 00 00 00 00
│  │  │  │  │
│  └──┴──┴──┴── immediate value (0)
└── opcode (b8 = mov to eax)
```