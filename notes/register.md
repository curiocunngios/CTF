---
aliases:
  - Registers
tags:
  - flashcard/active/ctf
---

# Register
RAX  :: Accumulator register, often for function returns <!--SR:!2024-12-15,1,210-->
RBX  :: Base register, preserved across function calls <!--SR:!2024-12-29,15,290-->
RCX  :: Counter register, used for loops/string operations <!--SR:!2024-12-17,3,250-->
RDX  :: Data register, often used for function parameters <!--SR:!2024-12-16,2,230-->
RDI  :: Destination index, first function parameter <!--SR:!2024-12-17,3,250-->
RSI  :: Source index, second function parameter <!--SR:!2024-12-17,3,250-->
R8-R15 :: General purpose registers <!--SR:!2024-12-17,3,250-->
RBP  :: Base pointer (frame pointer) <!--SR:!2024-12-17,3,250-->
RSP  :: Stack pointer <!--SR:!2024-12-17,3,250-->
RIP  :: Instruction pointer (current instruction) <!--SR:!2024-12-17,3,250-->

## RAX
### EAX = 0
- clears out the {{lower 32 bits}} (least significant) for RAX
```
RAX (64-bit):
[               RAX (64 bits)               ]
[       EAX (32 bits)      ][  unused      ]
[   AX (16)   ][         ][  unused      ]
[ AH (8) ][ AL (8) ][         ][  unused      ]

Before:
RAX: [XXXX XXXX XXXX XXXX] (64 bits, X = unknown value)
     [XXXX XXXX][XXXX XXXX]
     
After mov eax, 0:
RAX: [0000 0000 XXXX XXXX]
     [0000 0000][XXXX XXXX]
                ↑
                Lower 32 bits zeroed
```
- required by the calling convention of x64 before variadic functions which are {{functions with variable arguments like printf}}
- 0 refers to the number of vector registers which is for {{floating point}} arguments <!--SR:!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250-->

## RIP 

### Modification of RIP
- pop rip is invalid because {{RIP/EIP (Instruction Pointer) cannot be directly modified in x86/x86_64 assembly}}
- you can't directly manipulate it like a general-purpose register.
```
pop rip    # Invalid - cannot directly modify RIP
ret        # Valid - implicitly pops into RIP
```
This is a hardware/architecture restriction:
- RIP/EIP is a special register that {{controls program execution}}
- For security and stability, {{CPU restricts direct modification}}
- Only {{certain instructions (ret, call, jmp, etc.)}} can modify it
- These instructions are specifically {{designed for control flow}} <!--SR:!2024-12-17,3,237!2024-12-17,3,237!2024-12-17,3,237!2024-12-17,3,237!2024-12-17,3,237-->
