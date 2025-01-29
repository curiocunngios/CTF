---
aliases:
  - Registers
tags:
  - flashcard/active/ctf/
---

# Registers

Each {{CPU core}} has a set of registers. The registers are the {{fastest components}} in any computer, as they are built within the CPU core. However, registers are very limited in size and can only hold a few bytes of data at a time. <!--SR:!2025-02-03,4,272!2025-02-03,4,270--> 

## Data Registers
are usually used for storing {{instructions/syscall arguments}}. The primary data registers are: {{`rax, rbx, rcx, and rdx`}}. The `rdi` and `rsi` registers also exist and are usually used for the {{instruction destination and source operands}}. Then, we have secondary data registers that can be used when all previous registers are in use, which are `r8, r9, and r10`.
- rax
- rbx
- rcx
- rdx
- r8
- r9
- r10 <!--SR:!2000-01-01,1,250!2025-02-02,3,252!2025-02-02,3,252-->

## Pointer Registers
are used to store specific {{important address pointers}}. The main pointer registers are the Base Stack Pointer rbp, which points to the beginning of the Stack, the Current Stack Pointer rsp, {{which points to the current location within the Stack (top of the Stack)}}, and the Instruction Pointer rip, {{which holds the address of the next instruction}}.
- rbp
- rsp
- rip <!--SR:!2000-01-01,1,250!2025-02-02,3,250!2000-01-01,1,250-->

# Sub-registers
Each `64-bit` register can be further divided into smaller sub-registers containing the lower bits, at one byte `8-bits`, 2 bytes `16-bits`, and 4 bytes `32-bits`. Each sub-register can be used and accessed on its own, so we don't have to consume {{the full 64-bits if we have a smaller amount of data}}.
![alt text](<../linked images/subREG.png>) <!--SR:!2025-02-03,4,272-->

## How to access
| Size in bits | Size in bytes | Name | Example |
|------------|--------------|------|----------|
| 16-bit | 2 bytes | the base name | ax |
| 8-bit | 1 bytes | base name and/or ends with `l` | al |
| 32-bit | 4 bytes | base name + starts with the `e` prefix | eax |
| 64-bit | 8 bytes | base name + starts with the `r` prefix | rax |
For example, for the `bx` data register, {{the 16-bit is `bx`, so the 8-bit is `bl`, the 32-bit would be `ebx`, and the 64-bit would be `rbx`}}. The same goes for pointer registers. If we take the base stack pointer `bp`, {{its 16-bit sub-register is `bp`, so the 8-bit is `bpl`, the 32-bit is `ebp`, and the 64-bit is `rbp`}}. <!--SR:!2000-01-01,1,250!2025-02-02,3,252-->


| Description | 64-bit Register | 32-bit Register | 16-bit Register | 8-bit Register |
|------------|----------------|-----------------|-----------------|----------------|
| Data/Arguments Registers |
| Syscall Number/Return value | rax | eax | ax | al |
| Callee Saved | rbx | ebx | bx | bl |
| 1st arg - Destination operand | rdi | edi | di | dil |
| 2nd arg - Source operand | rsi | esi | si | sil |
| 3rd arg | rdx | edx | dx | dl |
| 4th arg - Loop counter | rcx | ecx | cx | cl |
| 5th arg | r8 | r8d | r8w | r8b |
| 6th arg | r9 | r9d | r9w | r9b |
| **Pointer Registers** |
| Base Stack Pointer | rbp | ebp | bp | bpl |
| Current/Top Stack Pointer | rsp | esp | sp | spl |
| Instruction Pointer 'call only' | rip | eip | ip | ipl | <!--SR:!2025-02-02,3,252-->

