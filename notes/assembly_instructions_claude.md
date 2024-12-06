---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - assembly
tags:
  - flashcard/active/ctf/testing
  - function/index
  - language/in/English
---

#### Basics
Memory operand :: A location in memory that is used as a source or destination for data operations  
Register :: {{A small, fast storage location}} built directly into the processor  

#### Common Registers  
General Purpose Registers   
??  
- RAX: {{Accumulator, used for arithmetic operations and return values}}  
- RBX: {{Base register, used as a pointer to data}}
- RCX: {{Counter register, used in loop operations}}
- RDX: {{Data register, used in arithmetic and I/O operations}}
- RSI: {{Source Index, source in string operations}}
- RDI: {{Destination Index, destination in string operations}}

Special Purpose Registers   
??  
- RIP: {{Instruction Pointer, points to next instruction}}
- RSP: {{Stack Pointer, points to top of stack}}
- RBP: {{Base Pointer, points to base of current stack frame}}

#### Basic instructions 
`mov` destination, source ::: Used to copy data from one location to another  
`mov` destination, source is equivalent to   
??  
```as
destination = source

Destination: register or memory location    
Source: register, immediate value, or memory location
```

`lea` destination, source ::: Used to compute the address of a memory operand and store it in a register  
`lea` destination, source is equivalent to  
??   
```as
destination = &source  // Note: & means "address of"

Destination: A register to store the computed address    
Source: A memory operand or an address calculation
```

`call` addr ::: used to call a {{subroutine (function)}} and transfer control to its starting address  
`call` is equivalent to
??  
```as
push rip  ; Save return address
jmp addr  ; Jump to subroutine
```


`push` Item ::: Pushes Item to the top of the stack  
`push` is equivalent to
??  
```as
sub rsp, 8     ; Decrease stack pointer (stack grows downward)
mov [rsp], Item ; Move Item to new top of stack
```
Item can be {{address, value, registers, instruction, etc. basically anything}}  

#### Arithmetic Instructions
`add` dest, source ::: Add source to destination and store in destination    
`add` dest, source is equivalent to  
??  
```as
dest = dest + source
```

`sub` dest, source ::: Subtract source from destination  
`sub` dest, source is equivalent to    
??   
```as
dest = dest - source
```

#### Comparison and Jumping
cmp operand1, operand2 ::: Compare two values by subtraction (without storing result)  
test operand1, operand2 ::: Compare two values by AND operation (without storing result)  
  
Conditional Jumps
??

- je/jz: {{Jump if equal/zero}}
- jne/jnz: {{Jump if not equal/not zero}}
- jg/jnle: {{Jump if greater (signed)}}
- jl/jnge: {{Jump if less (signed)}}
- jge/jnl: {{Jump if greater or equal}}
- jle/jng: {{Jump if less or equal}}
#### Function epilogue
`leave` ::: Preparing to leave a stack frame by cleaning it up and restoring base pointer of previous frame  
`leave` is equivalent to  
??  
```as
mov rsp, rbp  ; Restore stack pointer
pop rbp       ; Restore previous frame's base pointer
```

`ret` ::: Return to the caller  
`ret` is equivalent to  
??  

```as
pop rip ; Pop return address into instruction pointer
```

#### Data Movement
xchg operand1, operand2 ::: Exchange the contents of two operands  
xchg is equivalent to  
??  
```as
temp = operand1
operand1 = operand2
operand2 = temp
```