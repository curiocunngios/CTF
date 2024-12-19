# Initial observation 
- program waits for inputs 
- inputs 
- enter (`\n`)
- nothing happens
- repeat
- shows `:(`

# Dive into assembly 
The intention is to understand the behaviour of the program 

## Typical function prologue 
```
    1149:	55                   	push   rbp          # function prologue
    114a:	48 89 e5             	mov    rbp,rsp      # function prologue
    114d:	48 83 ec 40          	sub    rsp,0x40     # allocate 64 bytes on stack
```
The assembly instructions here first save old rbp value (`1` in this case), then move rbp to point to the base of new frame (`main`). Finally, allocate 64 bytes for potentially local variables, code, etc. 

~~perhaps i don't have to make notes, just write writeups and use them as flashcards lol~~

## calling scanf to get input 


```
    1151:	48 8d 05 d0 2e 00 00 	lea    rax,[rip+0x2ed0]        # 4028 <input.0>                          
    1158:	48 89 c6             	mov    rsi,rax      # <input.0> (what is this?) goes into rsi
     115b:	48 8d 05 a2 0e 00 00 	lea    rax,[rip+0xea2]        # 2004 <_IO_stdin_used+0x4>
    1162:	48 89 c7             	mov    rdi,rax      # <_IO_stdin_used+0x4> 
    1165:	b8 00 00 00 00       	mov    eax,0x0      #  zero out lower 32 bit of rax
    116a:	e8 d1 fe ff ff       	call   1040 <__isoc99_scanf@plt>
```

Here the function `scanf` is called with `# <_IO_stdin_used+0x4>` i.e. `%5c` from inspection of hexdump, as the first argument `rdi`. Second argument is `<input.0>` which seems to be an unintialized variable in .bss segment that is not present in hexdump and static assembly source. I guess it's just where it stores the input

So the above few codes looks like this in c and python:
```c
scanf(%5c, input)
```
```py
input = input()[:5]
```
Which receives exactly 5 bytes of input from user

Similarly,
```
    116f:	48 8d 05 b2 2e 00 00 	lea    rax,[rip+0x2eb2]        # 4028 <input.0>
    1176:	48 89 c6             	mov    rsi,rax
    1179:	48 8d 05 88 0e 00 00 	lea    rax,[rip+0xe88]        # 2008 <_IO_stdin_used+0x8>
    1180:	48 89 c7             	mov    rdi,rax
    1183:	b8 00 00 00 00       	mov    eax,0x0
    1188:	e8 b3 fe ff ff       	call   1040 <__isoc99_scanf@plt>
```
It calls `scanf` again to get input but this time the first argument is `%8c` from raw address `0x2008` which is just beside `%5c`, to get 8 bytes of input from user.

Interesting point is that the input seemed to be stored in the exact same variable `<input.0>` in `0x4028`

~~ I am currently writing this writeup while doing but I guess it's better to first focus on finishing the challenge first. Come back and write this writeup as a revise and learning process. Now I am kinda losing focus~~