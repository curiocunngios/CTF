---
aliases:
  - Instruction Set Architectures
tags:
  - flashcard/active/ctf/HTB
---

An **Instruction Set Architecture (ISA)** specifies the syntax and semantics of the assembly language on each architecture. It is not just a different syntax but is built in the core design of a processor, as it affects the way and order instructions are executed and their level of complexity. ISA mainly consists of the following components:
- Instructions
- Registers
- Memory Addresses
- Data Types <!--SR:!2025-01-30,3,250-->


Instructions: The instruction to be processed in the opcode operand_list format. There are usually 1,2, or 3 comma-separated operands.	Example: `add rax, 1, mov rsp, rax, push rax`  

Registers: Used to store {{operands, addresses, or instructions}} temporarily.	Example: `rax, rsp, rip`  

Memory Addresses: The address in which {{data or instructions}} are stored. May point to memory or registers.	Example: `0xffffffffaa8a25ff, 0x44d0, $rax`  

Data Types: The type of stored data.	byte, word, double word <!--SR:!2025-01-30,3,250!2025-01-30,3,250-->

Above are the main components that distinguish different ISA's and assembly languages.

Two main Instruction Set Architectures that are widely used:

- Complex Instruction Set Computer (CISC) - Used in Intel and AMD processors in most computers and servers.

- Reduced Instruction Set Computer (RISC) - Used in ARM and Apple processors, in most smartphones, and some modern laptops.


# CISC
the CISC architecture favors more {{complex instructions to be run at a time to reduce the overall number of instructions}}. This is done to rely as much as possible on the CPU by combining minor instructions into more complex instructions. <!--SR:!2025-01-30,3,250-->

- To enable more instructions to be executed at once
- In the past, memory and transistors were limited, so it was preferred to write shorter programs by combining multiple instructions into one.

# RISC
The RISC architecture favors {{splitting instructions into minor instructions}}, and so the CPU is designed only to handle simple instructions. This is done to relay the optimization to the software by writing the most optimized assembly code. <!--SR:!2025-01-30,3,250-->

For example, the same previous `add r1, r2, r3` instruction on a RISC processor would fetch r2, then fetch r3, add them, and finally store them in r1. Every instruction of these takes {{an entire 'Fetch-Decode-Execute-Store' instruction cycle}}, which leads, as can be expected, to a larger number of total instructions per program, and hence a longer assembly code. <!--SR:!2025-01-30,3,250-->

By not supporting various types of complex instructions, RISC processors only support a limited number of instructions (~200) compared to CISC processors (~1500). So, to execute complex instructions, this has to be done through a combination of minor instructions through Assembly.

It is said that we can build a general-purpose computer with a processor that only supports one instruction! This indicates that we can create very complex instructions using the sub instruction only. 

On the other hand, an advantage of splitting complex instructions into minor ones is having all instructions of the same length either 32-bit or 64-bit long. This enables designing the CPU clock speed around the instruction length so that executing each stage in the instruction cycle would always take precisely one machine clock cycle.

The below diagram shows how CISC instructions take a variable amount of clock cycles, while RISC instructions take a fixed amount:

![alt text](<../linked images/CISCRISC.png>)


# CISC vs RISC Architecture

## Key Differences

| Area | CISC | RISC |
|------|------|------|
| Complexity | Complex instructions | Simple instructions |
| Instruction Length | Variable (multiples of 8-bits) | Fixed (32-bit/64-bit) |
| Program Size | Fewer instructions, shorter code | More instructions, longer code |
| Optimization | Hardware-based (CPU) | Software-based (Assembly) |
| Execution Time | Multiple clock cycles | One clock cycle |
| Instruction Set | ~1500 instructions | ~200 instructions |
| Power Usage | High consumption | Very low consumption |

