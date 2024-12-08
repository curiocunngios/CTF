---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - assembly
tags:
  - flashcard/active/ctf/testing/temp
  - function/index
  - language/in/English
---

#### Basics
Memory operand :: A location in memory that is used as a source or destination for data operations <!--SR:!2024-12-09,1,225-->
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
<!--SR:!2024-12-09,1,230-->

`call` addr ::: used to call a {{subroutine (function)}} and transfer control to its starting address <!--SR:!2000-01-01,1,250!2024-12-12,4,270-->
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

#### Comparison Instructions

CMP operand1, operand2 ::: Performs operand1 - operand2, sets processor flags without storing result

TEST operand1, operand2 ::: Performs operand1 AND operand2, sets flags without storing result

#### Processor Flags
??  
Key processor flags affected by CMP:

- ZF (Zero Flag): Set to 1 if comparison result is zero (values are equal)
- SF (Sign Flag): Set to 1 if result is negative
- CF (Carry Flag): Set to 1 if borrow needed (for unsigned numbers)
- OF (Overflow Flag): Set to 1 if signed overflow occurs

#### How CMP and Flags Work
??
1. CMP performs subtraction internally
2. Results set processor flags
3. Conditional jumps use these flags to decide whether to jump
Example:
```assembly
CMP AX, BX    ; If AX=5, BX=3: 
              ; - Performs 5-3
              ; - Sets flags based on result
JG  Label     ; Checks flags to see if AX>BX
```
<!--SR:!2024-12-09,1,230-->

#### TEST Instruction and Bits  
??  

- A bit is {{a single binary digit (0 or 1)}}
- "Set" means {{bit is 1}}
- "Reset" means {{bit is 0}}
Example:
```as
TEST AL, 01h  ; Tests if lowest bit is 1
```

#### Conditional Jumps  
??  
Equal/Not Equal:  

- JE/JZ ::: Jump if Equal (ZF=1)
- JNE/JNZ ::: Jump if Not Equal (ZF=0)
- Signed Comparisons:

- JG/JNLE ::: Jump if Greater (signed)
- JL/JNGE ::: Jump if Less (signed)
- JGE/JNL ::: Jump if Greater or Equal
- JLE/JNG ::: Jump if Less or Equal <!--SR:!2024-12-09,1,230!2000-01-01,1,250-->

#### Jump Instruction Naming  
??  

- J means {{Jump}}  
- E means {{Equal}}  
- N means {{Not}}  
- G means {{Greater}}  
- L means {{Less}}  
- Z means {{Zero}}  
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
xchg operand1, operand2 ::: Exchange the contents of two operands <!--SR:!2000-01-01,1,250!2024-12-09,1,230-->
xchg is equivalent to  
??  
```as
temp = operand1
operand1 = operand2
operand2 = temp
```

#### flags
ZF (Zero Flag)  
??  
- 1 if equal (result is zero)  
- 0 if not equal  

SF (Sign Flag)  

- 1 if result is negative  
- 0 if result is positive  
  
CF (Carry Flag)  
??
- 1 if borrow needed (for unsigned comparison)  
- Set when operand1 < operand2 (unsigned)  

OF (Overflow Flag)  
??
- 1 if signed overflow occurs  
- Used for signed arithmetic  

PF (Parity Flag)  
??
- 1 if result has even number of 1 bits  
- 0 if odd number of 1 bits  

AF (Auxiliary Flag)  
??
- 1 if borrow needed for low nibble  
- Used for BCD arithmetic  