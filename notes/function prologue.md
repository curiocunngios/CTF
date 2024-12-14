---
aliases:
  - Function's start 
  - Stack frame's start
  - Beginning of frame
tags:
  - flashcard/active/ctf
---


# Function Prologue assembly instruction
??
```
0x40118b: push   rbp        # Save old base pointer on stack
0x40118c: mov    rbp,rsp    # Set up new base pointer for this frame
```
## Right before `push rbp`
```as
RBP  1
 RSP  0x7fffffffdc38 —▸ 0x7ffff7ddbd68 (__libc_start_call_main+120) ◂— mov edi, eax
 RIP  0x55555555519e (main) ◂— push rbp
───────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────
 ► 0x55555555519e <main>       push   rbp
   0x55555555519f <main+1>     mov    rbp, rsp     RBP => 0x7fffffffdc30 ◂— 1
─────────────────────────────────────────────────────[ STACK ]─────────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffdc38 —▸ 0x7ffff7ddbd68 (__libc_start_call_main+120) ◂— mov edi, eax
```
## After `push rbp`
```
RBP  1
*RSP  0x7fffffffdc30 ◂— 1
*RIP  0x55555555519f (main+1) ◂— mov rbp, rsp
───────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────
   0x55555555519e <main>       push   rbp
 ► 0x55555555519f <main+1>     mov    rbp, rsp     RBP => 0x7fffffffdc30 ◂— 1
─────────────────────────────────────────────────────[ STACK ]─────────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffdc30 ◂— 1
```
What happened above is that {{rsp--}} and rbp's value gets {{copied to rsp}}
## After `mov    rbp, rsp`
```
*RBP  0x7fffffffdc30 ◂— 1
 RSP  0x7fffffffdc30 ◂— 1
*RIP  0x5555555551a2 (main+4) ◂— mov eax, 0
───────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────
   0x55555555519e <main>       push   rbp
   0x55555555519f <main+1>     mov    rbp, rsp     RBP => 0x7fffffffdc30 ◂— 1
 ► 0x5555555551a2 <main+4>     mov    eax, 0       EAX => 0
─────────────────────────────────────────────────────[ STACK ]─────────────────────────────────────────────────────
00:0000│ rbp rsp 0x7fffffffdc30 ◂— 1
```
The entirety of RSP was {{copied}} RBP and now they point to {{same address}}

## The stack operation
How does stack looks like from before prologue to after prologue
??
```
Before prologue:
        [old rbp]
        [......]                       <--- (other data e.g. cosmetic point arguments)
        [old return addr]  <--- RSP (call <addr> pushes next instruction here)
        [......]

After push rbp:
        [old return addr]
        [old rbp]                 <--- RSP
        [......]

After mov rbp,rsp:
        [old return addr]
        [old rbp]                <--- RBP, RSP
        [......]
```
<!--SR:!2024-12-18,4,274-->

- RBP value is saved below the return address to be {{restored later during `leave` instruction}} <!--SR:!2024-12-18,4,270--> 

### Assembly instructions in details

`push` Item :: Pushes Item to the top of the frame <!--SR:!2024-12-18,4,270-->
`push` is equivalent to
??
```as
sub rsp, 1    ; Item to be appended in the top slot, allocate space 
mov rsp, Item ; Move Item to the top slot
Item can be address, value, registers, instruction, etc. (Basically anything).
```
<!--SR:!2024-12-18,4,270-->

