# Where is instructions written 
```
115f:	48 89 e6             	mov    rsi,rsp
1162:	31 c0                	xor    eax,eax
1164:	ff 15 66 9e 00 00    	call   QWORD PTR [rip+0x9e66]        # afd0 <scanf@GLIBC_2.2.5>
116a:	48 8b 04 24          	mov    rax,QWORD PTR [rsp]
```
There are two instructions in between the stack, they don't get written to the stack so it wouldn't affect the value of rsp 
Instead, the instructions gets 
- written to {{text segment (code section)}}
- They're loaded into memory when program starts
- But they're in a different memory region from the stack
Layout:
```json
High addresses
    [Stack]        <- rsp points here (grows down)
    [Heap]
    [BSS]
    [Data]
    [Text/Code]    <- instructions are here
Low addresses
```
Although there was a function call 
> `call   QWORD PTR [rip + 0x9e66]    <scanf>`
it was a PLT/GOT call, not direct call. SO the address does not get pushed onto rsp

This is different from a regular call instruction because:

    It's an indirect call through the PLT (Procedure Linkage Table)
    The actual call mechanics are handled by the dynamic linker
    The return address handling is done differently since it's a libc function call

When calling external functions like scanf:

    The PLT/GOT mechanism is used to resolve the actual function address
    The calling convention for external functions may preserve RSP
    The libc function manages its own stack frame independently





