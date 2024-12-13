---
aliases:
  - Function's end 
  - Stack frame's end
  - End of frame
tags:
  - flashcard/active/ctf
---


# Function epilogue assembly instruction
??
```
0x8049370  <vuln+56>                       leave  
0x8049371  <vuln+57>                       ret                                <main+107>
```
<!--SR:!2024-12-17,3,248-->

## The stack operation
How does stack looks like from before epilogue to after epilogue
??
```
Before epilogue:
        [higher addresses]

        [rbp of prev frame]
        [......]                       
        [old return addr]  
        [prev rbp addr]             <--- RBP
        [...]
        [top of stack]              <--- RSP

        [lower addresses]
After leave(mov rsp,rbp; pop rbp):
        [rbp of prev frame]         <--- RBP (restored after pop)
        [......]                       
        [old return addr]           <--- RSP
        [prev rbp addr]             
        [...]                       // effectively "removed", no longer accessible via stack pointers
        [top of stack]              // effectively "removed", no longer accessible via stack pointers

After ret:
        [rbp of prev frame]         <--- RBP
        [next instruction]          <--- RSP
```
<!--SR:!2024-12-16,3,259-->

- RBP value is saved below the return address to be {{restored later during `leave` instruction}} <!--SR:!2024-12-17,3,230-->

### Assembly instructions in details

`leave` :: Prepare to leave the frame by closing the frame and restoring old base pointer <!--SR:!2024-12-18,4,270-->
`leave` is equivalent to
??
```as
mov rsp, rbp    ; rsp := rbp. Closes the frame
pop rbp         ; rbp := top of stack (expected to be old rbp), rsp++. Points back to rbp of previous frame, restoring old rbp 
                ; rsp++ (expected to be pointing to return address)
```
<!--SR:!2024-12-17,3,248-->

`ret` :: Return to frame's caller <!--SR:!2024-12-17,3,248-->
`ret` is equivalent to
??
```as
pop rip     ; rip = top of the stack, which is expected to be return address i.e. the address of next instruction after -- call <func addr>
            ; rip = addr is equivalent to jumping to the address 
```
<!--SR:!2024-12-17,3,248-->


- `ret` is essentially doing `pop rip` but it's a {{dedicated instruction}}that the CPU allows. The CPU implements `ret` as: 
- `Pop` value from stack
- Move that value to `RIP`
- Continue execution at new `RIP` value
- this restriction helps maintain {{program flow control}}
- {{Security}} (can't arbitrarily jump anywhere)
- Proper function {{call/return mechanics}} <!--SR:!2024-12-15,1,219!2024-12-17,3,259!2024-12-17,3,259!2024-12-17,3,259-->