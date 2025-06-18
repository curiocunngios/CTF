# Memory segments
Memory in x86 is organized into segments:
- Data Segment: {{Global/static variables}}
- Stack Segment: {{Local variables, function parameters}}
- Code Segment: {{Program instructions}}
## QWORD PTR syntax on different segments
```nasm 
; With base register (stack)
mov rax, QWORD PTR [rbp-0x8]    ; Access stack variable

; Without base register (data)
mov rax, QWORD PTR [0x123456]   ; Access global variable
```
Example:
```
mov    rax,QWORD PTR [rip+0x2e94]        # 0x4028 <input.0>
```
means:

- {{Calculate address}}: current instruction pointer + 0x2e94
- Treat that location as an {{8-byte value (QWORD)}}

The addressing modes are crucial for understanding how the program accesses different types of variables and data structures in memory.