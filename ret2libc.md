ret2libc attack:
- It's a technique where we make the program return to functions in the C library (libc)
- Commonly used to get a shell by calling system("/bin/sh")
- We use this when we can't execute code on the stack (NX is enabled, as shown in your checksec output)

Normal program flow: [[Normal function return]]

Buffer overflow for ret2libc:

```
Original stack:
[32 byte buffer ] 
[8 byte old rbp ]
[Return Address ] <- We overflow up to here!

We overflow with:
[AAAAAAAA...   ] <- 40 bytes (buffer + old rbp)
[pop rdi addr  ] <- This becomes the new return address!
[puts_got addr ]
[puts_plt addr ]
[main addr     ]
```

When the function returns:

1. CPU reads return address (which we overwrote with pop rdi gadget address)
2. Jumps to the pop rdi instruction
3. pop rdi instruction:
- Takes next value from stack (puts_got addr) and puts it in rdi register
- The ret part then gets next address (puts_plt)
4. Jumps to puts_plt, which now uses the value in rdi as its argument
It's like creating a chain reaction:

It's like creating a chain reaction:

```
1. ret → reads pop_rdi address → jumps there
2. pop rdi → reads puts_got → puts in rdi register
3. ret → reads puts_plt → jumps there
4. puts executes with rdi value as argument
5. ret → reads main → jumps there
```
The intention here is to leak a function's address in libc, calculate libc's base address and calculate the exact addresses of functions we want to use, e.g. system() to call shellcode

#### why reading GOT before PLT

Noraml puts call:

```c
puts("Hello");  // Normal usage
// This goes through: PLT → GOT → real puts function
```


```c
puts(puts_got_address);  // We're printing the GOT entry itself!
// This makes puts print the address stored in its own GOT entry
```


```apache
Memory:
puts_got (at 0x601018) contains: 0x7ffff7a649c0 (actual puts in libc)

Our payload makes:
puts(0x601018) 
↓
prints: 0x7ffff7a649c0
↓
Now we know where puts is in libc!
```