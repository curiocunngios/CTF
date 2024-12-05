ret
 ● Pop a value from the top of the stack and jump there
 ● Equivalent to pop rip, but is valid assembly code
 ● ret
 ret 
COMP2633 Competitive Programming in Cybersecurity I
 pop rip ; rip := top of stack ; rsp++
 ; jmp rip ; setting rip to a value can be seen as 
jumping to said valu


### how is pop rip invalid and ret making it valid?

pop rip is invalid because RIP/EIP (Instruction Pointer) cannot be directly modified in x86/x86_64 assembly - you can't directly manipulate it like a general-purpose register.


```
pop rip    # Invalid - cannot directly modify RIP
ret        # Valid - implicitly pops into RIP
```


This is a hardware/architecture restriction:

- RIP/EIP is a special register that controls program execution
- For security and stability, CPU restricts direct modification
- Only certain instructions (ret, call, jmp, etc.) can modify it
- These instructions are specifically designed for control flow


ret is essentially doing pop rip but it's a dedicated instruction that the CPU allows. The CPU implements ret as:

- Pop value from stack
- Move that value to RIP
- Continue execution at new RIP value
This restriction helps maintain:

Program flow control
- Security (can't arbitrarily jump anywhere)
- Proper function call/return mechanics