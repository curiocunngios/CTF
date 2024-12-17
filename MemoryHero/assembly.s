    sub    rsp,0x8
    mov    rax,QWORD PTR [rip+0x9fbd]        # afc8 <__gmon_start__@Base>
    test   rax,rax
    je     1012 <_init+0x12>
    call   rax
    add    rsp,0x8
    ret
    push   QWORD PTR [rip+0x9fca]        # aff0 <_GLOBAL_OFFSET_TABLE_+0x8>
    jmp    QWORD PTR [rip+0x9fcc]        # aff8 <_GLOBAL_OFFSET_TABLE_+0x10>
    nop    DWORD PTR [rax+0x0]
    jmp    QWORD PTR [rip+0x9faa]        # afe0 <__cxa_finalize@GLIBC_2.2.5>
    xchg   ax,ax
    xor    ebp,ebp
    mov    r9,rdx
    pop    rsi
    mov    rdx,rsp
    and    rsp,0xfffffffffffffff0
    push   rax
    push   rsp
    xor    r8d,r8d
    xor    ecx,ecx
    lea    rdi,[rip+0xd5]        # 1130 <main>
    call   QWORD PTR [rip+0x9f4f]        # afb0 <__libc_start_main@GLIBC_2.34>
    hlt
    cs nop WORD PTR [rax+rax*1+0x0]
    nop    DWORD PTR [rax+0x0]
    lea    rdi,[rip+0xa059]        # b0d0 <__TMC_END__>
    lea    rax,[rip+0xa052]        # b0d0 <__TMC_END__>
    cmp    rax,rdi
    je     1098 <deregister_tm_clones+0x28>
    mov    rax,QWORD PTR [rip+0x9f2e]        # afb8 <_ITM_deregisterTMCloneTable@Base>
    test   rax,rax
    je     1098 <deregister_tm_clones+0x28>
    jmp    rax
    nop    DWORD PTR [rax+0x0]
    ret
    nop    DWORD PTR [rax+0x0]
    lea    rdi,[rip+0xa029]        # b0d0 <__TMC_END__>
    lea    rsi,[rip+0xa022]        # b0d0 <__TMC_END__>
    sub    rsi,rdi
    mov    rax,rsi
    shr    rsi,0x3f
    sar    rax,0x3
    add    rsi,rax
    sar    rsi,1
    je     10d8 <register_tm_clones+0x38>
    mov    rax,QWORD PTR [rip+0x9f0d]        # afd8 <_ITM_registerTMCloneTable@Base>
    test   rax,rax
    je     10d8 <register_tm_clones+0x38>
    jmp    rax
    nop    WORD PTR [rax+rax*1+0x0]
    ret
    nop    DWORD PTR [rax+0x0]
    endbr64
    cmp    BYTE PTR [rip+0x9fe1],0x0        # b0cc <completed.0>
    jne    1118 <__do_global_dtors_aux+0x38>
    push   rbp
    cmp    QWORD PTR [rip+0x9eea],0x0        # afe0 <__cxa_finalize@GLIBC_2.2.5>
    mov    rbp,rsp
    je     1107 <__do_global_dtors_aux+0x27>
    mov    rdi,QWORD PTR [rip+0x9f06]        # b008 <__dso_handle>
    call   1030 <__cxa_finalize@plt>
    call   1070 <deregister_tm_clones>
    mov    BYTE PTR [rip+0x9fb9],0x1        # b0cc <completed.0>
    pop    rbp
    ret
    nop    DWORD PTR [rax]
    ret
    nop    DWORD PTR [rax+0x0]
    endbr64
    jmp    10a0 <register_tm_clones>
    nop    DWORD PTR [rax+0x0]
    push   rbp
    mov    rbp,rsp
    sub    rsp,0x10
    lea    rdi,[rip+0x9eda]        # b019 <intro>
    xor    eax,eax
    call   QWORD PTR [rip+0x9e79]        # afc0 <printf@GLIBC_2.2.5>
    xor    rbx,rbx
000000000000114a <node0>:
    lea    rax,[rip+0x9f7f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x66
    inc    rbx
    lea    rdi,[rip+0x9eb1]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9e66]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x85
    je     33a7 <node133>
    cmp    rax,0x3c
    je     218c <node60>
    cmp    rax,0xdc
    je     4e32 <node220>
    jmp    8e4d <fail_code>
0000000000001195 <node1>:
    lea    rax,[rip+0x9f34]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x72
    inc    rbx
    lea    rdi,[rip+0x9e66]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9e1b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe3
    je     5009 <node227>
    cmp    rax,0x12e
    je     661e <node302>
    jmp    8e4d <fail_code>
00000000000011d6 <node2>:
    lea    rax,[rip+0x9ef3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xd
    inc    rbx
    lea    rdi,[rip+0x9e25]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9dda]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x67
    je     2b99 <node103>
    cmp    rax,0x1ae
    je     881a <node430>
    cmp    rax,0x106
    je     5a8a <node262>
    jmp    8e4d <fail_code>
0000000000001221 <node3>:
    lea    rax,[rip+0x9ea8]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5f
    inc    rbx
    lea    rdi,[rip+0x9dda]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9d8f]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x130
    je     6672 <node304>
    cmp    rax,0xfa
    je     56d2 <node250>
    cmp    rax,0x19a
    je     8366 <node410>
    cmp    rax,0xfc
    je     57fe <node252>
    cmp    rax,0x13d
    je     6a8f <node317>
    jmp    8e4d <fail_code>
0000000000001286 <node4>:
    lea    rax,[rip+0x9e43]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x41
    inc    rbx
    lea    rdi,[rip+0x9d75]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9d2a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x32
    je     1ece <node50>
    cmp    rax,0x22
    je     1ae0 <node34>
    cmp    rax,0x123
    je     63b9 <node291>
    jmp    8e4d <fail_code>
00000000000012cf <node5>:
    lea    rax,[rip+0x9dfa]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6f
    inc    rbx
    lea    rdi,[rip+0x9d2c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9ce1]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x101
    je     5933 <node257>
    jmp    8e4d <fail_code>
0000000000001304 <node6>:
    lea    rax,[rip+0x9dc5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4e
    inc    rbx
    lea    rdi,[rip+0x9cf7]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9cac]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xde
    je     4ebe <node222>
    cmp    rax,0x32
    je     1ece <node50>
    cmp    rax,0xc2
    je     4580 <node194>
    jmp    8e4d <fail_code>
000000000000134f <node7>:
    lea    rax,[rip+0x9d7a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x59
    inc    rbx
    lea    rdi,[rip+0x9cac]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9c61]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x13b
    je     69d9 <node315>
    cmp    rax,0xd6
    je     4c58 <node214>
    cmp    rax,0x16c
    je     77c2 <node364>
    cmp    rax,0x113
    je     5ed1 <node275>
    jmp    8e4d <fail_code>
00000000000013a8 <node8>:
    lea    rax,[rip+0x9d21]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5b
    inc    rbx
    lea    rdi,[rip+0x9c53]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9c08]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xf7
    je     55b3 <node247>
    cmp    rax,0x11d
    je     61cd <node285>
    jmp    8e4d <fail_code>
00000000000013e9 <node9>:
    lea    rax,[rip+0x9ce0]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7c
    inc    rbx
    lea    rdi,[rip+0x9c12]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9bc7]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x184
    je     7d56 <node388>
    jmp    8e4d <fail_code>
000000000000141e <node10>:
    lea    rax,[rip+0x9cab]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x24
    inc    rbx
    lea    rdi,[rip+0x9bdd]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9b92]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xac
    je     3fc4 <node172>
    cmp    rax,0x30
    je     1e30 <node48>
    cmp    rax,0x10e
    je     5cc4 <node270>
    cmp    rax,0xd2
    je     4af2 <node210>
    cmp    rax,0x9
    je     13e9 <node9>
    cmp    rax,0x7f
    je     324f <node127>
    jmp    8e4d <fail_code>
0000000000001489 <node11>:
    lea    rax,[rip+0x9c40]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x26
    inc    rbx
    jmp    8e4d <fail_code>
000000000000149c <node12>:
    lea    rax,[rip+0x9c2d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x55
    inc    rbx
    lea    rdi,[rip+0x9b5f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9b14]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1ab
    je     87b3 <node427>
    cmp    rax,0x14d
    je     6f05 <node333>
    cmp    rax,0x3b
    je     2137 <node59>
    cmp    rax,0x16e
    je     785c <node366>
    jmp    8e4d <fail_code>
00000000000014f3 <node13>:
    lea    rax,[rip+0x9bd6]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    lea    rdi,[rip+0x9b08]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9abd]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xda
    je     4d7c <node218>
    cmp    rax,0x126
    je     644a <node294>
    cmp    rax,0x8
    je     13a8 <node8>
    cmp    rax,0xa4
    je     3dec <node164>
    cmp    rax,0x86
    je     343a <node134>
    cmp    rax,0xf0
    je     5374 <node240>
    cmp    rax,0x7e
    je     31f6 <node126>
    cmp    rax,0x121
    je     6311 <node289>
    cmp    rax,0xf3
    je     5491 <node243>
    cmp    rax,0x165
    je     7541 <node357>
    jmp    8e4d <fail_code>
0000000000001590 <node14>:
    lea    rax,[rip+0x9b39]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x40
    inc    rbx
    jmp    8e4d <fail_code>
00000000000015a3 <node15>:
    lea    rax,[rip+0x9b26]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x77
    inc    rbx
    lea    rdi,[rip+0x9a58]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9a0d]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x5b
    je     28c9 <node91>
    cmp    rax,0x87
    je     3479 <node135>
    cmp    rax,0xfd
    je     585f <node253>
    jmp    8e4d <fail_code>
00000000000015ee <node16>:
    lea    rax,[rip+0x9adb]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    lea    rdi,[rip+0x9a0d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x99c2]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a8
    je     86f4 <node424>
    cmp    rax,0xac
    je     3fc4 <node172>
    cmp    rax,0x27
    je     1c9b <node39>
    cmp    rax,0xd6
    je     4c58 <node214>
    cmp    rax,0x1af
    je     882d <node431>
    cmp    rax,0x7b
    je     30fd <node123>
    cmp    rax,0x49
    je     2499 <node73>
    cmp    rax,0xe3
    je     5009 <node227>
    jmp    8e4d <fail_code>
0000000000001671 <node17>:
    lea    rax,[rip+0x9a58]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x37
    inc    rbx
    jmp    8e4d <fail_code>
0000000000001684 <node18>:
    lea    rax,[rip+0x9a45]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x54
    inc    rbx
    lea    rdi,[rip+0x9977]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x992c]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x21
    je     1aad <node33>
    cmp    rax,0x19
    je     187f <node25>
    cmp    rax,0x12c
    je     65ca <node300>
    jmp    8e4d <fail_code>
00000000000016cd <node19>:
    lea    rax,[rip+0x99fc]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x66
    inc    rbx
    lea    rdi,[rip+0x992e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x98e3]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x4d
    je     25c3 <node77>
    jmp    8e4d <fail_code>
0000000000001700 <node20>:
    lea    rax,[rip+0x99c9]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5f
    inc    rbx
    lea    rdi,[rip+0x98fb]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x98b0]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xd5
    je     4be9 <node213>
    cmp    rax,0x5c
    je     291c <node92>
    cmp    rax,0x1c
    je     18fa <node28>
    cmp    rax,0x39
    je     206f <node57>
    jmp    8e4d <fail_code>
0000000000001753 <node21>:
    lea    rax,[rip+0x9976]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7a
    inc    rbx
    lea    rdi,[rip+0x98a8]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x985d]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x6
    je     1304 <node6>
    cmp    rax,0x12a
    je     6584 <node298>
    cmp    rax,0x43
    je     232f <node67>
    jmp    8e4d <fail_code>
000000000000179c <node22>:
    lea    rax,[rip+0x992d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x31
    inc    rbx
    lea    rdi,[rip+0x985f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9814]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x11f
    je     6289 <node287>
    jmp    8e4d <fail_code>
00000000000017d1 <node23>:
    lea    rax,[rip+0x98f8]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x63
    inc    rbx
    lea    rdi,[rip+0x982a]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x97df]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xa5
    je     3dff <node165>
    cmp    rax,0x131
    je     66f7 <node305>
    jmp    8e4d <fail_code>
0000000000001812 <node24>:
    lea    rax,[rip+0x98b7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x9
    inc    rbx
    lea    rdi,[rip+0x97e9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x979e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x52
    je     26a4 <node82>
    cmp    rax,0x152
    je     7002 <node338>
    cmp    rax,0x8
    je     13a8 <node8>
    cmp    rax,0x8f
    je     36f7 <node143>
    cmp    rax,0x95
    je     3909 <node149>
    cmp    rax,0xb9
    je     432d <node185>
    jmp    8e4d <fail_code>
000000000000187f <node25>:
    lea    rax,[rip+0x984a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x52
    inc    rbx
    lea    rdi,[rip+0x977c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9731]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x29
    je     1cf7 <node41>
    jmp    8e4d <fail_code>
00000000000018b2 <node26>:
    lea    rax,[rip+0x9817]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x25
    inc    rbx
    jmp    8e4d <fail_code>
00000000000018c5 <node27>:
    lea    rax,[rip+0x9804]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x61
    inc    rbx
    lea    rdi,[rip+0x9736]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x96eb]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xab
    je     3fb1 <node171>
    jmp    8e4d <fail_code>
00000000000018fa <node28>:
    lea    rax,[rip+0x97cf]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x41
    inc    rbx
    lea    rdi,[rip+0x9701]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x96b6]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x174
    je     79c2 <node372>
    cmp    rax,0x18c
    je     7ff6 <node396>
    cmp    rax,0xf8
    je     55f0 <node248>
    cmp    rax,0x19d
    je     8485 <node413>
    cmp    rax,0x163
    je     7493 <node355>
    cmp    rax,0x149
    je     6de5 <node329>
    jmp    8e4d <fail_code>
000000000000196b <node29>:
    lea    rax,[rip+0x975e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5b
    inc    rbx
    lea    rdi,[rip+0x9690]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9645]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x4b
    je     2539 <node75>
    jmp    8e4d <fail_code>
000000000000199e <node30>:
    lea    rax,[rip+0x972b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x25
    inc    rbx
    jmp    8e4d <fail_code>
00000000000019b1 <node31>:
    lea    rax,[rip+0x9718]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2d
    inc    rbx
    lea    rdi,[rip+0x964a]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x95ff]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x17
    je     17d1 <node23>
    cmp    rax,0x9e
    je     3c7e <node158>
    cmp    rax,0x58
    je     286e <node88>
    cmp    rax,0x11e
    je     620c <node286>
    jmp    8e4d <fail_code>
0000000000001a06 <node32>:
    lea    rax,[rip+0x96c3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7a
    inc    rbx
    lea    rdi,[rip+0x95f5]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x95aa]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1b
    je     18c5 <node27>
    cmp    rax,0x164
    je     74ec <node356>
    cmp    rax,0xb4
    je     4212 <node180>
    cmp    rax,0x8e
    je     36ac <node142>
    cmp    rax,0xc0
    je     4518 <node192>
    cmp    rax,0xb0
    je     40fe <node176>
    cmp    rax,0x2e
    je     1db4 <node46>
    cmp    rax,0xb7
    je     42b9 <node183>
    cmp    rax,0x119
    je     609b <node281>
    cmp    rax,0x121
    je     6311 <node289>
    cmp    rax,0x69
    je     2c35 <node105>
    jmp    8e4d <fail_code>
0000000000001aad <node33>:
    lea    rax,[rip+0x961c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x56
    inc    rbx
    lea    rdi,[rip+0x954e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9503]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x66
    je     2b64 <node102>
    jmp    8e4d <fail_code>
0000000000001ae0 <node34>:
    lea    rax,[rip+0x95e9]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x28
    inc    rbx
    lea    rdi,[rip+0x951b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x94d0]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x10e
    je     5cc4 <node270>
    cmp    rax,0x6c
    je     2cb2 <node108>
    cmp    rax,0x50
    je     265c <node80>
    jmp    8e4d <fail_code>
0000000000001b29 <node35>:
    lea    rax,[rip+0x95a0]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3a
    inc    rbx
    lea    rdi,[rip+0x94d2]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9487]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x72
    je     2e2a <node114>
    cmp    rax,0x126
    je     644a <node294>
    cmp    rax,0xa2
    je     3d68 <node162>
    cmp    rax,0x9c
    je     3bc4 <node156>
    cmp    rax,0xd2
    je     4af2 <node210>
    cmp    rax,0xb2
    je     4186 <node178>
    cmp    rax,0x49
    je     2499 <node73>
    cmp    rax,0x87
    je     3479 <node135>
    cmp    rax,0x3d
    je     21e1 <node61>
    cmp    rax,0x153
    je     706f <node339>
    jmp    8e4d <fail_code>
0000000000001bc4 <node36>:
    lea    rax,[rip+0x9505]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x64
    inc    rbx
    lea    rdi,[rip+0x9437]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x93ec]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x13
    je     16cd <node19>
    cmp    rax,0xde
    je     4ebe <node222>
    jmp    8e4d <fail_code>
0000000000001c03 <node37>:
    lea    rax,[rip+0x94c6]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x57
    inc    rbx
    lea    rdi,[rip+0x93f8]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x93ad]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a3
    je     861b <node419>
    cmp    rax,0x147
    je     6d9d <node327>
    cmp    rax,0x5e
    je     29e0 <node94>
    jmp    8e4d <fail_code>
0000000000001c4e <node38>:
    lea    rax,[rip+0x947b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7c
    inc    rbx
    lea    rdi,[rip+0x93ad]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9362]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x174
    je     79c2 <node372>
    cmp    rax,0x114
    je     5ee4 <node276>
    cmp    rax,0x181
    je     7ce7 <node385>
    jmp    8e4d <fail_code>
0000000000001c9b <node39>:
    lea    rax,[rip+0x942e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x60
    inc    rbx
    lea    rdi,[rip+0x9360]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9315]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xd7
    je     4ca5 <node215>
    cmp    rax,0x2d
    je     1da1 <node45>
    cmp    rax,0x7d
    je     31ab <node125>
    jmp    8e4d <fail_code>
0000000000001ce4 <node40>:
    lea    rax,[rip+0x93e5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x54
    inc    rbx
    jmp    8e4d <fail_code>
0000000000001cf7 <node41>:
    lea    rax,[rip+0x93d2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3e
    inc    rbx
    lea    rdi,[rip+0x9304]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x92b9]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x15f
    je     737d <node351>
    cmp    rax,0x154
    je     70d2 <node340>
    jmp    8e4d <fail_code>
0000000000001d38 <node42>:
    lea    rax,[rip+0x9391]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7a
    inc    rbx
    jmp    8e4d <fail_code>
0000000000001d4b <node43>:
    lea    rax,[rip+0x937e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x36
    inc    rbx
    jmp    8e4d <fail_code>
0000000000001d5e <node44>:
    lea    rax,[rip+0x936b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x41
    inc    rbx
    lea    rdi,[rip+0x929d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9252]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x4e
    je     25d6 <node78>
    cmp    rax,0x2d
    je     1da1 <node45>
    cmp    rax,0x70
    je     2dd8 <node112>
    jmp    8e4d <fail_code>
0000000000001da1 <node45>:
    lea    rax,[rip+0x9328]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2e
    inc    rbx
    jmp    8e4d <fail_code>
0000000000001db4 <node46>:
    lea    rax,[rip+0x9315]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7d
    inc    rbx
    lea    rdi,[rip+0x9247]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x91fc]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x28
    je     1ce4 <node40>
    cmp    rax,0x33
    je     1f03 <node51>
    cmp    rax,0x9
    je     13e9 <node9>
    jmp    8e4d <fail_code>
0000000000001dfb <node47>:
    lea    rax,[rip+0x92ce]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    lea    rdi,[rip+0x9200]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x91b5]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x148
    je     6db0 <node328>
    jmp    8e4d <fail_code>
0000000000001e30 <node48>:
    lea    rax,[rip+0x9299]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x43
    inc    rbx
    lea    rdi,[rip+0x91cb]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9180]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x192
    je     81ae <node402>
    cmp    rax,0x5e
    je     29e0 <node94>
    jmp    8e4d <fail_code>
0000000000001e6f <node49>:
    lea    rax,[rip+0x925a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x31
    inc    rbx
    lea    rdi,[rip+0x918c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9141]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x7c
    je     3148 <node124>
    cmp    rax,0x13c
    je     6a22 <node316>
    cmp    rax,0x79
    je     3071 <node121>
    cmp    rax,0x127
    je     649f <node295>
    cmp    rax,0xd
    je     14f3 <node13>
    jmp    8e4d <fail_code>
0000000000001ece <node50>:
    lea    rax,[rip+0x91fb]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x28
    inc    rbx
    lea    rdi,[rip+0x912d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x90e2]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x173
    je     79af <node371>
    jmp    8e4d <fail_code>
0000000000001f03 <node51>:
    lea    rax,[rip+0x91c6]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3d
    inc    rbx
    lea    rdi,[rip+0x90f8]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x90ad]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x11d
    je     61cd <node285>
    cmp    rax,0x5f
    je     29f3 <node95>
    jmp    8e4d <fail_code>
0000000000001f42 <node52>:
    lea    rax,[rip+0x9187]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xa
    inc    rbx
    lea    rdi,[rip+0x90b9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x906e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xa2
    je     3d68 <node162>
    jmp    8e4d <fail_code>
0000000000001f77 <node53>:
    lea    rax,[rip+0x9152]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xc
    inc    rbx
    lea    rdi,[rip+0x9084]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9039]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a9
    je     8727 <node425>
    cmp    rax,0x121
    je     6311 <node289>
    jmp    8e4d <fail_code>
0000000000001fb8 <node54>:
    lea    rax,[rip+0x9111]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x77
    inc    rbx
    lea    rdi,[rip+0x9043]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8ff8]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x10e
    je     5cc4 <node270>
    cmp    rax,0x131
    je     66f7 <node305>
    cmp    rax,0x181
    je     7ce7 <node385>
    jmp    8e4d <fail_code>
0000000000002005 <node55>:
    lea    rax,[rip+0x90c4]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xd
    inc    rbx
    jmp    8e4d <fail_code>
0000000000002018 <node56>:
    lea    rax,[rip+0x90b1]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x50
    inc    rbx
    lea    rdi,[rip+0x8fe3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8f98]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x11b
    je     614d <node283>
    cmp    rax,0x1
    je     1195 <node1>
    cmp    rax,0x1a5
    je     866d <node421>
    cmp    rax,0x16f
    je     789b <node367>
    jmp    8e4d <fail_code>
000000000000206f <node57>:
    lea    rax,[rip+0x905a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    lea    rdi,[rip+0x8f8c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8f41]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x142
    je     6c54 <node322>
    cmp    rax,0x10f
    je     5d0d <node271>
    cmp    rax,0x109
    je     5af1 <node265>
    jmp    8e4d <fail_code>
00000000000020bc <node58>:
    lea    rax,[rip+0x900d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5a
    inc    rbx
    lea    rdi,[rip+0x8f3f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8ef4]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x82
    je     32c0 <node130>
    cmp    rax,0x19c
    je     8446 <node412>
    cmp    rax,0x8f
    je     36f7 <node143>
    cmp    rax,0x12
    je     1684 <node18>
    cmp    rax,0x99
    je     3a85 <node153>
    cmp    rax,0x1a7
    je     86c1 <node423>
    cmp    rax,0x111
    je     5daf <node273>
    jmp    8e4d <fail_code>
0000000000002137 <node59>:
    lea    rax,[rip+0x8f92]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x37
    inc    rbx
    lea    rdi,[rip+0x8ec4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8e79]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x15b
    je     72b3 <node347>
    cmp    rax,0x2a
    je     1d38 <node42>
    cmp    rax,0x2d
    je     1da1 <node45>
    cmp    rax,0x1b5
    je     8997 <node437>
    jmp    8e4d <fail_code>
000000000000218c <node60>:
    lea    rax,[rip+0x8f3d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x79
    inc    rbx
    lea    rdi,[rip+0x8e6f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8e24]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x124
    je     6404 <node292>
    cmp    rax,0x33
    je     1f03 <node51>
    cmp    rax,0x19d
    je     8485 <node413>
    cmp    rax,0x27
    je     1c9b <node39>
    jmp    8e4d <fail_code>
00000000000021e1 <node61>:
    lea    rax,[rip+0x8ee8]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x66
    inc    rbx
    lea    rdi,[rip+0x8e1a]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8dcf]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x5
    je     12cf <node5>
    cmp    rax,0x17c
    je     7b4c <node380>
    cmp    rax,0x69
    je     2c35 <node105>
    cmp    rax,0x173
    je     79af <node371>
    jmp    8e4d <fail_code>
0000000000002236 <node62>:
    lea    rax,[rip+0x8e93]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x32
    inc    rbx
    lea    rdi,[rip+0x8dc5]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8d7a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x32
    je     1ece <node50>
    jmp    8e4d <fail_code>
0000000000002269 <node63>:
    lea    rax,[rip+0x8e60]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    jmp    8e4d <fail_code>
000000000000227c <node64>:
    lea    rax,[rip+0x8e4d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x60
    inc    rbx
    jmp    8e4d <fail_code>
000000000000228f <node65>:
    lea    rax,[rip+0x8e3a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6b
    inc    rbx
    lea    rdi,[rip+0x8d6c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8d21]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1c4
    je     8dbe <node452>
    jmp    8e4d <fail_code>
00000000000022c4 <node66>:
    lea    rax,[rip+0x8e05]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4c
    inc    rbx
    lea    rdi,[rip+0x8d37]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8cec]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x100
    je     5920 <node256>
    cmp    rax,0x92
    je     381e <node146>
    cmp    rax,0x4e
    je     25d6 <node78>
    cmp    rax,0x16
    je     179c <node22>
    cmp    rax,0x35
    je     1f77 <node53>
    cmp    rax,0x17f
    je     7c21 <node383>
    jmp    8e4d <fail_code>
000000000000232f <node67>:
    lea    rax,[rip+0x8d9a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4d
    inc    rbx
    jmp    8e4d <fail_code>
0000000000002342 <node68>:
    lea    rax,[rip+0x8d87]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    lea    rdi,[rip+0x8cb9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8c6e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x140
    je     6b98 <node320>
    cmp    rax,0x14a
    je     6e26 <node330>
    cmp    rax,0xf2
    je     53f4 <node242>
    jmp    8e4d <fail_code>
000000000000238f <node69>:
    lea    rax,[rip+0x8d3a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x72
    inc    rbx
    lea    rdi,[rip+0x8c6c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8c21]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xdd
    je     4e7d <node221>
    cmp    rax,0x11c
    je     618e <node284>
    cmp    rax,0x80
    je     329a <node128>
    jmp    8e4d <fail_code>
00000000000023dc <node70>:
    lea    rax,[rip+0x8ced]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x43
    inc    rbx
    lea    rdi,[rip+0x8c1f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8bd4]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x45
    je     238f <node69>
    cmp    rax,0xab
    je     3fb1 <node171>
    cmp    rax,0xf3
    je     5491 <node243>
    cmp    rax,0xae
    je     407e <node174>
    jmp    8e4d <fail_code>
000000000000242f <node71>:
    lea    rax,[rip+0x8c9a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3c
    inc    rbx
    jmp    8e4d <fail_code>
0000000000002442 <node72>:
    lea    rax,[rip+0x8c87]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x73
    inc    rbx
    lea    rdi,[rip+0x8bb9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8b6e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x12f
    je     6631 <node303>
    cmp    rax,0x2
    je     11d6 <node2>
    cmp    rax,0x1a7
    je     86c1 <node423>
    cmp    rax,0xb3
    je     41bb <node179>
    jmp    8e4d <fail_code>
0000000000002499 <node73>:
    lea    rax,[rip+0x8c30]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x21
    inc    rbx
    lea    rdi,[rip+0x8b62]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8b17]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1be
    je     8be4 <node446>
    cmp    rax,0xa0
    je     3d08 <node160>
    cmp    rax,0x67
    je     2b99 <node103>
    cmp    rax,0x7d
    je     31ab <node125>
    cmp    rax,0x69
    je     2c35 <node105>
    jmp    8e4d <fail_code>
00000000000024f8 <node74>:
    lea    rax,[rip+0x8bd1]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x71
    inc    rbx
    lea    rdi,[rip+0x8b03]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8ab8]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x106
    je     5a8a <node262>
    cmp    rax,0xd7
    je     4ca5 <node215>
    jmp    8e4d <fail_code>
0000000000002539 <node75>:
    lea    rax,[rip+0x8b90]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x34
    inc    rbx
    lea    rdi,[rip+0x8ac2]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8a77]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x104
    je     5a16 <node260>
    cmp    rax,0xa
    je     141e <node10>
    cmp    rax,0xe4
    je     501c <node228>
    jmp    8e4d <fail_code>
0000000000002584 <node76>:
    lea    rax,[rip+0x8b45]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x61
    inc    rbx
    lea    rdi,[rip+0x8a77]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8a2c]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x19e
    je     84e6 <node414>
    cmp    rax,0x46
    je     23dc <node70>
    jmp    8e4d <fail_code>
00000000000025c3 <node77>:
    lea    rax,[rip+0x8b06]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x47
    inc    rbx
    jmp    8e4d <fail_code>
00000000000025d6 <node78>:
    lea    rax,[rip+0x8af3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x42
    inc    rbx
    jmp    8e4d <fail_code>
00000000000025e9 <node79>:
    lea    rax,[rip+0x8ae0]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x44
    inc    rbx
    lea    rdi,[rip+0x8a12]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x89c7]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x36
    je     1fb8 <node54>
    cmp    rax,0x4e
    je     25d6 <node78>
    cmp    rax,0x69
    je     2c35 <node105>
    cmp    rax,0x19b
    je     83ef <node411>
    cmp    rax,0xd7
    je     4ca5 <node215>
    cmp    rax,0x14b
    je     6e7f <node331>
    cmp    rax,0x117
    je     5f8f <node279>
    jmp    8e4d <fail_code>
000000000000265c <node80>:
    lea    rax,[rip+0x8a6d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6f
    inc    rbx
    jmp    8e4d <fail_code>
000000000000266f <node81>:
    lea    rax,[rip+0x8a5a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7b
    inc    rbx
    lea    rdi,[rip+0x898c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8941]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xb2
    je     4186 <node178>
    jmp    8e4d <fail_code>
00000000000026a4 <node82>:
    lea    rax,[rip+0x8a25]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3d
    inc    rbx
    lea    rdi,[rip+0x8957]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x890c]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe8
    je     514a <node232>
    cmp    rax,0xa7
    je     3e95 <node167>
    cmp    rax,0x14e
    je     6f46 <node334>
    jmp    8e4d <fail_code>
00000000000026f1 <node83>:
    lea    rax,[rip+0x89d8]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x47
    inc    rbx
    jmp    8e4d <fail_code>
0000000000002704 <node84>:
    lea    rax,[rip+0x89c5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4e
    inc    rbx
    lea    rdi,[rip+0x88f7]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x88ac]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x122
    je     6364 <node290>
    cmp    rax,0xaa
    je     3f7e <node170>
    cmp    rax,0x188
    je     7e9a <node392>
    cmp    rax,0xd4
    je     4baa <node212>
    cmp    rax,0x1a1
    je     8577 <node417>
    cmp    rax,0x165
    je     7541 <node357>
    jmp    8e4d <fail_code>
0000000000002775 <node85>:
    lea    rax,[rip+0x8954]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x35
    inc    rbx
    lea    rdi,[rip+0x8886]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x883b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a6
    je     8680 <node422>
    cmp    rax,0x10e
    je     5cc4 <node270>
    cmp    rax,0x13e
    je     6adc <node318>
    jmp    8e4d <fail_code>
00000000000027c2 <node86>:
    lea    rax,[rip+0x8907]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x36
    inc    rbx
    lea    rdi,[rip+0x8839]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x87ee]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x10
    je     15ee <node16>
    cmp    rax,0x10a
    je     5b48 <node266>
    cmp    rax,0x9b
    je     3b4b <node155>
    cmp    rax,0x71
    je     2deb <node113>
    jmp    8e4d <fail_code>
0000000000002817 <node87>:
    lea    rax,[rip+0x88b2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2c
    inc    rbx
    lea    rdi,[rip+0x87e4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8799]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x62
    je     2a92 <node98>
    cmp    rax,0xc4
    je     460c <node196>
    cmp    rax,0xa6
    je     3e3e <node166>
    cmp    rax,0xf8
    je     55f0 <node248>
    jmp    8e4d <fail_code>
000000000000286e <node88>:
    lea    rax,[rip+0x885b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x44
    inc    rbx
    lea    rdi,[rip+0x878d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8742]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x15b
    je     72b3 <node347>
    jmp    8e4d <fail_code>
00000000000028a3 <node89>:
    lea    rax,[rip+0x8826]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    jmp    8e4d <fail_code>
00000000000028b6 <node90>:
    lea    rax,[rip+0x8813]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x60
    inc    rbx
    jmp    8e4d <fail_code>
00000000000028c9 <node91>:
    lea    rax,[rip+0x8800]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7b
    inc    rbx
    lea    rdi,[rip+0x8732]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x86e7]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x168
    je     7668 <node360>
    cmp    rax,0x76
    je     2f9e <node118>
    cmp    rax,0xb
    je     1489 <node11>
    cmp    rax,0x1e
    je     199e <node30>
    jmp    8e4d <fail_code>
000000000000291c <node92>:
    lea    rax,[rip+0x87ad]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6f
    inc    rbx
    lea    rdi,[rip+0x86df]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8694]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xba
    je     4340 <node186>
    cmp    rax,0x72
    je     2e2a <node114>
    cmp    rax,0x122
    je     6364 <node290>
    cmp    rax,0x190
    je     811c <node400>
    cmp    rax,0x7d
    je     31ab <node125>
    cmp    rax,0x99
    je     3a85 <node153>
    cmp    rax,0x19b
    je     83ef <node411>
    jmp    8e4d <fail_code>
0000000000002995 <node93>:
    lea    rax,[rip+0x8734]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x34
    inc    rbx
    lea    rdi,[rip+0x8666]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x861b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x196
    je     82aa <node406>
    cmp    rax,0x2
    je     11d6 <node2>
    cmp    rax,0x86
    je     343a <node134>
    jmp    8e4d <fail_code>
00000000000029e0 <node94>:
    lea    rax,[rip+0x86e9]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5f
    inc    rbx
    jmp    8e4d <fail_code>
00000000000029f3 <node95>:
    lea    rax,[rip+0x86d6]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    lea    rdi,[rip+0x8608]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x85bd]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1ba
    je     8afa <node442>
    jmp    8e4d <fail_code>
0000000000002a28 <node96>:
    lea    rax,[rip+0x86a1]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x50
    inc    rbx
    lea    rdi,[rip+0x85d3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8588]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1ac
    je     87f4 <node428>
    jmp    8e4d <fail_code>
0000000000002a5d <node97>:
    lea    rax,[rip+0x866c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x42
    inc    rbx
    lea    rdi,[rip+0x859e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8553]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x8c
    je     3606 <node140>
    jmp    8e4d <fail_code>
0000000000002a92 <node98>:
    lea    rax,[rip+0x8637]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x34
    inc    rbx
    jmp    8e4d <fail_code>
0000000000002aa5 <node99>:
    lea    rax,[rip+0x8624]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3e
    inc    rbx
    lea    rdi,[rip+0x8556]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x850b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x19f
    je     8525 <node415>
    cmp    rax,0xe1
    je     4fad <node225>
    cmp    rax,0x199
    je     8327 <node409>
    jmp    8e4d <fail_code>
0000000000002af2 <node100>:
    lea    rax,[rip+0x85d7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4d
    inc    rbx
    jmp    8e4d <fail_code>
0000000000002b05 <node101>:
    lea    rax,[rip+0x85c4]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x60
    inc    rbx
    lea    rdi,[rip+0x84f6]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x84ab]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe8
    je     514a <node232>
    cmp    rax,0x2
    je     11d6 <node2>
    cmp    rax,0x7
    je     134f <node7>
    cmp    rax,0xc1
    je     454b <node193>
    cmp    rax,0x61
    je     2a5d <node97>
    jmp    8e4d <fail_code>
0000000000002b64 <node102>:
    lea    rax,[rip+0x8565]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x66
    inc    rbx
    lea    rdi,[rip+0x8497]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x844c]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x151
    je     6fef <node337>
    jmp    8e4d <fail_code>
0000000000002b99 <node103>:
    lea    rax,[rip+0x8530]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xb
    inc    rbx
    jmp    8e4d <fail_code>
0000000000002bac <node104>:
    lea    rax,[rip+0x851d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x38
    inc    rbx
    lea    rdi,[rip+0x844f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8404]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1c0
    je     8c5a <node448>
    cmp    rax,0x1a6
    je     8680 <node422>
    cmp    rax,0x138
    je     6918 <node312>
    cmp    rax,0xae
    je     407e <node174>
    cmp    rax,0x19c
    je     8446 <node412>
    cmp    rax,0x1ac
    je     87f4 <node428>
    cmp    rax,0x139
    je     696f <node313>
    cmp    rax,0x15d
    je     7335 <node349>
    jmp    8e4d <fail_code>
0000000000002c35 <node105>:
    lea    rax,[rip+0x8494]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7e
    inc    rbx
    jmp    8e4d <fail_code>
0000000000002c48 <node106>:
    lea    rax,[rip+0x8481]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7a
    inc    rbx
    jmp    8e4d <fail_code>
0000000000002c5b <node107>:
    lea    rax,[rip+0x846e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x52
    inc    rbx
    lea    rdi,[rip+0x83a0]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8355]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xf7
    je     55b3 <node247>
    cmp    rax,0x14c
    je     6ed2 <node332>
    cmp    rax,0x59
    je     28a3 <node89>
    cmp    rax,0x109
    je     5af1 <node265>
    jmp    8e4d <fail_code>
0000000000002cb2 <node108>:
    lea    rax,[rip+0x8417]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x75
    inc    rbx
    jmp    8e4d <fail_code>
0000000000002cc5 <node109>:
    lea    rax,[rip+0x8404]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x71
    inc    rbx
    lea    rdi,[rip+0x8336]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x82eb]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x188
    je     7e9a <node392>
    cmp    rax,0x124
    je     6404 <node292>
    cmp    rax,0xbc
    je     43ec <node188>
    cmp    rax,0xd2
    je     4af2 <node210>
    cmp    rax,0x152
    je     7002 <node338>
    jmp    8e4d <fail_code>
0000000000002d2a <node110>:
    lea    rax,[rip+0x839f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7b
    inc    rbx
    lea    rdi,[rip+0x82d1]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8286]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x9d
    je     3c05 <node157>
    cmp    rax,0xdb
    je     4dbb <node219>
    cmp    rax,0x56
    je     27c2 <node86>
    cmp    rax,0x159
    je     71fb <node345>
    jmp    8e4d <fail_code>
0000000000002d81 <node111>:
    lea    rax,[rip+0x8348]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x69
    inc    rbx
    lea    rdi,[rip+0x827a]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x822f]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x8c
    je     3606 <node140>
    cmp    rax,0xca
    je     485a <node202>
    cmp    rax,0x14c
    je     6ed2 <node332>
    cmp    rax,0x75
    je     2f6b <node117>
    jmp    8e4d <fail_code>
0000000000002dd8 <node112>:
    lea    rax,[rip+0x82f1]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x74
    inc    rbx
    jmp    8e4d <fail_code>
0000000000002deb <node113>:
    lea    rax,[rip+0x82de]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x72
    inc    rbx
    lea    rdi,[rip+0x8210]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x81c5]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x4b
    je     2539 <node75>
    cmp    rax,0x1a2
    je     85b8 <node418>
    jmp    8e4d <fail_code>
0000000000002e2a <node114>:
    lea    rax,[rip+0x829f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x24
    inc    rbx
    lea    rdi,[rip+0x81d1]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8186]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xf6
    je     557e <node246>
    cmp    rax,0x14d
    je     6f05 <node333>
    cmp    rax,0x1c5
    je     8dce <node453>
    cmp    rax,0x192
    je     81ae <node402>
    jmp    8e4d <fail_code>
0000000000002e83 <node115>:
    lea    rax,[rip+0x8246]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x34
    inc    rbx
    lea    rdi,[rip+0x8178]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x812d]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x132
    je     6738 <node306>
    cmp    rax,0x10c
    je     5c16 <node268>
    cmp    rax,0x15
    je     1753 <node21>
    cmp    rax,0xc5
    je     4659 <node197>
    cmp    rax,0xb7
    je     42b9 <node183>
    jmp    8e4d <fail_code>
0000000000002ee6 <node116>:
    lea    rax,[rip+0x81e3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x55
    inc    rbx
    lea    rdi,[rip+0x8115]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x80ca]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xca
    je     485a <node202>
    cmp    rax,0x86
    je     343a <node134>
    cmp    rax,0xbc
    je     43ec <node188>
    cmp    rax,0x190
    je     811c <node400>
    cmp    rax,0xc
    je     149c <node12>
    cmp    rax,0x165
    je     7541 <node357>
    cmp    rax,0x14b
    je     6e7f <node331>
    cmp    rax,0x3b
    je     2137 <node59>
    jmp    8e4d <fail_code>
0000000000002f6b <node117>:
    lea    rax,[rip+0x815e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3b
    inc    rbx
    lea    rdi,[rip+0x8090]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8045]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x69
    je     2c35 <node105>
    jmp    8e4d <fail_code>
0000000000002f9e <node118>:
    lea    rax,[rip+0x812b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x31
    inc    rbx
    lea    rdi,[rip+0x805d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x8012]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xcb
    je     48a5 <node203>
    jmp    8e4d <fail_code>
0000000000002fd3 <node119>:
    lea    rax,[rip+0x80f6]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3c
    inc    rbx
    lea    rdi,[rip+0x8028]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7fdd]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe2
    je     4fc0 <node226>
    cmp    rax,0x12
    je     1684 <node18>
    cmp    rax,0x119
    je     609b <node281>
    cmp    rax,0x63
    je     2aa5 <node99>
    cmp    rax,0x6f
    je     2d81 <node111>
    jmp    8e4d <fail_code>
0000000000003032 <node120>:
    lea    rax,[rip+0x8097]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x65
    inc    rbx
    lea    rdi,[rip+0x7fc9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7f7e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x70
    je     2dd8 <node112>
    cmp    rax,0xf6
    je     557e <node246>
    jmp    8e4d <fail_code>
0000000000003071 <node121>:
    lea    rax,[rip+0x8058]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6e
    inc    rbx
    lea    rdi,[rip+0x7f8a]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7f3f]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1b7
    je     89df <node439>
    cmp    rax,0xf5
    je     5527 <node245>
    jmp    8e4d <fail_code>
00000000000030b2 <node122>:
    lea    rax,[rip+0x8017]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x38
    inc    rbx
    lea    rdi,[rip+0x7f49]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7efe]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x87
    je     3479 <node135>
    cmp    rax,0x15a
    je     7276 <node346>
    cmp    rax,0x34
    je     1f42 <node52>
    jmp    8e4d <fail_code>
00000000000030fd <node123>:
    lea    rax,[rip+0x7fcc]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x31
    inc    rbx
    lea    rdi,[rip+0x7efe]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7eb3]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x98
    je     3a50 <node152>
    cmp    rax,0x1a8
    je     86f4 <node424>
    cmp    rax,0x53
    je     26f1 <node83>
    jmp    8e4d <fail_code>
0000000000003148 <node124>:
    lea    rax,[rip+0x7f81]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x66
    inc    rbx
    lea    rdi,[rip+0x7eb3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7e68]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x60
    je     2a28 <node96>
    cmp    rax,0x18c
    je     7ff6 <node396>
    cmp    rax,0x117
    je     5f8f <node279>
    cmp    rax,0x11d
    je     61cd <node285>
    cmp    rax,0x163
    je     7493 <node355>
    jmp    8e4d <fail_code>
00000000000031ab <node125>:
    lea    rax,[rip+0x7f1e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5d
    inc    rbx
    lea    rdi,[rip+0x7e50]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7e05]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x2c
    je     1d5e <node44>
    cmp    rax,0xc0
    je     4518 <node192>
    cmp    rax,0x113
    je     5ed1 <node275>
    jmp    8e4d <fail_code>
00000000000031f6 <node126>:
    lea    rax,[rip+0x7ed3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x52
    inc    rbx
    lea    rdi,[rip+0x7e05]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7dba]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x10b
    je     5be3 <node267>
    cmp    rax,0x1b5
    je     8997 <node437>
    cmp    rax,0x129
    je     654f <node297>
    cmp    rax,0xee
    je     52ac <node238>
    jmp    8e4d <fail_code>
000000000000324f <node127>:
    lea    rax,[rip+0x7e7a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x52
    inc    rbx
    lea    rdi,[rip+0x7dac]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7d61]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1af
    je     882d <node431>
    cmp    rax,0xa1
    je     3d55 <node161>
    cmp    rax,0x34
    je     1f42 <node52>
    jmp    8e4d <fail_code>
000000000000329a <node128>:
    lea    rax,[rip+0x7e2f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6a
    inc    rbx
    jmp    8e4d <fail_code>
00000000000032ad <node129>:
    lea    rax,[rip+0x7e1c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x51
    inc    rbx
    jmp    8e4d <fail_code>
00000000000032c0 <node130>:
    lea    rax,[rip+0x7e09]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x32
    inc    rbx
    lea    rdi,[rip+0x7d3b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7cf0]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x10e
    je     5cc4 <node270>
    cmp    rax,0x148
    je     6db0 <node328>
    cmp    rax,0xff
    je     58d5 <node255>
    cmp    rax,0xe7
    je     5117 <node231>
    cmp    rax,0x1ad
    je     8807 <node429>
    jmp    8e4d <fail_code>
0000000000003325 <node131>:
    lea    rax,[rip+0x7da4]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x78
    inc    rbx
    lea    rdi,[rip+0x7cd6]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7c8b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x12a
    je     6584 <node298>
    cmp    rax,0x16c
    je     77c2 <node364>
    cmp    rax,0x145
    je     6d57 <node325>
    cmp    rax,0xbb
    je     43ad <node187>
    cmp    rax,0x195
    je     8245 <node405>
    cmp    rax,0x7
    je     134f <node7>
    jmp    8e4d <fail_code>
0000000000003394 <node132>:
    lea    rax,[rip+0x7d35]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6a
    inc    rbx
    jmp    8e4d <fail_code>
00000000000033a7 <node133>:
    lea    rax,[rip+0x7d22]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7b
    inc    rbx
    lea    rdi,[rip+0x7c54]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7c09]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xb8
    je     42ee <node184>
    cmp    rax,0xe2
    je     4fc0 <node226>
    cmp    rax,0x92
    je     381e <node146>
    cmp    rax,0x18c
    je     7ff6 <node396>
    cmp    rax,0x160
    je     7390 <node352>
    cmp    rax,0x182
    je     7cfa <node386>
    cmp    rax,0x1b8
    je     8a42 <node440>
    cmp    rax,0x47
    je     242f <node71>
    cmp    rax,0x1a3
    je     861b <node419>
    jmp    8e4d <fail_code>
000000000000343a <node134>:
    lea    rax,[rip+0x7c8f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4e
    inc    rbx
    lea    rdi,[rip+0x7bc1]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7b76]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x10c
    je     5c16 <node268>
    cmp    rax,0x30
    je     1e30 <node48>
    jmp    8e4d <fail_code>
0000000000003479 <node135>:
    lea    rax,[rip+0x7c50]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x75
    inc    rbx
    lea    rdi,[rip+0x7b82]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7b37]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x50
    je     265c <node80>
    jmp    8e4d <fail_code>
00000000000034ac <node136>:
    lea    rax,[rip+0x7c1d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x68
    inc    rbx
    lea    rdi,[rip+0x7b4f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7b04]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x28
    je     1ce4 <node40>
    jmp    8e4d <fail_code>
00000000000034df <node137>:
    lea    rax,[rip+0x7bea]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5e
    inc    rbx
    lea    rdi,[rip+0x7b1c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7ad1]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x72
    je     2e2a <node114>
    cmp    rax,0x120
    je     62bc <node288>
    cmp    rax,0xc
    je     149c <node12>
    cmp    rax,0xd6
    je     4c58 <node214>
    cmp    rax,0x192
    je     81ae <node402>
    cmp    rax,0x185
    je     7d89 <node389>
    cmp    rax,0x177
    je     7a3f <node375>
    jmp    8e4d <fail_code>
0000000000003558 <node138>:
    lea    rax,[rip+0x7b71]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3f
    inc    rbx
    lea    rdi,[rip+0x7aa3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7a58]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xc4
    je     460c <node196>
    cmp    rax,0x48
    je     2442 <node72>
    cmp    rax,0x4
    je     1286 <node4>
    cmp    rax,0x162
    je     7434 <node354>
    cmp    rax,0xc2
    je     4580 <node194>
    cmp    rax,0x1af
    je     882d <node431>
    cmp    rax,0x163
    je     7493 <node355>
    jmp    8e4d <fail_code>
00000000000035d1 <node139>:
    lea    rax,[rip+0x7af8]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2f
    inc    rbx
    lea    rdi,[rip+0x7a2a]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x79df]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x107
    je     5a9d <node263>
    jmp    8e4d <fail_code>
0000000000003606 <node140>:
    lea    rax,[rip+0x7ac3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2c
    inc    rbx
    lea    rdi,[rip+0x79f5]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x79aa]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x14e
    je     6f46 <node334>
    cmp    rax,0x12d
    je     660b <node301>
    jmp    8e4d <fail_code>
0000000000003647 <node141>:
    lea    rax,[rip+0x7a82]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x31
    inc    rbx
    lea    rdi,[rip+0x79b4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7969]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x172
    je     797a <node370>
    cmp    rax,0x146
    je     6d6a <node326>
    cmp    rax,0x139
    je     696f <node313>
    cmp    rax,0x11f
    je     6289 <node287>
    cmp    rax,0x101
    je     5933 <node257>
    jmp    8e4d <fail_code>
00000000000036ac <node142>:
    lea    rax,[rip+0x7a1d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x31
    inc    rbx
    lea    rdi,[rip+0x794f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7904]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xf1
    je     53b3 <node241>
    cmp    rax,0x7d
    je     31ab <node125>
    cmp    rax,0xde
    je     4ebe <node222>
    jmp    8e4d <fail_code>
00000000000036f7 <node143>:
    lea    rax,[rip+0x79d2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3a
    inc    rbx
    lea    rdi,[rip+0x7904]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x78b9]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x129
    je     654f <node297>
    cmp    rax,0x141
    je     6c1f <node321>
    cmp    rax,0x4a
    je     24f8 <node74>
    jmp    8e4d <fail_code>
0000000000003742 <node144>:
    lea    rax,[rip+0x7987]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x79
    inc    rbx
    lea    rdi,[rip+0x78b9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x786e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x30
    je     1e30 <node48>
    cmp    rax,0x1ab
    je     87b3 <node427>
    cmp    rax,0x14e
    je     6f46 <node334>
    jmp    8e4d <fail_code>
000000000000378d <node145>:
    lea    rax,[rip+0x793c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7c
    inc    rbx
    lea    rdi,[rip+0x786e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7823]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x88
    je     34ac <node136>
    cmp    rax,0xcc
    je     48e6 <node204>
    cmp    rax,0x12c
    je     65ca <node300>
    cmp    rax,0xf4
    je     54f2 <node244>
    cmp    rax,0x101
    je     5933 <node257>
    cmp    rax,0x16
    je     179c <node22>
    cmp    rax,0x3d
    je     21e1 <node61>
    cmp    rax,0xc5
    je     4659 <node197>
    cmp    rax,0xc1
    je     454b <node193>
    jmp    8e4d <fail_code>
000000000000381e <node146>:
    lea    rax,[rip+0x78ab]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5e
    inc    rbx
    lea    rdi,[rip+0x77dd]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7792]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x34
    je     1f42 <node52>
    jmp    8e4d <fail_code>
0000000000003851 <node147>:
    lea    rax,[rip+0x7878]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x41
    inc    rbx
    lea    rdi,[rip+0x77aa]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x775f]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x8d
    je     3647 <node141>
    cmp    rax,0x7e
    je     31f6 <node126>
    cmp    rax,0x150
    je     6fdc <node336>
    cmp    rax,0x4e
    je     25d6 <node78>
    jmp    8e4d <fail_code>
00000000000038a6 <node148>:
    lea    rax,[rip+0x7823]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x76
    inc    rbx
    lea    rdi,[rip+0x7755]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x770a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x144
    je     6d22 <node324>
    cmp    rax,0x17a
    je     7ad2 <node378>
    cmp    rax,0x14b
    je     6e7f <node331>
    cmp    rax,0x131
    je     66f7 <node305>
    cmp    rax,0x7f
    je     324f <node127>
    jmp    8e4d <fail_code>
0000000000003909 <node149>:
    lea    rax,[rip+0x77c0]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x36
    inc    rbx
    lea    rdi,[rip+0x76f2]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x76a7]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x11a
    je     60f4 <node282>
    cmp    rax,0x1a0
    je     8538 <node416>
    cmp    rax,0x154
    je     70d2 <node340>
    cmp    rax,0x63
    je     2aa5 <node99>
    cmp    rax,0x13b
    je     69d9 <node315>
    cmp    rax,0x151
    je     6fef <node337>
    jmp    8e4d <fail_code>
0000000000003978 <node150>:
    lea    rax,[rip+0x7751]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5f
    inc    rbx
    lea    rdi,[rip+0x7683]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7638]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x17b
    je     7b0f <node379>
    cmp    rax,0x68
    je     2bac <node104>
    jmp    8e4d <fail_code>
00000000000039b7 <node151>:
    lea    rax,[rip+0x7712]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x57
    inc    rbx
    lea    rdi,[rip+0x7644]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x75f9]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x132
    je     6738 <node306>
    cmp    rax,0xb8
    je     42ee <node184>
    cmp    rax,0x4
    je     1286 <node4>
    cmp    rax,0xf0
    je     5374 <node240>
    cmp    rax,0x1bf
    je     8c19 <node447>
    cmp    rax,0x61
    je     2a5d <node97>
    cmp    rax,0x7
    je     134f <node7>
    cmp    rax,0x14b
    je     6e7f <node331>
    cmp    rax,0x7f
    je     324f <node127>
    cmp    rax,0x8f
    je     36f7 <node143>
    jmp    8e4d <fail_code>
0000000000003a50 <node152>:
    lea    rax,[rip+0x7679]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x50
    inc    rbx
    lea    rdi,[rip+0x75ab]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7560]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a5
    je     866d <node421>
    jmp    8e4d <fail_code>
0000000000003a85 <node153>:
    lea    rax,[rip+0x7644]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4c
    inc    rbx
    lea    rdi,[rip+0x7576]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x752b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x14e
    je     6f46 <node334>
    cmp    rax,0x185
    je     7d89 <node389>
    cmp    rax,0x80
    je     329a <node128>
    jmp    8e4d <fail_code>
0000000000003ad2 <node154>:
    lea    rax,[rip+0x75f7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x39
    inc    rbx
    lea    rdi,[rip+0x7529]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x74de]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xac
    je     3fc4 <node172>
    cmp    rax,0x66
    je     2b64 <node102>
    cmp    rax,0x6a
    je     2c48 <node106>
    cmp    rax,0x95
    je     3909 <node149>
    cmp    rax,0x155
    je     70e5 <node341>
    cmp    rax,0xc7
    je     471d <node199>
    cmp    rax,0x17f
    je     7c21 <node383>
    jmp    8e4d <fail_code>
0000000000003b4b <node155>:
    lea    rax,[rip+0x757e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x75
    inc    rbx
    lea    rdi,[rip+0x74b0]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7465]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x176
    je     79e8 <node374>
    cmp    rax,0x38
    je     2018 <node56>
    cmp    rax,0x162
    je     7434 <node354>
    cmp    rax,0x8e
    je     36ac <node142>
    cmp    rax,0x16
    je     179c <node22>
    cmp    rax,0x119
    je     609b <node281>
    cmp    rax,0x1a1
    je     8577 <node417>
    jmp    8e4d <fail_code>
0000000000003bc4 <node156>:
    lea    rax,[rip+0x7505]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x71
    inc    rbx
    lea    rdi,[rip+0x7437]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x73ec]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x198
    je     82f2 <node408>
    cmp    rax,0xe9
    je     515d <node233>
    jmp    8e4d <fail_code>
0000000000003c05 <node157>:
    lea    rax,[rip+0x74c4]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x59
    inc    rbx
    lea    rdi,[rip+0x73f6]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x73ab]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x13a
    je     69c6 <node314>
    cmp    rax,0x138
    je     6918 <node312>
    cmp    rax,0x9e
    je     3c7e <node158>
    cmp    rax,0xe2
    je     4fc0 <node226>
    cmp    rax,0x19b
    je     83ef <node411>
    cmp    rax,0x11b
    je     614d <node283>
    cmp    rax,0x199
    je     8327 <node409>
    jmp    8e4d <fail_code>
0000000000003c7e <node158>:
    lea    rax,[rip+0x744b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x73
    inc    rbx
    lea    rdi,[rip+0x737d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7332]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x3b
    je     2137 <node59>
    cmp    rax,0x17c
    je     7b4c <node380>
    cmp    rax,0x15d
    je     7335 <node349>
    jmp    8e4d <fail_code>
0000000000003cc9 <node159>:
    lea    rax,[rip+0x7400]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x49
    inc    rbx
    lea    rdi,[rip+0x7332]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x72e7]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x5f
    je     29f3 <node95>
    cmp    rax,0xcd
    je     4923 <node205>
    jmp    8e4d <fail_code>
0000000000003d08 <node160>:
    lea    rax,[rip+0x73c1]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    lea    rdi,[rip+0x72f3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x72a8]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x131
    je     66f7 <node305>
    cmp    rax,0x125
    je     6437 <node293>
    cmp    rax,0xce
    je     4958 <node206>
    jmp    8e4d <fail_code>
0000000000003d55 <node161>:
    lea    rax,[rip+0x7374]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x62
    inc    rbx
    jmp    8e4d <fail_code>
0000000000003d68 <node162>:
    lea    rax,[rip+0x7361]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x75
    inc    rbx
    jmp    8e4d <fail_code>
0000000000003d7b <node163>:
    lea    rax,[rip+0x734e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x55
    inc    rbx
    lea    rdi,[rip+0x7280]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7235]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xf8
    je     55f0 <node248>
    cmp    rax,0xec
    je     522a <node236>
    cmp    rax,0xae
    je     407e <node174>
    cmp    rax,0x162
    je     7434 <node354>
    cmp    rax,0xb7
    je     42b9 <node183>
    cmp    rax,0x187
    je     7e39 <node391>
    jmp    8e4d <fail_code>
0000000000003dec <node164>:
    lea    rax,[rip+0x72dd]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x56
    inc    rbx
    jmp    8e4d <fail_code>
0000000000003dff <node165>:
    lea    rax,[rip+0x72ca]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6a
    inc    rbx
    lea    rdi,[rip+0x71fc]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x71b1]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x81
    je     32ad <node129>
    cmp    rax,0x70
    je     2dd8 <node112>
    jmp    8e4d <fail_code>
0000000000003e3e <node166>:
    lea    rax,[rip+0x728b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x24
    inc    rbx
    lea    rdi,[rip+0x71bd]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7172]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x148
    je     6db0 <node328>
    cmp    rax,0x16
    je     179c <node22>
    cmp    rax,0xb3
    je     41bb <node179>
    cmp    rax,0xfe
    je     58a0 <node254>
    jmp    8e4d <fail_code>
0000000000003e95 <node167>:
    lea    rax,[rip+0x7234]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x33
    inc    rbx
    lea    rdi,[rip+0x7166]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x711b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x37
    je     2005 <node55>
    jmp    8e4d <fail_code>
0000000000003ec8 <node168>:
    lea    rax,[rip+0x7201]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x61
    inc    rbx
    lea    rdi,[rip+0x7133]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x70e8]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x98
    je     3a50 <node152>
    cmp    rax,0x2
    je     11d6 <node2>
    jmp    8e4d <fail_code>
0000000000003f07 <node169>:
    lea    rax,[rip+0x71c2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2f
    inc    rbx
    lea    rdi,[rip+0x70f4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x70a9]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x4a
    je     24f8 <node74>
    cmp    rax,0xb4
    je     4212 <node180>
    cmp    rax,0x128
    je     64ec <node296>
    cmp    rax,0x21
    je     1aad <node33>
    cmp    rax,0x1c0
    je     8c5a <node448>
    cmp    rax,0x37
    je     2005 <node55>
    cmp    rax,0x187
    je     7e39 <node391>
    jmp    8e4d <fail_code>
0000000000003f7e <node170>:
    lea    rax,[rip+0x714b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3d
    inc    rbx
    lea    rdi,[rip+0x707d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x7032]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x40
    je     227c <node64>
    jmp    8e4d <fail_code>
0000000000003fb1 <node171>:
    lea    rax,[rip+0x7118]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x40
    inc    rbx
    jmp    8e4d <fail_code>
0000000000003fc4 <node172>:
    lea    rax,[rip+0x7105]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x45
    inc    rbx
    lea    rdi,[rip+0x7037]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6fec]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1be
    je     8be4 <node446>
    cmp    rax,0x120
    je     62bc <node288>
    cmp    rax,0x53
    je     26f1 <node83>
    cmp    rax,0x194
    je     8232 <node404>
    jmp    8e4d <fail_code>
000000000000401b <node173>:
    lea    rax,[rip+0x70ae]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x63
    inc    rbx
    lea    rdi,[rip+0x6fe0]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6f95]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x116
    je     5f44 <node278>
    cmp    rax,0x170
    je     78e4 <node368>
    cmp    rax,0xc
    je     149c <node12>
    cmp    rax,0xec
    je     522a <node236>
    cmp    rax,0x162
    je     7434 <node354>
    jmp    8e4d <fail_code>
000000000000407e <node174>:
    lea    rax,[rip+0x704b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2c
    inc    rbx
    lea    rdi,[rip+0x6f7d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6f32]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xee
    je     52ac <node238>
    jmp    8e4d <fail_code>
00000000000040b3 <node175>:
    lea    rax,[rip+0x7016]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x68
    inc    rbx
    lea    rdi,[rip+0x6f48]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6efd]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x14
    je     1700 <node20>
    cmp    rax,0x91
    je     378d <node145>
    cmp    rax,0x193
    je     81c1 <node403>
    jmp    8e4d <fail_code>
00000000000040fe <node176>:
    lea    rax,[rip+0x6fcb]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x23
    inc    rbx
    lea    rdi,[rip+0x6efd]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6eb2]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x53
    je     26f1 <node83>
    cmp    rax,0x2d
    je     1da1 <node45>
    cmp    rax,0x1a7
    je     86c1 <node423>
    jmp    8e4d <fail_code>
0000000000004147 <node177>:
    lea    rax,[rip+0x6f82]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x38
    inc    rbx
    lea    rdi,[rip+0x6eb4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6e69]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a
    je     18b2 <node26>
    cmp    rax,0xa1
    je     3d55 <node161>
    jmp    8e4d <fail_code>
0000000000004186 <node178>:
    lea    rax,[rip+0x6f43]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    lea    rdi,[rip+0x6e75]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6e2a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xb9
    je     432d <node185>
    jmp    8e4d <fail_code>
00000000000041bb <node179>:
    lea    rax,[rip+0x6f0e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7e
    inc    rbx
    lea    rdi,[rip+0x6e40]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6df5]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a3
    je     861b <node419>
    cmp    rax,0x62
    je     2a92 <node98>
    cmp    rax,0x1b1
    je     8895 <node433>
    cmp    rax,0xa2
    je     3d68 <node162>
    jmp    8e4d <fail_code>
0000000000004212 <node180>:
    lea    rax,[rip+0x6eb7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4b
    inc    rbx
    lea    rdi,[rip+0x6de9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6d9e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x52
    je     26a4 <node82>
    jmp    8e4d <fail_code>
0000000000004245 <node181>:
    lea    rax,[rip+0x6e84]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x73
    inc    rbx
    lea    rdi,[rip+0x6db6]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6d6b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x5
    je     12cf <node5>
    jmp    8e4d <fail_code>
0000000000004278 <node182>:
    lea    rax,[rip+0x6e51]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xc
    inc    rbx
    lea    rdi,[rip+0x6d83]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6d38]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x170
    je     78e4 <node368>
    cmp    rax,0xaa
    je     3f7e <node170>
    jmp    8e4d <fail_code>
00000000000042b9 <node183>:
    lea    rax,[rip+0x6e10]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x26
    inc    rbx
    lea    rdi,[rip+0x6d42]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6cf7]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xbe
    je     4476 <node190>
    jmp    8e4d <fail_code>
00000000000042ee <node184>:
    lea    rax,[rip+0x6ddb]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    lea    rdi,[rip+0x6d0d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6cc2]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xff
    je     58d5 <node255>
    cmp    rax,0x35
    je     1f77 <node53>
    jmp    8e4d <fail_code>
000000000000432d <node185>:
    lea    rax,[rip+0x6d9c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7c
    inc    rbx
    jmp    8e4d <fail_code>
0000000000004340 <node186>:
    lea    rax,[rip+0x6d89]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x24
    inc    rbx
    lea    rdi,[rip+0x6cbb]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6c70]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x24
    je     1bc4 <node36>
    cmp    rax,0x186
    je     7de0 <node390>
    cmp    rax,0x88
    je     34ac <node136>
    cmp    rax,0x11
    je     1671 <node17>
    cmp    rax,0x177
    je     7a3f <node375>
    cmp    rax,0x1bd
    je     8b77 <node445>
    jmp    8e4d <fail_code>
00000000000043ad <node187>:
    lea    rax,[rip+0x6d1c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x21
    inc    rbx
    lea    rdi,[rip+0x6c4e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6c03]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xc6
    je     46be <node198>
    cmp    rax,0xf
    je     15a3 <node15>
    jmp    8e4d <fail_code>
00000000000043ec <node188>:
    lea    rax,[rip+0x6cdd]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x33
    inc    rbx
    lea    rdi,[rip+0x6c0f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6bc4]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x14e
    je     6f46 <node334>
    cmp    rax,0x19
    je     187f <node25>
    cmp    rax,0x41
    je     228f <node65>
    jmp    8e4d <fail_code>
0000000000004435 <node189>:
    lea    rax,[rip+0x6c94]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5b
    inc    rbx
    lea    rdi,[rip+0x6bc6]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6b7b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xa7
    je     3e95 <node167>
    cmp    rax,0x12f
    je     6631 <node303>
    jmp    8e4d <fail_code>
0000000000004476 <node190>:
    lea    rax,[rip+0x6c53]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4d
    inc    rbx
    lea    rdi,[rip+0x6b85]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6b3a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xa4
    je     3dec <node164>
    cmp    rax,0x175
    je     79d5 <node373>
    cmp    rax,0x8b
    je     35d1 <node139>
    jmp    8e4d <fail_code>
00000000000044c3 <node191>:
    lea    rax,[rip+0x6c06]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x53
    inc    rbx
    lea    rdi,[rip+0x6b38]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6aed]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x198
    je     82f2 <node408>
    cmp    rax,0x3d
    je     21e1 <node61>
    cmp    rax,0x4d
    je     25c3 <node77>
    cmp    rax,0x123
    je     63b9 <node291>
    jmp    8e4d <fail_code>
0000000000004518 <node192>:
    lea    rax,[rip+0x6bb1]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5a
    inc    rbx
    lea    rdi,[rip+0x6ae3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6a98]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x67
    je     2b99 <node103>
    jmp    8e4d <fail_code>
000000000000454b <node193>:
    lea    rax,[rip+0x6b7e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x46
    inc    rbx
    lea    rdi,[rip+0x6ab0]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6a65]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x150
    je     6fdc <node336>
    jmp    8e4d <fail_code>
0000000000004580 <node194>:
    lea    rax,[rip+0x6b49]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x60
    inc    rbx
    lea    rdi,[rip+0x6a7b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6a30]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x2a
    je     1d38 <node42>
    cmp    rax,0x15e
    je     736a <node350>
    jmp    8e4d <fail_code>
00000000000045bf <node195>:
    lea    rax,[rip+0x6b0a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x9
    inc    rbx
    lea    rdi,[rip+0x6a3c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x69f1]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xd6
    je     4c58 <node214>
    cmp    rax,0x19b
    je     83ef <node411>
    cmp    rax,0x161
    je     73e7 <node353>
    jmp    8e4d <fail_code>
000000000000460c <node196>:
    lea    rax,[rip+0x6abd]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x75
    inc    rbx
    lea    rdi,[rip+0x69ef]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x69a4]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x141
    je     6c1f <node321>
    cmp    rax,0x186
    je     7de0 <node390>
    cmp    rax,0x12c
    je     65ca <node300>
    jmp    8e4d <fail_code>
0000000000004659 <node197>:
    lea    rax,[rip+0x6a70]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5c
    inc    rbx
    lea    rdi,[rip+0x69a2]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6957]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x92
    je     381e <node146>
    cmp    rax,0x17f
    je     7c21 <node383>
    cmp    rax,0x1a9
    je     8727 <node425>
    cmp    rax,0x167
    je     7627 <node359>
    cmp    rax,0x16d
    je     7803 <node365>
    jmp    8e4d <fail_code>
00000000000046be <node198>:
    lea    rax,[rip+0x6a0b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6c
    inc    rbx
    lea    rdi,[rip+0x693d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x68f2]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x100
    je     5920 <node256>
    cmp    rax,0x60
    je     2a28 <node96>
    cmp    rax,0x39
    je     206f <node57>
    cmp    rax,0x2a
    je     1d38 <node42>
    cmp    rax,0x145
    je     6d57 <node325>
    jmp    8e4d <fail_code>
000000000000471d <node199>:
    lea    rax,[rip+0x69ac]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2e
    inc    rbx
    lea    rdi,[rip+0x68de]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6893]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x55
    je     2775 <node85>
    cmp    rax,0x108
    je     5ab0 <node264>
    jmp    8e4d <fail_code>
000000000000475c <node200>:
    lea    rax,[rip+0x696d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6c
    inc    rbx
    lea    rdi,[rip+0x689f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6854]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1c2
    je     8d4a <node450>
    cmp    rax,0x170
    je     78e4 <node368>
    cmp    rax,0x176
    je     79e8 <node374>
    cmp    rax,0x17c
    je     7b4c <node380>
    cmp    rax,0x9e
    je     3c7e <node158>
    cmp    rax,0x30
    je     1e30 <node48>
    cmp    rax,0x1c0
    je     8c5a <node448>
    cmp    rax,0x15f
    je     737d <node351>
    cmp    rax,0x41
    je     228f <node65>
    cmp    rax,0x67
    je     2b99 <node103>
    jmp    8e4d <fail_code>
00000000000047f7 <node201>:
    lea    rax,[rip+0x68d2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2c
    inc    rbx
    lea    rdi,[rip+0x6804]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x67b9]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x82
    je     32c0 <node130>
    cmp    rax,0x63
    je     2aa5 <node99>
    cmp    rax,0xc5
    je     4659 <node197>
    cmp    rax,0x16d
    je     7803 <node365>
    cmp    rax,0x99
    je     3a85 <node153>
    jmp    8e4d <fail_code>
000000000000485a <node202>:
    lea    rax,[rip+0x686f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x68
    inc    rbx
    lea    rdi,[rip+0x67a1]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6756]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1ae
    je     881a <node430>
    cmp    rax,0x105
    je     5a57 <node261>
    cmp    rax,0x1
    je     1195 <node1>
    jmp    8e4d <fail_code>
00000000000048a5 <node203>:
    lea    rax,[rip+0x6824]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x33
    inc    rbx
    lea    rdi,[rip+0x6756]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x670b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xc3
    je     45bf <node195>
    cmp    rax,0x17e
    je     7be0 <node382>
    jmp    8e4d <fail_code>
00000000000048e6 <node204>:
    lea    rax,[rip+0x67e3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    lea    rdi,[rip+0x6715]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x66ca]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x78
    je     3032 <node120>
    cmp    rax,0x3e
    je     2236 <node62>
    jmp    8e4d <fail_code>
0000000000004923 <node205>:
    lea    rax,[rip+0x67a6]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xa
    inc    rbx
    lea    rdi,[rip+0x66d8]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x668d]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x113
    je     5ed1 <node275>
    jmp    8e4d <fail_code>
0000000000004958 <node206>:
    lea    rax,[rip+0x6771]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2a
    inc    rbx
    lea    rdi,[rip+0x66a3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6658]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x114
    je     5ee4 <node276>
    cmp    rax,0x196
    je     82aa <node406>
    cmp    rax,0x178
    je     7a72 <node376>
    jmp    8e4d <fail_code>
00000000000049a5 <node207>:
    lea    rax,[rip+0x6724]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x35
    inc    rbx
    lea    rdi,[rip+0x6656]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x660b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xd9
    je     4d1b <node217>
    cmp    rax,0x3
    je     1221 <node3>
    cmp    rax,0x83
    je     3325 <node131>
    jmp    8e4d <fail_code>
00000000000049f0 <node208>:
    lea    rax,[rip+0x66d9]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x72
    inc    rbx
    lea    rdi,[rip+0x660b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x65c0]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x54
    je     2704 <node84>
    cmp    rax,0xc8
    je     475c <node200>
    cmp    rax,0x1b9
    je     8ab1 <node441>
    cmp    rax,0xef
    je     5303 <node239>
    cmp    rax,0xa9
    je     3f07 <node169>
    jmp    8e4d <fail_code>
0000000000004a53 <node209>:
    lea    rax,[rip+0x6676]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x43
    inc    rbx
    lea    rdi,[rip+0x65a8]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x655d]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x8c
    je     3606 <node140>
    cmp    rax,0x42
    je     22c4 <node66>
    cmp    rax,0xc4
    je     460c <node196>
    cmp    rax,0x116
    je     5f44 <node278>
    cmp    rax,0x8e
    je     36ac <node142>
    cmp    rax,0xae
    je     407e <node174>
    cmp    rax,0x1ab
    je     87b3 <node427>
    cmp    rax,0x1bf
    je     8c19 <node447>
    cmp    rax,0x14d
    je     6f05 <node333>
    cmp    rax,0x197
    je     82bd <node407>
    jmp    8e4d <fail_code>
0000000000004af2 <node210>:
    lea    rax,[rip+0x65d7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x79
    inc    rbx
    lea    rdi,[rip+0x6509]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x64be]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xa0
    je     3d08 <node160>
    cmp    rax,0x11a
    je     60f4 <node282>
    cmp    rax,0x4a
    je     24f8 <node74>
    cmp    rax,0x6b
    je     2c5b <node107>
    jmp    8e4d <fail_code>
0000000000004b47 <node211>:
    lea    rax,[rip+0x6582]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x33
    inc    rbx
    lea    rdi,[rip+0x64b4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6469]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x94
    je     38a6 <node148>
    cmp    rax,0x183
    je     7d0d <node387>
    cmp    rax,0x18
    je     1812 <node24>
    cmp    rax,0x18b
    je     7f59 <node395>
    cmp    rax,0x16b
    je     776d <node363>
    jmp    8e4d <fail_code>
0000000000004baa <node212>:
    lea    rax,[rip+0x651f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x34
    inc    rbx
    lea    rdi,[rip+0x6451]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6406]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x5e
    je     29e0 <node94>
    cmp    rax,0xe1
    je     4fad <node225>
    jmp    8e4d <fail_code>
0000000000004be9 <node213>:
    lea    rax,[rip+0x64e0]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x22
    inc    rbx
    lea    rdi,[rip+0x6412]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x63c7]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1b8
    je     8a42 <node440>
    cmp    rax,0x56
    je     27c2 <node86>
    cmp    rax,0x122
    je     6364 <node290>
    cmp    rax,0xf8
    je     55f0 <node248>
    cmp    rax,0xbb
    je     43ad <node187>
    cmp    rax,0x161
    je     73e7 <node353>
    jmp    8e4d <fail_code>
0000000000004c58 <node214>:
    lea    rax,[rip+0x6471]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x78
    inc    rbx
    lea    rdi,[rip+0x63a3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6358]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xb1
    je     4147 <node177>
    cmp    rax,0x1b5
    je     8997 <node437>
    cmp    rax,0x1b6
    je     89cc <node438>
    jmp    8e4d <fail_code>
0000000000004ca5 <node215>:
    lea    rax,[rip+0x6424]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x33
    inc    rbx
    lea    rdi,[rip+0x6356]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x630b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x196
    je     82aa <node406>
    jmp    8e4d <fail_code>
0000000000004cda <node216>:
    lea    rax,[rip+0x63ef]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x29
    inc    rbx
    lea    rdi,[rip+0x6321]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x62d6]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x14c
    je     6ed2 <node332>
    cmp    rax,0x12a
    je     6584 <node298>
    jmp    8e4d <fail_code>
0000000000004d1b <node217>:
    lea    rax,[rip+0x63ae]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x60
    inc    rbx
    lea    rdi,[rip+0x62e0]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6295]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1aa
    je     8768 <node426>
    cmp    rax,0x26
    je     1c4e <node38>
    cmp    rax,0xce
    je     4958 <node206>
    cmp    rax,0x45
    je     238f <node69>
    cmp    rax,0x13b
    je     69d9 <node315>
    jmp    8e4d <fail_code>
0000000000004d7c <node218>:
    lea    rax,[rip+0x634d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x67
    inc    rbx
    lea    rdi,[rip+0x627f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6234]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x150
    je     6fdc <node336>
    cmp    rax,0x2b
    je     1d4b <node43>
    jmp    8e4d <fail_code>
0000000000004dbb <node219>:
    lea    rax,[rip+0x630e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x52
    inc    rbx
    lea    rdi,[rip+0x6240]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x61f5]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x190
    je     811c <node400>
    cmp    rax,0xa6
    je     3e3e <node166>
    cmp    rax,0xa8
    je     3ec8 <node168>
    cmp    rax,0x164
    je     74ec <node356>
    cmp    rax,0x33
    je     1f03 <node51>
    cmp    rax,0x9
    je     13e9 <node9>
    cmp    rax,0x7b
    je     30fd <node123>
    jmp    8e4d <fail_code>
0000000000004e32 <node220>:
    lea    rax,[rip+0x6297]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6c
    inc    rbx
    lea    rdi,[rip+0x61c9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x617e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x97
    je     39b7 <node151>
    cmp    rax,0x4c
    je     2584 <node76>
    cmp    rax,0x93
    je     3851 <node147>
    jmp    8e4d <fail_code>
0000000000004e7d <node221>:
    lea    rax,[rip+0x624c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5e
    inc    rbx
    lea    rdi,[rip+0x617e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6133]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a8
    je     86f4 <node424>
    cmp    rax,0x196
    je     82aa <node406>
    jmp    8e4d <fail_code>
0000000000004ebe <node222>:
    lea    rax,[rip+0x620b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6f
    inc    rbx
    lea    rdi,[rip+0x613d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x60f2]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x106
    je     5a8a <node262>
    jmp    8e4d <fail_code>
0000000000004ef3 <node223>:
    lea    rax,[rip+0x61d6]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6c
    inc    rbx
    lea    rdi,[rip+0x6108]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x60bd]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x15c
    je     72c6 <node348>
    cmp    rax,0xcb
    je     48a5 <node203>
    cmp    rax,0x1c3
    je     8d5d <node451>
    jmp    8e4d <fail_code>
0000000000004f40 <node224>:
    lea    rax,[rip+0x6189]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3f
    inc    rbx
    lea    rdi,[rip+0x60bb]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x6070]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xea
    je     5170 <node234>
    cmp    rax,0x120
    je     62bc <node288>
    cmp    rax,0xd2
    je     4af2 <node210>
    cmp    rax,0xc5
    je     4659 <node197>
    cmp    rax,0x1bd
    je     8b77 <node445>
    cmp    rax,0xe3
    je     5009 <node227>
    jmp    8e4d <fail_code>
0000000000004fad <node225>:
    lea    rax,[rip+0x611c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3b
    inc    rbx
    jmp    8e4d <fail_code>
0000000000004fc0 <node226>:
    lea    rax,[rip+0x6109]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x67
    inc    rbx
    lea    rdi,[rip+0x603b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5ff0]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x2f
    je     1dfb <node47>
    cmp    rax,0x151
    je     6fef <node337>
    cmp    rax,0x3f
    je     2269 <node63>
    jmp    8e4d <fail_code>
0000000000005009 <node227>:
    lea    rax,[rip+0x60c0]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3d
    inc    rbx
    jmp    8e4d <fail_code>
000000000000501c <node228>:
    lea    rax,[rip+0x60ad]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5b
    inc    rbx
    lea    rdi,[rip+0x5fdf]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5f94]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x126
    je     644a <node294>
    cmp    rax,0x19c
    je     8446 <node412>
    cmp    rax,0x24
    je     1bc4 <node36>
    cmp    rax,0xe7
    je     5117 <node231>
    cmp    rax,0xb5
    je     4245 <node181>
    cmp    rax,0xbf
    je     44c3 <node191>
    jmp    8e4d <fail_code>
000000000000508b <node229>:
    lea    rax,[rip+0x603e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x58
    inc    rbx
    lea    rdi,[rip+0x5f70]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5f25]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x17a
    je     7ad2 <node378>
    cmp    rax,0x25
    je     1c03 <node37>
    cmp    rax,0x167
    je     7627 <node359>
    jmp    8e4d <fail_code>
00000000000050d6 <node230>:
    lea    rax,[rip+0x5ff3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x38
    inc    rbx
    lea    rdi,[rip+0x5f25]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5eda]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1b0
    je     8882 <node432>
    cmp    rax,0x1c2
    je     8d4a <node450>
    jmp    8e4d <fail_code>
0000000000005117 <node231>:
    lea    rax,[rip+0x5fb2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x49
    inc    rbx
    lea    rdi,[rip+0x5ee4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5e99]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x13
    je     16cd <node19>
    jmp    8e4d <fail_code>
000000000000514a <node232>:
    lea    rax,[rip+0x5f7f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x79
    inc    rbx
    jmp    8e4d <fail_code>
000000000000515d <node233>:
    lea    rax,[rip+0x5f6c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4e
    inc    rbx
    jmp    8e4d <fail_code>
0000000000005170 <node234>:
    lea    rax,[rip+0x5f59]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x34
    inc    rbx
    lea    rdi,[rip+0x5e8b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5e40]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xd4
    je     4baa <node212>
    cmp    rax,0x9f
    je     3cc9 <node159>
    cmp    rax,0x17f
    je     7c21 <node383>
    jmp    8e4d <fail_code>
00000000000051bd <node235>:
    lea    rax,[rip+0x5f0c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x67
    inc    rbx
    lea    rdi,[rip+0x5e3e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5df3]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x42
    je     22c4 <node66>
    cmp    rax,0x1c4
    je     8dbe <node452>
    cmp    rax,0x9e
    je     3c7e <node158>
    cmp    rax,0x11e
    je     620c <node286>
    cmp    rax,0x6f
    je     2d81 <node111>
    cmp    rax,0x1a7
    je     86c1 <node423>
    jmp    8e4d <fail_code>
000000000000522a <node236>:
    lea    rax,[rip+0x5e9f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x29
    inc    rbx
    lea    rdi,[rip+0x5dd1]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5d86]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x110
    je     5d70 <node272>
    cmp    rax,0x146
    je     6d6a <node326>
    cmp    rax,0x1b1
    je     8895 <node433>
    jmp    8e4d <fail_code>
0000000000005277 <node237>:
    lea    rax,[rip+0x5e52]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2f
    inc    rbx
    lea    rdi,[rip+0x5d84]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5d39]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1b6
    je     89cc <node438>
    jmp    8e4d <fail_code>
00000000000052ac <node238>:
    lea    rax,[rip+0x5e1d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    lea    rdi,[rip+0x5d4f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5d04]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xc1
    je     454b <node193>
    cmp    rax,0x194
    je     8232 <node404>
    cmp    rax,0xb
    je     1489 <node11>
    cmp    rax,0x1a7
    je     86c1 <node423>
    jmp    8e4d <fail_code>
0000000000005303 <node239>:
    lea    rax,[rip+0x5dc6]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x75
    inc    rbx
    lea    rdi,[rip+0x5cf8]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5cad]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x108
    je     5ab0 <node264>
    cmp    rax,0x100
    je     5920 <node256>
    cmp    rax,0x144
    je     6d22 <node324>
    cmp    rax,0x111
    je     5daf <node273>
    cmp    rax,0xb1
    je     4147 <node177>
    cmp    rax,0x131
    je     66f7 <node305>
    jmp    8e4d <fail_code>
0000000000005374 <node240>:
    lea    rax,[rip+0x5d55]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x26
    inc    rbx
    lea    rdi,[rip+0x5c87]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5c3c]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe9
    je     515d <node233>
    cmp    rax,0x33
    je     1f03 <node51>
    jmp    8e4d <fail_code>
00000000000053b3 <node241>:
    lea    rax,[rip+0x5d16]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6c
    inc    rbx
    lea    rdi,[rip+0x5c48]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5bfd]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xd4
    je     4baa <node212>
    cmp    rax,0x113
    je     5ed1 <node275>
    jmp    8e4d <fail_code>
00000000000053f4 <node242>:
    lea    rax,[rip+0x5cd5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2b
    inc    rbx
    lea    rdi,[rip+0x5c07]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5bbc]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xea
    je     5170 <node234>
    cmp    rax,0xa6
    je     3e3e <node166>
    cmp    rax,0xc
    je     149c <node12>
    cmp    rax,0x182
    je     7cfa <node386>
    cmp    rax,0x128
    je     64ec <node296>
    cmp    rax,0x157
    je     7165 <node343>
    cmp    rax,0x153
    je     706f <node339>
    cmp    rax,0x15b
    je     72b3 <node347>
    cmp    rax,0x75
    je     2f6b <node117>
    cmp    rax,0x14b
    je     6e7f <node331>
    jmp    8e4d <fail_code>
0000000000005491 <node243>:
    lea    rax,[rip+0x5c38]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x58
    inc    rbx
    lea    rdi,[rip+0x5b6a]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5b1f]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x24
    je     1bc4 <node36>
    cmp    rax,0xe6
    je     50d6 <node230>
    cmp    rax,0x5
    je     12cf <node5>
    cmp    rax,0x1b2
    je     88d4 <node434>
    cmp    rax,0x10d
    je     5c77 <node269>
    jmp    8e4d <fail_code>
00000000000054f2 <node244>:
    lea    rax,[rip+0x5bd7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x23
    inc    rbx
    lea    rdi,[rip+0x5b09]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5abe]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x80
    je     329a <node128>
    jmp    8e4d <fail_code>
0000000000005527 <node245>:
    lea    rax,[rip+0x5ba2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5f
    inc    rbx
    lea    rdi,[rip+0x5ad4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5a89]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x14f
    je     6f85 <node335>
    cmp    rax,0x20
    je     1a06 <node32>
    cmp    rax,0x8a
    je     3558 <node138>
    cmp    rax,0x115
    je     5ef7 <node277>
    jmp    8e4d <fail_code>
000000000000557e <node246>:
    lea    rax,[rip+0x5b4b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    lea    rdi,[rip+0x5a7d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5a32]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x15f
    je     737d <node351>
    jmp    8e4d <fail_code>
00000000000055b3 <node247>:
    lea    rax,[rip+0x5b16]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x27
    inc    rbx
    lea    rdi,[rip+0x5a48]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x59fd]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x6c
    je     2cb2 <node108>
    cmp    rax,0x11
    je     1671 <node17>
    jmp    8e4d <fail_code>
00000000000055f0 <node248>:
    lea    rax,[rip+0x5ad9]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4c
    inc    rbx
    lea    rdi,[rip+0x5a0b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x59c0]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xb0
    je     40fe <node176>
    cmp    rax,0x1a9
    je     8727 <node425>
    cmp    rax,0x1b5
    je     8997 <node437>
    jmp    8e4d <fail_code>
000000000000563d <node249>:
    lea    rax,[rip+0x5a8c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x65
    inc    rbx
    lea    rdi,[rip+0x59be]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5973]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x7e
    je     31f6 <node126>
    cmp    rax,0x62
    je     2a92 <node98>
    cmp    rax,0x156
    je     7126 <node342>
    cmp    rax,0xf0
    je     5374 <node240>
    cmp    rax,0xc4
    je     460c <node196>
    cmp    rax,0x126
    je     644a <node294>
    cmp    rax,0x48
    je     2442 <node72>
    cmp    rax,0x11
    je     1671 <node17>
    cmp    rax,0x45
    je     238f <node69>
    cmp    rax,0x22
    je     1ae0 <node34>
    jmp    8e4d <fail_code>
00000000000056d2 <node250>:
    lea    rax,[rip+0x59f7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x74
    inc    rbx
    lea    rdi,[rip+0x5929]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x58de]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x13a
    je     69c6 <node314>
    cmp    rax,0x17
    je     17d1 <node23>
    cmp    rax,0x164
    je     74ec <node356>
    cmp    rax,0x38
    je     2018 <node56>
    cmp    rax,0xf3
    je     5491 <node243>
    cmp    rax,0x179
    je     7a85 <node377>
    jmp    8e4d <fail_code>
000000000000573f <node251>:
    lea    rax,[rip+0x598a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x39
    inc    rbx
    lea    rdi,[rip+0x58bc]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5871]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xea
    je     5170 <node234>
    cmp    rax,0x1c2
    je     8d4a <node450>
    cmp    rax,0x7e
    je     31f6 <node126>
    cmp    rax,0x72
    je     2e2a <node114>
    cmp    rax,0x1b0
    je     8882 <node432>
    cmp    rax,0x160
    je     7390 <node352>
    cmp    rax,0xda
    je     4d7c <node218>
    cmp    rax,0x49
    je     2499 <node73>
    cmp    rax,0x125
    je     6437 <node293>
    cmp    rax,0x111
    je     5daf <node273>
    cmp    rax,0xa1
    je     3d55 <node161>
    cmp    rax,0x135
    je     682d <node309>
    cmp    rax,0x12d
    je     660b <node301>
    jmp    8e4d <fail_code>
00000000000057fe <node252>:
    lea    rax,[rip+0x58cb]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x33
    inc    rbx
    lea    rdi,[rip+0x57fd]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x57b2]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xec
    je     522a <node236>
    cmp    rax,0x110
    je     5d70 <node272>
    cmp    rax,0x12c
    je     65ca <node300>
    cmp    rax,0x157
    je     7165 <node343>
    cmp    rax,0xff
    je     58d5 <node255>
    jmp    8e4d <fail_code>
000000000000585f <node253>:
    lea    rax,[rip+0x586a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x56
    inc    rbx
    lea    rdi,[rip+0x579c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5751]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xb9
    je     432d <node185>
    cmp    rax,0x175
    je     79d5 <node373>
    jmp    8e4d <fail_code>
00000000000058a0 <node254>:
    lea    rax,[rip+0x5829]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x42
    inc    rbx
    lea    rdi,[rip+0x575b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5710]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1b3
    je     8915 <node435>
    jmp    8e4d <fail_code>
00000000000058d5 <node255>:
    lea    rax,[rip+0x57f4]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4e
    inc    rbx
    lea    rdi,[rip+0x5726]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x56db]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x10b
    je     5be3 <node267>
    cmp    rax,0x1
    je     1195 <node1>
    cmp    rax,0xa2
    je     3d68 <node162>
    jmp    8e4d <fail_code>
0000000000005920 <node256>:
    lea    rax,[rip+0x57a9]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3d
    inc    rbx
    jmp    8e4d <fail_code>
0000000000005933 <node257>:
    lea    rax,[rip+0x5796]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x64
    inc    rbx
    jmp    8e4d <fail_code>
0000000000005946 <node258>:
    lea    rax,[rip+0x5783]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x78
    inc    rbx
    lea    rdi,[rip+0x56b5]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x566a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x15a
    je     7276 <node346>
    cmp    rax,0x101
    je     5933 <node257>
    cmp    rax,0xb7
    je     42b9 <node183>
    cmp    rax,0x16e
    je     785c <node366>
    jmp    8e4d <fail_code>
000000000000599b <node259>:
    lea    rax,[rip+0x572e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2e
    inc    rbx
    lea    rdi,[rip+0x5660]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5615]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x4
    je     1286 <node4>
    cmp    rax,0x1be
    je     8be4 <node446>
    cmp    rax,0x138
    je     6918 <node312>
    cmp    rax,0x141
    je     6c1f <node321>
    cmp    rax,0xa7
    je     3e95 <node167>
    cmp    rax,0x18f
    je     80c9 <node399>
    cmp    rax,0x135
    je     682d <node309>
    jmp    8e4d <fail_code>
0000000000005a16 <node260>:
    lea    rax,[rip+0x56b3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    lea    rdi,[rip+0x55e5]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x559a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x102
    je     5946 <node258>
    cmp    rax,0xaf
    je     40b3 <node175>
    jmp    8e4d <fail_code>
0000000000005a57 <node261>:
    lea    rax,[rip+0x5672]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    lea    rdi,[rip+0x55a4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5559]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe
    je     1590 <node14>
    jmp    8e4d <fail_code>
0000000000005a8a <node262>:
    lea    rax,[rip+0x563f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x56
    inc    rbx
    jmp    8e4d <fail_code>
0000000000005a9d <node263>:
    lea    rax,[rip+0x562c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x38
    inc    rbx
    jmp    8e4d <fail_code>
0000000000005ab0 <node264>:
    lea    rax,[rip+0x5619]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7a
    inc    rbx
    lea    rdi,[rip+0x554b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5500]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x19f
    je     8525 <node415>
    cmp    rax,0x192
    je     81ae <node402>
    jmp    8e4d <fail_code>
0000000000005af1 <node265>:
    lea    rax,[rip+0x55d8]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x72
    inc    rbx
    lea    rdi,[rip+0x550a]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x54bf]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe0
    je     4f40 <node224>
    cmp    rax,0xeb
    je     51bd <node235>
    cmp    rax,0x44
    je     2342 <node68>
    cmp    rax,0xc9
    je     47f7 <node201>
    jmp    8e4d <fail_code>
0000000000005b48 <node266>:
    lea    rax,[rip+0x5581]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x73
    inc    rbx
    lea    rdi,[rip+0x54b3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5468]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x120
    je     62bc <node288>
    cmp    rax,0x124
    je     6404 <node292>
    cmp    rax,0x38
    je     2018 <node56>
    cmp    rax,0x148
    je     6db0 <node328>
    cmp    rax,0x12e
    je     661e <node302>
    cmp    rax,0x18a
    je     7f1a <node394>
    cmp    rax,0x106
    je     5a8a <node262>
    cmp    rax,0xac
    je     3fc4 <node172>
    cmp    rax,0x10c
    je     5c16 <node268>
    cmp    rax,0x195
    je     8245 <node405>
    jmp    8e4d <fail_code>
0000000000005be3 <node267>:
    lea    rax,[rip+0x54e6]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4e
    inc    rbx
    lea    rdi,[rip+0x5418]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x53cd]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x43
    je     232f <node67>
    jmp    8e4d <fail_code>
0000000000005c16 <node268>:
    lea    rax,[rip+0x54b3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4a
    inc    rbx
    lea    rdi,[rip+0x53e5]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x539a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x19e
    je     84e6 <node414>
    cmp    rax,0xc0
    je     4518 <node192>
    cmp    rax,0xb2
    je     4186 <node178>
    cmp    rax,0x37
    je     2005 <node55>
    cmp    rax,0x75
    je     2f6b <node117>
    jmp    8e4d <fail_code>
0000000000005c77 <node269>:
    lea    rax,[rip+0x5452]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4c
    inc    rbx
    lea    rdi,[rip+0x5384]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5339]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x12a
    je     6584 <node298>
    cmp    rax,0x156
    je     7126 <node342>
    cmp    rax,0xfd
    je     585f <node253>
    jmp    8e4d <fail_code>
0000000000005cc4 <node270>:
    lea    rax,[rip+0x5405]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x61
    inc    rbx
    lea    rdi,[rip+0x5337]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x52ec]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x47
    je     242f <node71>
    cmp    rax,0x19f
    je     8525 <node415>
    cmp    rax,0x28
    je     1ce4 <node40>
    jmp    8e4d <fail_code>
0000000000005d0d <node271>:
    lea    rax,[rip+0x53bc]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x72
    inc    rbx
    lea    rdi,[rip+0x52ee]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x52a3]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x186
    je     7de0 <node390>
    cmp    rax,0xc5
    je     4659 <node197>
    cmp    rax,0x165
    je     7541 <node357>
    cmp    rax,0x3d
    je     21e1 <node61>
    cmp    rax,0x1b1
    je     8895 <node433>
    jmp    8e4d <fail_code>
0000000000005d70 <node272>:
    lea    rax,[rip+0x5359]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6f
    inc    rbx
    lea    rdi,[rip+0x528b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5240]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x108
    je     5ab0 <node264>
    cmp    rax,0x67
    je     2b99 <node103>
    jmp    8e4d <fail_code>
0000000000005daf <node273>:
    lea    rax,[rip+0x531a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xa
    inc    rbx
    lea    rdi,[rip+0x524c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5201]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x8
    je     13a8 <node8>
    cmp    rax,0x174
    je     79c2 <node372>
    cmp    rax,0x12e
    je     661e <node302>
    cmp    rax,0xbe
    je     4476 <node190>
    cmp    rax,0x58
    je     286e <node88>
    cmp    rax,0x125
    je     6437 <node293>
    cmp    rax,0x139
    je     696f <node313>
    cmp    rax,0xb9
    je     432d <node185>
    cmp    rax,0x137
    je     68cb <node311>
    cmp    rax,0x1af
    je     882d <node431>
    cmp    rax,0x10d
    je     5c77 <node269>
    jmp    8e4d <fail_code>
0000000000005e58 <node274>:
    lea    rax,[rip+0x5271]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6b
    inc    rbx
    lea    rdi,[rip+0x51a3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5158]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x132
    je     6738 <node306>
    cmp    rax,0x48
    je     2442 <node72>
    cmp    rax,0x174
    je     79c2 <node372>
    cmp    rax,0xce
    je     4958 <node206>
    cmp    rax,0x138
    je     6918 <node312>
    cmp    rax,0x6f
    je     2d81 <node111>
    cmp    rax,0xf3
    je     5491 <node243>
    jmp    8e4d <fail_code>
0000000000005ed1 <node275>:
    lea    rax,[rip+0x51f8]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7c
    inc    rbx
    jmp    8e4d <fail_code>
0000000000005ee4 <node276>:
    lea    rax,[rip+0x51e5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3e
    inc    rbx
    jmp    8e4d <fail_code>
0000000000005ef7 <node277>:
    lea    rax,[rip+0x51d2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x34
    inc    rbx
    lea    rdi,[rip+0x5104]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x50b9]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xa3
    je     3d7b <node163>
    cmp    rax,0xd1
    je     4a53 <node209>
    cmp    rax,0x18d
    je     8037 <node397>
    jmp    8e4d <fail_code>
0000000000005f44 <node278>:
    lea    rax,[rip+0x5185]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6d
    inc    rbx
    lea    rdi,[rip+0x50b7]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x506c]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x3d
    je     21e1 <node61>
    cmp    rax,0x1c5
    je     8dce <node453>
    cmp    rax,0xe3
    je     5009 <node227>
    jmp    8e4d <fail_code>
0000000000005f8f <node279>:
    lea    rax,[rip+0x513a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5b
    inc    rbx
    lea    rdi,[rip+0x506c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x5021]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x24
    je     1bc4 <node36>
    cmp    rax,0x17
    je     17d1 <node23>
    cmp    rax,0x51
    je     266f <node81>
    cmp    rax,0xed
    je     5277 <node237>
    cmp    rax,0x55
    je     2775 <node85>
    cmp    rax,0x22
    je     1ae0 <node34>
    jmp    8e4d <fail_code>
0000000000005ff6 <node280>:
    lea    rax,[rip+0x50d3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x26
    inc    rbx
    lea    rdi,[rip+0x5005]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4fba]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1b2
    je     88d4 <node434>
    cmp    rax,0x1ac
    je     87f4 <node428>
    cmp    rax,0x178
    je     7a72 <node376>
    cmp    rax,0x138
    je     6918 <node312>
    cmp    rax,0x161
    je     73e7 <node353>
    cmp    rax,0x119
    je     609b <node281>
    cmp    rax,0x149
    je     6de5 <node329>
    cmp    rax,0x12
    je     1684 <node18>
    cmp    rax,0x129
    je     654f <node297>
    cmp    rax,0x1b5
    je     8997 <node437>
    cmp    rax,0x5b
    je     28c9 <node91>
    jmp    8e4d <fail_code>
000000000000609b <node281>:
    lea    rax,[rip+0x502e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7a
    inc    rbx
    lea    rdi,[rip+0x4f60]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4f15]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xd7
    je     4ca5 <node215>
    cmp    rax,0x17a
    je     7ad2 <node378>
    cmp    rax,0xa4
    je     3dec <node164>
    cmp    rax,0x1bd
    je     8b77 <node445>
    jmp    8e4d <fail_code>
00000000000060f4 <node282>:
    lea    rax,[rip+0x4fd5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2c
    inc    rbx
    lea    rdi,[rip+0x4f07]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4ebc]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x178
    je     7a72 <node376>
    cmp    rax,0x1be
    je     8be4 <node446>
    cmp    rax,0x8b
    je     35d1 <node139>
    cmp    rax,0x1ac
    je     87f4 <node428>
    jmp    8e4d <fail_code>
000000000000614d <node283>:
    lea    rax,[rip+0x4f7c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x37
    inc    rbx
    lea    rdi,[rip+0x4eae]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4e63]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xed
    je     5277 <node237>
    cmp    rax,0x13e
    je     6adc <node318>
    jmp    8e4d <fail_code>
000000000000618e <node284>:
    lea    rax,[rip+0x4f3b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x38
    inc    rbx
    lea    rdi,[rip+0x4e6d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4e22]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x84
    je     3394 <node132>
    cmp    rax,0x30
    je     1e30 <node48>
    jmp    8e4d <fail_code>
00000000000061cd <node285>:
    lea    rax,[rip+0x4efc]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x77
    inc    rbx
    lea    rdi,[rip+0x4e2e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4de3]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1c4
    je     8dbe <node452>
    cmp    rax,0x2d
    je     1da1 <node45>
    jmp    8e4d <fail_code>
000000000000620c <node286>:
    lea    rax,[rip+0x4ebd]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x43
    inc    rbx
    lea    rdi,[rip+0x4def]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4da4]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x2c
    je     1d5e <node44>
    cmp    rax,0x120
    je     62bc <node288>
    cmp    rax,0x7a
    je     30b2 <node122>
    cmp    rax,0x58
    je     286e <node88>
    cmp    rax,0x146
    je     6d6a <node326>
    cmp    rax,0x1bb
    je     8b0d <node443>
    cmp    rax,0x12b
    je     65b7 <node299>
    cmp    rax,0x9
    je     13e9 <node9>
    jmp    8e4d <fail_code>
0000000000006289 <node287>:
    lea    rax,[rip+0x4e40]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x78
    inc    rbx
    lea    rdi,[rip+0x4d72]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4d27]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x76
    je     2f9e <node118>
    jmp    8e4d <fail_code>
00000000000062bc <node288>:
    lea    rax,[rip+0x4e0d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    lea    rdi,[rip+0x4d3f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4cf4]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xf4
    je     54f2 <node244>
    cmp    rax,0x29
    je     1cf7 <node41>
    cmp    rax,0x4e
    je     25d6 <node78>
    cmp    rax,0x108
    je     5ab0 <node264>
    jmp    8e4d <fail_code>
0000000000006311 <node289>:
    lea    rax,[rip+0x4db8]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6b
    inc    rbx
    lea    rdi,[rip+0x4cea]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4c9f]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x2b
    je     1d4b <node43>
    cmp    rax,0x145
    je     6d57 <node325>
    cmp    rax,0x62
    je     2a92 <node98>
    cmp    rax,0x1a
    je     18b2 <node26>
    jmp    8e4d <fail_code>
0000000000006364 <node290>:
    lea    rax,[rip+0x4d65]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3a
    inc    rbx
    lea    rdi,[rip+0x4c97]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4c4c]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x17
    je     17d1 <node23>
    cmp    rax,0x107
    je     5a9d <node263>
    cmp    rax,0x6
    je     1304 <node6>
    cmp    rax,0x189
    je     7ecf <node393>
    jmp    8e4d <fail_code>
00000000000063b9 <node291>:
    lea    rax,[rip+0x4d10]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x33
    inc    rbx
    lea    rdi,[rip+0x4c42]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4bf7]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x149
    je     6de5 <node329>
    cmp    rax,0x58
    je     286e <node88>
    cmp    rax,0x16f
    je     789b <node367>
    jmp    8e4d <fail_code>
0000000000006404 <node292>:
    lea    rax,[rip+0x4cc5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x77
    inc    rbx
    lea    rdi,[rip+0x4bf7]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4bac]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x22
    je     1ae0 <node34>
    jmp    8e4d <fail_code>
0000000000006437 <node293>:
    lea    rax,[rip+0x4c92]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x40
    inc    rbx
    jmp    8e4d <fail_code>
000000000000644a <node294>:
    lea    rax,[rip+0x4c7f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x47
    inc    rbx
    lea    rdi,[rip+0x4bb1]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4b66]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x189
    je     7ecf <node393>
    cmp    rax,0x78
    je     3032 <node120>
    cmp    rax,0x2f
    je     1dfb <node47>
    cmp    rax,0xbd
    je     4435 <node189>
    jmp    8e4d <fail_code>
000000000000649f <node295>:
    lea    rax,[rip+0x4c2a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3c
    inc    rbx
    lea    rdi,[rip+0x4b5c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4b11]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x15f
    je     737d <node351>
    cmp    rax,0x19f
    je     8525 <node415>
    cmp    rax,0x179
    je     7a85 <node377>
    jmp    8e4d <fail_code>
00000000000064ec <node296>:
    lea    rax,[rip+0x4bdd]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2f
    inc    rbx
    lea    rdi,[rip+0x4b0f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4ac4]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xd6
    je     4c58 <node214>
    cmp    rax,0x182
    je     7cfa <node386>
    cmp    rax,0x1b6
    je     89cc <node438>
    cmp    rax,0xb5
    je     4245 <node181>
    cmp    rax,0x53
    je     26f1 <node83>
    jmp    8e4d <fail_code>
000000000000654f <node297>:
    lea    rax,[rip+0x4b7a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x34
    inc    rbx
    lea    rdi,[rip+0x4aac]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4a61]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xfe
    je     58a0 <node254>
    jmp    8e4d <fail_code>
0000000000006584 <node298>:
    lea    rax,[rip+0x4b45]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4e
    inc    rbx
    lea    rdi,[rip+0x4a77]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4a2c]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x47
    je     242f <node71>
    jmp    8e4d <fail_code>
00000000000065b7 <node299>:
    lea    rax,[rip+0x4b12]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7c
    inc    rbx
    jmp    8e4d <fail_code>
00000000000065ca <node300>:
    lea    rax,[rip+0x4aff]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xc
    inc    rbx
    lea    rdi,[rip+0x4a31]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x49e6]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a0
    je     8538 <node416>
    cmp    rax,0x105
    je     5a57 <node261>
    jmp    8e4d <fail_code>
000000000000660b <node301>:
    lea    rax,[rip+0x4abe]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x54
    inc    rbx
    jmp    8e4d <fail_code>
000000000000661e <node302>:
    lea    rax,[rip+0x4aab]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    jmp    8e4d <fail_code>
0000000000006631 <node303>:
    lea    rax,[rip+0x4a98]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x79
    inc    rbx
    lea    rdi,[rip+0x49ca]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x497f]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1b0
    je     8882 <node432>
    cmp    rax,0xab
    je     3fb1 <node171>
    jmp    8e4d <fail_code>
0000000000006672 <node304>:
    lea    rax,[rip+0x4a57]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x42
    inc    rbx
    lea    rdi,[rip+0x4989]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x493e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x196
    je     82aa <node406>
    cmp    rax,0x38
    je     2018 <node56>
    cmp    rax,0x144
    je     6d22 <node324>
    cmp    rax,0x52
    je     26a4 <node82>
    cmp    rax,0xbe
    je     4476 <node190>
    cmp    rax,0x123
    je     63b9 <node291>
    cmp    rax,0x19f
    je     8525 <node415>
    cmp    rax,0xbd
    je     4435 <node189>
    jmp    8e4d <fail_code>
00000000000066f7 <node305>:
    lea    rax,[rip+0x49d2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x61
    inc    rbx
    lea    rdi,[rip+0x4904]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x48b9]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x84
    je     3394 <node132>
    cmp    rax,0x100
    je     5920 <node256>
    jmp    8e4d <fail_code>
0000000000006738 <node306>:
    lea    rax,[rip+0x4991]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2b
    inc    rbx
    lea    rdi,[rip+0x48c3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4878]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1ba
    je     8afa <node442>
    cmp    rax,0x7a
    je     30b2 <node122>
    cmp    rax,0xd8
    je     4cda <node216>
    cmp    rax,0x4a
    je     24f8 <node74>
    jmp    8e4d <fail_code>
000000000000678d <node307>:
    lea    rax,[rip+0x493c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x78
    inc    rbx
    lea    rdi,[rip+0x486e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4823]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x124
    je     6404 <node292>
    cmp    rax,0x156
    je     7126 <node342>
    cmp    rax,0x132
    je     6738 <node306>
    cmp    rax,0x72
    je     2e2a <node114>
    cmp    rax,0x1af
    je     882d <node431>
    cmp    rax,0x3b
    je     2137 <node59>
    jmp    8e4d <fail_code>
00000000000067fa <node308>:
    lea    rax,[rip+0x48cf]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xb
    inc    rbx
    lea    rdi,[rip+0x4801]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x47b6]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1d
    je     196b <node29>
    jmp    8e4d <fail_code>
000000000000682d <node309>:
    lea    rax,[rip+0x489c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x67
    inc    rbx
    lea    rdi,[rip+0x47ce]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4783]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x172
    je     797a <node370>
    cmp    rax,0x64
    je     2af2 <node100>
    cmp    rax,0x17
    je     17d1 <node23>
    cmp    rax,0xdd
    je     4e7d <node221>
    cmp    rax,0x2f
    je     1dfb <node47>
    jmp    8e4d <fail_code>
000000000000688c <node310>:
    lea    rax,[rip+0x483d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xb
    inc    rbx
    lea    rdi,[rip+0x476f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4724]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xa4
    je     3dec <node164>
    cmp    rax,0x11
    je     1671 <node17>
    jmp    8e4d <fail_code>
00000000000068cb <node311>:
    lea    rax,[rip+0x47fe]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3a
    inc    rbx
    lea    rdi,[rip+0x4730]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x46e5]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a6
    je     8680 <node422>
    cmp    rax,0x1a0
    je     8538 <node416>
    cmp    rax,0x1bc
    je     8b42 <node444>
    jmp    8e4d <fail_code>
0000000000006918 <node312>:
    lea    rax,[rip+0x47b1]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5d
    inc    rbx
    lea    rdi,[rip+0x46e3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4698]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x24
    je     1bc4 <node36>
    cmp    rax,0x16e
    je     785c <node366>
    cmp    rax,0xcd
    je     4923 <node205>
    cmp    rax,0x1c2
    je     8d4a <node450>
    jmp    8e4d <fail_code>
000000000000696f <node313>:
    lea    rax,[rip+0x475a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    lea    rdi,[rip+0x468c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4641]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x2b
    je     1d4b <node43>
    cmp    rax,0x136
    je     688c <node310>
    cmp    rax,0x147
    je     6d9d <node327>
    cmp    rax,0x184
    je     7d56 <node388>
    jmp    8e4d <fail_code>
00000000000069c6 <node314>:
    lea    rax,[rip+0x4703]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x49
    inc    rbx
    jmp    8e4d <fail_code>
00000000000069d9 <node315>:
    lea    rax,[rip+0x46f0]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x38
    inc    rbx
    lea    rdi,[rip+0x4622]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x45d7]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x26
    je     1c4e <node38>
    cmp    rax,0xc2
    je     4580 <node194>
    cmp    rax,0x70
    je     2dd8 <node112>
    jmp    8e4d <fail_code>
0000000000006a22 <node316>:
    lea    rax,[rip+0x46a7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x31
    inc    rbx
    lea    rdi,[rip+0x45d9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x458e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xca
    je     485a <node202>
    cmp    rax,0x8e
    je     36ac <node142>
    cmp    rax,0xc
    je     149c <node12>
    cmp    rax,0x15
    je     1753 <node21>
    cmp    rax,0x157
    je     7165 <node343>
    cmp    rax,0x1c5
    je     8dce <node453>
    jmp    8e4d <fail_code>
0000000000006a8f <node317>:
    lea    rax,[rip+0x463a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x34
    inc    rbx
    lea    rdi,[rip+0x456c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4521]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x171
    je     7923 <node369>
    cmp    rax,0xd0
    je     49f0 <node208>
    cmp    rax,0x180
    je     7c84 <node384>
    jmp    8e4d <fail_code>
0000000000006adc <node318>:
    lea    rax,[rip+0x45ed]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4c
    inc    rbx
    lea    rdi,[rip+0x451f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x44d4]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x12b
    je     65b7 <node299>
    cmp    rax,0x178
    je     7a72 <node376>
    jmp    8e4d <fail_code>
0000000000006b1d <node319>:
    lea    rax,[rip+0x45ac]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x73
    inc    rbx
    lea    rdi,[rip+0x44de]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4493]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x160
    je     7390 <node352>
    cmp    rax,0x7e
    je     31f6 <node126>
    cmp    rax,0x86
    je     343a <node134>
    cmp    rax,0xc7
    je     471d <node199>
    cmp    rax,0xbf
    je     44c3 <node191>
    cmp    rax,0x135
    je     682d <node309>
    cmp    rax,0x8d
    je     3647 <node141>
    jmp    8e4d <fail_code>
0000000000006b98 <node320>:
    lea    rax,[rip+0x4531]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x27
    inc    rbx
    lea    rdi,[rip+0x4463]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4418]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xcc
    je     48e6 <node204>
    cmp    rax,0xc6
    je     46be <node198>
    cmp    rax,0x186
    je     7de0 <node390>
    cmp    rax,0x152
    je     7002 <node338>
    cmp    rax,0x175
    je     79d5 <node373>
    cmp    rax,0x1bf
    je     8c19 <node447>
    cmp    rax,0x61
    je     2a5d <node97>
    cmp    rax,0xfd
    je     585f <node253>
    jmp    8e4d <fail_code>
0000000000006c1f <node321>:
    lea    rax,[rip+0x44aa]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4e
    inc    rbx
    lea    rdi,[rip+0x43dc]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4391]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x167
    je     7627 <node359>
    jmp    8e4d <fail_code>
0000000000006c54 <node322>:
    lea    rax,[rip+0x4475]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x76
    inc    rbx
    lea    rdi,[rip+0x43a7]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x435c]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xc6
    je     46be <node198>
    cmp    rax,0x18c
    je     7ff6 <node396>
    cmp    rax,0x12e
    je     661e <node302>
    cmp    rax,0x38
    je     2018 <node56>
    cmp    rax,0x197
    je     82bd <node407>
    cmp    rax,0x7d
    je     31ab <node125>
    cmp    rax,0x1ab
    je     87b3 <node427>
    jmp    8e4d <fail_code>
0000000000006ccd <node323>:
    lea    rax,[rip+0x43fc]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x62
    inc    rbx
    lea    rdi,[rip+0x432e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x42e3]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x133
    je     678d <node307>
    cmp    rax,0x77
    je     2fd3 <node119>
    cmp    rax,0x16a
    je     772c <node362>
    cmp    rax,0x65
    je     2b05 <node101>
    jmp    8e4d <fail_code>
0000000000006d22 <node324>:
    lea    rax,[rip+0x43a7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x21
    inc    rbx
    lea    rdi,[rip+0x42d9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x428e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x188
    je     7e9a <node392>
    jmp    8e4d <fail_code>
0000000000006d57 <node325>:
    lea    rax,[rip+0x4372]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x20
    inc    rbx
    jmp    8e4d <fail_code>
0000000000006d6a <node326>:
    lea    rax,[rip+0x435f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x20
    inc    rbx
    lea    rdi,[rip+0x4291]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4246]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x75
    je     2f6b <node117>
    jmp    8e4d <fail_code>
0000000000006d9d <node327>:
    lea    rax,[rip+0x432c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3a
    inc    rbx
    jmp    8e4d <fail_code>
0000000000006db0 <node328>:
    lea    rax,[rip+0x4319]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x53
    inc    rbx
    lea    rdi,[rip+0x424b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4200]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x125
    je     6437 <node293>
    jmp    8e4d <fail_code>
0000000000006de5 <node329>:
    lea    rax,[rip+0x42e4]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x36
    inc    rbx
    lea    rdi,[rip+0x4216]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x41cb]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x13a
    je     69c6 <node314>
    cmp    rax,0x15e
    je     736a <node350>
    jmp    8e4d <fail_code>
0000000000006e26 <node330>:
    lea    rax,[rip+0x42a3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x62
    inc    rbx
    lea    rdi,[rip+0x41d5]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x418a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x118
    je     5ff6 <node280>
    cmp    rax,0x9a
    je     3ad2 <node154>
    cmp    rax,0x112
    je     5e58 <node274>
    cmp    rax,0xdf
    je     4ef3 <node223>
    jmp    8e4d <fail_code>
0000000000006e7f <node331>:
    lea    rax,[rip+0x424a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x24
    inc    rbx
    lea    rdi,[rip+0x417c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x4131]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xee
    je     52ac <node238>
    cmp    rax,0x63
    je     2aa5 <node99>
    cmp    rax,0x3f
    je     2269 <node63>
    cmp    rax,0x1d
    je     196b <node29>
    jmp    8e4d <fail_code>
0000000000006ed2 <node332>:
    lea    rax,[rip+0x41f7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x23
    inc    rbx
    lea    rdi,[rip+0x4129]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x40de]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xb
    je     1489 <node11>
    jmp    8e4d <fail_code>
0000000000006f05 <node333>:
    lea    rax,[rip+0x41c4]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x41
    inc    rbx
    lea    rdi,[rip+0x40f6]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x40ab]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a9
    je     8727 <node425>
    cmp    rax,0x149
    je     6de5 <node329>
    jmp    8e4d <fail_code>
0000000000006f46 <node334>:
    lea    rax,[rip+0x4183]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3d
    inc    rbx
    lea    rdi,[rip+0x40b5]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x406a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x145
    je     6d57 <node325>
    cmp    rax,0x50
    je     265c <node80>
    jmp    8e4d <fail_code>
0000000000006f85 <node335>:
    lea    rax,[rip+0x4144]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x39
    inc    rbx
    lea    rdi,[rip+0x4076]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x402b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x153
    je     706f <node339>
    cmp    rax,0x90
    je     3742 <node144>
    cmp    rax,0xb7
    je     42b9 <node183>
    cmp    rax,0x2e
    je     1db4 <node46>
    jmp    8e4d <fail_code>
0000000000006fdc <node336>:
    lea    rax,[rip+0x40ed]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7c
    inc    rbx
    jmp    8e4d <fail_code>
0000000000006fef <node337>:
    lea    rax,[rip+0x40da]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2e
    inc    rbx
    jmp    8e4d <fail_code>
0000000000007002 <node338>:
    lea    rax,[rip+0x40c7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x25
    inc    rbx
    lea    rdi,[rip+0x3ff9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3fae]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a0
    je     8538 <node416>
    cmp    rax,0xe6
    je     50d6 <node230>
    cmp    rax,0xf
    je     15a3 <node15>
    cmp    rax,0x81
    je     32ad <node129>
    cmp    rax,0x1a3
    je     861b <node419>
    cmp    rax,0x1e
    je     199e <node30>
    jmp    8e4d <fail_code>
000000000000706f <node339>:
    lea    rax,[rip+0x405a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4c
    inc    rbx
    lea    rdi,[rip+0x3f8c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3f41]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xc6
    je     46be <node198>
    cmp    rax,0x1b0
    je     8882 <node432>
    cmp    rax,0x9f
    je     3cc9 <node159>
    cmp    rax,0x1
    je     1195 <node1>
    cmp    rax,0x11d
    je     61cd <node285>
    jmp    8e4d <fail_code>
00000000000070d2 <node340>:
    lea    rax,[rip+0x3ff7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2c
    inc    rbx
    jmp    8e4d <fail_code>
00000000000070e5 <node341>:
    lea    rax,[rip+0x3fe4]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x68
    inc    rbx
    lea    rdi,[rip+0x3f16]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3ecb]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xfd
    je     585f <node253>
    cmp    rax,0xb2
    je     4186 <node178>
    jmp    8e4d <fail_code>
0000000000007126 <node342>:
    lea    rax,[rip+0x3fa3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2f
    inc    rbx
    lea    rdi,[rip+0x3ed5]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3e8a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x81
    je     32ad <node129>
    cmp    rax,0x62
    je     2a92 <node98>
    jmp    8e4d <fail_code>
0000000000007165 <node343>:
    lea    rax,[rip+0x3f64]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7c
    inc    rbx
    lea    rdi,[rip+0x3e96]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3e4b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x11f
    je     6289 <node287>
    cmp    rax,0xf
    je     15a3 <node15>
    cmp    rax,0x189
    je     7ecf <node393>
    jmp    8e4d <fail_code>
00000000000071b0 <node344>:
    lea    rax,[rip+0x3f19]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x65
    inc    rbx
    lea    rdi,[rip+0x3e4b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3e00]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xfe
    je     58a0 <node254>
    cmp    rax,0x160
    je     7390 <node352>
    cmp    rax,0x45
    je     238f <node69>
    jmp    8e4d <fail_code>
00000000000071fb <node345>:
    lea    rax,[rip+0x3ece]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x23
    inc    rbx
    lea    rdi,[rip+0x3e00]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3db5]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xba
    je     4340 <node186>
    cmp    rax,0xee
    je     52ac <node238>
    cmp    rax,0x116
    je     5f44 <node278>
    cmp    rax,0x117
    je     5f8f <node279>
    cmp    rax,0x9
    je     13e9 <node9>
    cmp    rax,0xe7
    je     5117 <node231>
    cmp    rax,0x13b
    je     69d9 <node315>
    jmp    8e4d <fail_code>
0000000000007276 <node346>:
    lea    rax,[rip+0x3e53]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2b
    inc    rbx
    lea    rdi,[rip+0x3d85]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3d3a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x6c
    je     2cb2 <node108>
    cmp    rax,0x59
    je     28a3 <node89>
    jmp    8e4d <fail_code>
00000000000072b3 <node347>:
    lea    rax,[rip+0x3e16]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x28
    inc    rbx
    jmp    8e4d <fail_code>
00000000000072c6 <node348>:
    lea    rax,[rip+0x3e03]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7a
    inc    rbx
    lea    rdi,[rip+0x3d35]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3cea]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x42
    je     22c4 <node66>
    cmp    rax,0x179
    je     7a85 <node377>
    cmp    rax,0x195
    je     8245 <node405>
    cmp    rax,0x187
    je     7e39 <node391>
    cmp    rax,0x117
    je     5f8f <node279>
    cmp    rax,0x161
    je     73e7 <node353>
    jmp    8e4d <fail_code>
0000000000007335 <node349>:
    lea    rax,[rip+0x3d94]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x77
    inc    rbx
    lea    rdi,[rip+0x3cc6]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3c7b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x88
    je     34ac <node136>
    jmp    8e4d <fail_code>
000000000000736a <node350>:
    lea    rax,[rip+0x3d5f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xa
    inc    rbx
    jmp    8e4d <fail_code>
000000000000737d <node351>:
    lea    rax,[rip+0x3d4c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x73
    inc    rbx
    jmp    8e4d <fail_code>
0000000000007390 <node352>:
    lea    rax,[rip+0x3d39]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5b
    inc    rbx
    lea    rdi,[rip+0x3c6b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3c20]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x2a
    je     1d38 <node42>
    cmp    rax,0xe5
    je     508b <node229>
    cmp    rax,0x13b
    je     69d9 <node315>
    cmp    rax,0x15a
    je     7276 <node346>
    jmp    8e4d <fail_code>
00000000000073e7 <node353>:
    lea    rax,[rip+0x3ce2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x39
    inc    rbx
    lea    rdi,[rip+0x3c14]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3bc9]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x129
    je     654f <node297>
    cmp    rax,0x197
    je     82bd <node407>
    cmp    rax,0xa8
    je     3ec8 <node168>
    jmp    8e4d <fail_code>
0000000000007434 <node354>:
    lea    rax,[rip+0x3c95]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2b
    inc    rbx
    lea    rdi,[rip+0x3bc7]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3b7c]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xf
    je     15a3 <node15>
    cmp    rax,0x16
    je     179c <node22>
    cmp    rax,0x137
    je     68cb <node311>
    cmp    rax,0x16d
    je     7803 <node365>
    cmp    rax,0x5b
    je     28c9 <node91>
    jmp    8e4d <fail_code>
0000000000007493 <node355>:
    lea    rax,[rip+0x3c36]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3c
    inc    rbx
    lea    rdi,[rip+0x3b68]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3b1d]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xb1
    je     4147 <node177>
    cmp    rax,0x16c
    je     77c2 <node364>
    cmp    rax,0x11c
    je     618e <node284>
    cmp    rax,0x12c
    je     65ca <node300>
    jmp    8e4d <fail_code>
00000000000074ec <node356>:
    lea    rax,[rip+0x3bdd]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2e
    inc    rbx
    lea    rdi,[rip+0x3b0f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3ac4]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x3b
    je     2137 <node59>
    cmp    rax,0x1b0
    je     8882 <node432>
    cmp    rax,0x6b
    je     2c5b <node107>
    cmp    rax,0x1ad
    je     8807 <node429>
    jmp    8e4d <fail_code>
0000000000007541 <node357>:
    lea    rax,[rip+0x3b88]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x39
    inc    rbx
    lea    rdi,[rip+0x3aba]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3a6f]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x9c
    je     3bc4 <node156>
    cmp    rax,0x173
    je     79af <node371>
    cmp    rax,0x2b
    je     1d4b <node43>
    jmp    8e4d <fail_code>
000000000000758c <node358>:
    lea    rax,[rip+0x3b3d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3c
    inc    rbx
    lea    rdi,[rip+0x3a6f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3a24]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xa0
    je     3d08 <node160>
    cmp    rax,0x11c
    je     618e <node284>
    cmp    rax,0x34
    je     1f42 <node52>
    cmp    rax,0x188
    je     7e9a <node392>
    cmp    rax,0xff
    je     58d5 <node255>
    cmp    rax,0xa5
    je     3dff <node165>
    cmp    rax,0x6f
    je     2d81 <node111>
    cmp    rax,0x49
    je     2499 <node73>
    cmp    rax,0x8f
    je     36f7 <node143>
    cmp    rax,0x16d
    je     7803 <node365>
    jmp    8e4d <fail_code>
0000000000007627 <node359>:
    lea    rax,[rip+0x3aa2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x35
    inc    rbx
    lea    rdi,[rip+0x39d4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3989]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x182
    je     7cfa <node386>
    cmp    rax,0xe1
    je     4fad <node225>
    jmp    8e4d <fail_code>
0000000000007668 <node360>:
    lea    rax,[rip+0x3a61]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x35
    inc    rbx
    lea    rdi,[rip+0x3993]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3948]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a4
    je     862e <node420>
    jmp    8e4d <fail_code>
000000000000769d <node361>:
    lea    rax,[rip+0x3a2c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x57
    inc    rbx
    lea    rdi,[rip+0x395e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3913]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x15
    je     1753 <node21>
    cmp    rax,0x2c
    je     1d5e <node44>
    cmp    rax,0xb8
    je     42ee <node184>
    cmp    rax,0x12a
    je     6584 <node298>
    cmp    rax,0x11b
    je     614d <node283>
    cmp    rax,0x185
    je     7d89 <node389>
    cmp    rax,0x5b
    je     28c9 <node91>
    cmp    rax,0x111
    je     5daf <node273>
    cmp    rax,0x153
    je     706f <node339>
    jmp    8e4d <fail_code>
000000000000772c <node362>:
    lea    rax,[rip+0x399d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6c
    inc    rbx
    lea    rdi,[rip+0x38cf]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3884]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x158
    je     71b0 <node344>
    cmp    rax,0x1a4
    je     862e <node420>
    jmp    8e4d <fail_code>
000000000000776d <node363>:
    lea    rax,[rip+0x395c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x77
    inc    rbx
    lea    rdi,[rip+0x388e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3843]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x42
    je     22c4 <node66>
    cmp    rax,0x41
    je     228f <node65>
    cmp    rax,0x84
    je     3394 <node132>
    cmp    rax,0x80
    je     329a <node128>
    jmp    8e4d <fail_code>
00000000000077c2 <node364>:
    lea    rax,[rip+0x3907]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xb
    inc    rbx
    lea    rdi,[rip+0x3839]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x37ee]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x149
    je     6de5 <node329>
    cmp    rax,0x10b
    je     5be3 <node267>
    jmp    8e4d <fail_code>
0000000000007803 <node365>:
    lea    rax,[rip+0x38c6]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7c
    inc    rbx
    lea    rdi,[rip+0x37f8]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x37ad]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xab
    je     3fb1 <node171>
    cmp    rax,0xc0
    je     4518 <node192>
    cmp    rax,0x197
    je     82bd <node407>
    cmp    rax,0xa2
    je     3d68 <node162>
    jmp    8e4d <fail_code>
000000000000785c <node366>:
    lea    rax,[rip+0x386d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x68
    inc    rbx
    lea    rdi,[rip+0x379f]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3754]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x134
    je     67fa <node308>
    cmp    rax,0x3f
    je     2269 <node63>
    jmp    8e4d <fail_code>
000000000000789b <node367>:
    lea    rax,[rip+0x382e]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6b
    inc    rbx
    lea    rdi,[rip+0x3760]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3715]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x40
    je     227c <node64>
    cmp    rax,0x53
    je     26f1 <node83>
    cmp    rax,0x151
    je     6fef <node337>
    jmp    8e4d <fail_code>
00000000000078e4 <node368>:
    lea    rax,[rip+0x37e5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x66
    inc    rbx
    lea    rdi,[rip+0x3717]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x36cc]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a0
    je     8538 <node416>
    cmp    rax,0x66
    je     2b64 <node102>
    jmp    8e4d <fail_code>
0000000000007923 <node369>:
    lea    rax,[rip+0x37a6]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x23
    inc    rbx
    lea    rdi,[rip+0x36d8]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x368d]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xcc
    je     48e6 <node204>
    cmp    rax,0xc6
    je     46be <node198>
    cmp    rax,0x49
    je     2499 <node73>
    cmp    rax,0x1b1
    je     8895 <node433>
    jmp    8e4d <fail_code>
000000000000797a <node370>:
    lea    rax,[rip+0x374f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7d
    inc    rbx
    lea    rdi,[rip+0x3681]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3636]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe6
    je     50d6 <node230>
    jmp    8e4d <fail_code>
00000000000079af <node371>:
    lea    rax,[rip+0x371a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x50
    inc    rbx
    jmp    8e4d <fail_code>
00000000000079c2 <node372>:
    lea    rax,[rip+0x3707]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x57
    inc    rbx
    jmp    8e4d <fail_code>
00000000000079d5 <node373>:
    lea    rax,[rip+0x36f4]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x28
    inc    rbx
    jmp    8e4d <fail_code>
00000000000079e8 <node374>:
    lea    rax,[rip+0x36e1]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x45
    inc    rbx
    lea    rdi,[rip+0x3613]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x35c8]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x55
    je     2775 <node85>
    cmp    rax,0xff
    je     58d5 <node255>
    cmp    rax,0x16d
    je     7803 <node365>
    cmp    rax,0x81
    je     32ad <node129>
    jmp    8e4d <fail_code>
0000000000007a3f <node375>:
    lea    rax,[rip+0x368a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    lea    rdi,[rip+0x35bc]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3571]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x58
    je     286e <node88>
    jmp    8e4d <fail_code>
0000000000007a72 <node376>:
    lea    rax,[rip+0x3657]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    jmp    8e4d <fail_code>
0000000000007a85 <node377>:
    lea    rax,[rip+0x3644]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x9
    inc    rbx
    lea    rdi,[rip+0x3576]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x352b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x155
    je     70e5 <node341>
    cmp    rax,0xdc
    je     4e32 <node220>
    cmp    rax,0xe3
    je     5009 <node227>
    jmp    8e4d <fail_code>
0000000000007ad2 <node378>:
    lea    rax,[rip+0x35f7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x21
    inc    rbx
    lea    rdi,[rip+0x3529]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x34de]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x59
    je     28a3 <node89>
    cmp    rax,0x3f
    je     2269 <node63>
    jmp    8e4d <fail_code>
0000000000007b0f <node379>:
    lea    rax,[rip+0x35ba]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x66
    inc    rbx
    lea    rdi,[rip+0x34ec]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x34a1]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x103
    je     599b <node259>
    cmp    rax,0x17d
    je     7b89 <node381>
    jmp    8e4d <fail_code>
0000000000007b4c <node380>:
    lea    rax,[rip+0x357d]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x51
    inc    rbx
    lea    rdi,[rip+0x34af]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3464]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x5a
    je     28b6 <node90>
    cmp    rax,0x1a
    je     18b2 <node26>
    jmp    8e4d <fail_code>
0000000000007b89 <node381>:
    lea    rax,[rip+0x3540]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x75
    inc    rbx
    lea    rdi,[rip+0x3472]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3427]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1f
    je     19b1 <node31>
    cmp    rax,0xf9
    je     563d <node249>
    cmp    rax,0x13f
    je     6b1d <node319>
    cmp    rax,0x18f
    je     80c9 <node399>
    jmp    8e4d <fail_code>
0000000000007be0 <node382>:
    lea    rax,[rip+0x34e9]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6d
    inc    rbx
    lea    rdi,[rip+0x341b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x33d0]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xcf
    je     49a5 <node207>
    cmp    rax,0x1b4
    je     8928 <node436>
    jmp    8e4d <fail_code>
0000000000007c21 <node383>:
    lea    rax,[rip+0x34a8]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3f
    inc    rbx
    lea    rdi,[rip+0x33da]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x338f]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x150
    je     6fdc <node336>
    cmp    rax,0x76
    je     2f9e <node118>
    cmp    rax,0x81
    je     32ad <node129>
    cmp    rax,0x1b3
    je     8915 <node435>
    cmp    rax,0xf7
    je     55b3 <node247>
    jmp    8e4d <fail_code>
0000000000007c84 <node384>:
    lea    rax,[rip+0x3445]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x79
    inc    rbx
    lea    rdi,[rip+0x3377]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x332c]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x190
    je     811c <node400>
    cmp    rax,0xb6
    je     4278 <node182>
    cmp    rax,0x19c
    je     8446 <node412>
    cmp    rax,0x4
    je     1286 <node4>
    cmp    rax,0x15b
    je     72b3 <node347>
    jmp    8e4d <fail_code>
0000000000007ce7 <node385>:
    lea    rax,[rip+0x33e2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x52
    inc    rbx
    jmp    8e4d <fail_code>
0000000000007cfa <node386>:
    lea    rax,[rip+0x33cf]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x34
    inc    rbx
    jmp    8e4d <fail_code>
0000000000007d0d <node387>:
    lea    rax,[rip+0x33bc]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6d
    inc    rbx
    lea    rdi,[rip+0x32ee]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x32a3]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x5d
    je     2995 <node93>
    cmp    rax,0x74
    je     2ee6 <node116>
    cmp    rax,0x143
    je     6ccd <node323>
    jmp    8e4d <fail_code>
0000000000007d56 <node388>:
    lea    rax,[rip+0x3373]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7c
    inc    rbx
    lea    rdi,[rip+0x32a5]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x325a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x64
    je     2af2 <node100>
    jmp    8e4d <fail_code>
0000000000007d89 <node389>:
    lea    rax,[rip+0x3340]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x27
    inc    rbx
    lea    rdi,[rip+0x3272]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3227]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x14c
    je     6ed2 <node332>
    cmp    rax,0x1b
    je     18c5 <node27>
    cmp    rax,0x134
    je     67fa <node308>
    cmp    rax,0x17c
    je     7b4c <node380>
    jmp    8e4d <fail_code>
0000000000007de0 <node390>:
    lea    rax,[rip+0x32e9]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2d
    inc    rbx
    lea    rdi,[rip+0x321b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x31d0]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x14c
    je     6ed2 <node332>
    cmp    rax,0xda
    je     4d7c <node218>
    cmp    rax,0xb1
    je     4147 <node177>
    cmp    rax,0x15f
    je     737d <node351>
    jmp    8e4d <fail_code>
0000000000007e39 <node391>:
    lea    rax,[rip+0x3290]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x41
    inc    rbx
    lea    rdi,[rip+0x31c2]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3177]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x3e
    je     2236 <node62>
    cmp    rax,0x90
    je     3742 <node144>
    cmp    rax,0x78
    je     3032 <node120>
    cmp    rax,0x150
    je     6fdc <node336>
    cmp    rax,0x185
    je     7d89 <node389>
    jmp    8e4d <fail_code>
0000000000007e9a <node392>:
    lea    rax,[rip+0x322f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x32
    inc    rbx
    lea    rdi,[rip+0x3161]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3116]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xaa
    je     3f7e <node170>
    jmp    8e4d <fail_code>
0000000000007ecf <node393>:
    lea    rax,[rip+0x31fa]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x74
    inc    rbx
    lea    rdi,[rip+0x312c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x30e1]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xf6
    je     557e <node246>
    cmp    rax,0x1b
    je     18c5 <node27>
    cmp    rax,0x1bb
    je     8b0d <node443>
    jmp    8e4d <fail_code>
0000000000007f1a <node394>:
    lea    rax,[rip+0x31af]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4d
    inc    rbx
    lea    rdi,[rip+0x30e1]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3096]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x36
    je     1fb8 <node54>
    cmp    rax,0x11c
    je     618e <node284>
    jmp    8e4d <fail_code>
0000000000007f59 <node395>:
    lea    rax,[rip+0x3170]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x43
    inc    rbx
    lea    rdi,[rip+0x30a2]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x3057]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x126
    je     644a <node294>
    cmp    rax,0x114
    je     5ee4 <node276>
    cmp    rax,0x18a
    je     7f1a <node394>
    cmp    rax,0xa6
    je     3e3e <node166>
    cmp    rax,0x1b6
    je     89cc <node438>
    cmp    rax,0x61
    je     2a5d <node97>
    cmp    rax,0x1b3
    je     8915 <node435>
    cmp    rax,0xbd
    je     4435 <node189>
    cmp    rax,0x12
    je     1684 <node18>
    cmp    rax,0xb5
    je     4245 <node181>
    jmp    8e4d <fail_code>
0000000000007ff6 <node396>:
    lea    rax,[rip+0x30d3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6f
    inc    rbx
    lea    rdi,[rip+0x3005]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2fba]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xb5
    je     4245 <node181>
    cmp    rax,0x136
    je     688c <node310>
    jmp    8e4d <fail_code>
0000000000008037 <node397>:
    lea    rax,[rip+0x3092]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x35
    inc    rbx
    lea    rdi,[rip+0x2fc4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2f79]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x18e
    je     807e <node398>
    cmp    rax,0x4f
    je     25e9 <node79>
    cmp    rax,0x169
    je     769d <node361>
    jmp    8e4d <fail_code>
000000000000807e <node398>:
    lea    rax,[rip+0x304b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x35
    inc    rbx
    lea    rdi,[rip+0x2f7d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2f32]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x73
    je     2e83 <node115>
    cmp    rax,0x1c1
    je     8cc7 <node449>
    cmp    rax,0xd3
    je     4b47 <node211>
    jmp    8e4d <fail_code>
00000000000080c9 <node399>:
    lea    rax,[rip+0x3000]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6e
    inc    rbx
    lea    rdi,[rip+0x2f32]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2ee7]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xfb
    je     573f <node251>
    cmp    rax,0x23
    je     1b29 <node35>
    cmp    rax,0x191
    je     816f <node401>
    cmp    rax,0xad
    je     401b <node173>
    jmp    8e4d <fail_code>
000000000000811c <node400>:
    lea    rax,[rip+0x2fad]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x43
    inc    rbx
    lea    rdi,[rip+0x2edf]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2e94]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x25
    je     1c03 <node37>
    cmp    rax,0x8
    je     13a8 <node8>
    cmp    rax,0xe
    je     1590 <node14>
    cmp    rax,0x1b2
    je     88d4 <node434>
    jmp    8e4d <fail_code>
000000000000816f <node401>:
    lea    rax,[rip+0x2f5a]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5f
    inc    rbx
    lea    rdi,[rip+0x2e8c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2e41]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x89
    je     34df <node137>
    cmp    rax,0x31
    je     1e6f <node49>
    jmp    8e4d <fail_code>
00000000000081ae <node402>:
    lea    rax,[rip+0x2f1b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3d
    inc    rbx
    jmp    8e4d <fail_code>
00000000000081c1 <node403>:
    lea    rax,[rip+0x2f08]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    lea    rdi,[rip+0x2e3a]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2def]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xf0
    je     5374 <node240>
    cmp    rax,0xcc
    je     48e6 <node204>
    cmp    rax,0x19c
    je     8446 <node412>
    cmp    rax,0x11e
    je     620c <node286>
    cmp    rax,0x8d
    je     3647 <node141>
    cmp    rax,0x15b
    je     72b3 <node347>
    jmp    8e4d <fail_code>
0000000000008232 <node404>:
    lea    rax,[rip+0x2e97]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x46
    inc    rbx
    jmp    8e4d <fail_code>
0000000000008245 <node405>:
    lea    rax,[rip+0x2e84]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x23
    inc    rbx
    lea    rdi,[rip+0x2db6]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2d6b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x90
    je     3742 <node144>
    cmp    rax,0xf4
    je     54f2 <node244>
    cmp    rax,0x16e
    je     785c <node366>
    cmp    rax,0x107
    je     5a9d <node263>
    cmp    rax,0x12f
    je     6631 <node303>
    jmp    8e4d <fail_code>
00000000000082aa <node406>:
    lea    rax,[rip+0x2e1f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x48
    inc    rbx
    jmp    8e4d <fail_code>
00000000000082bd <node407>:
    lea    rax,[rip+0x2e0c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x29
    inc    rbx
    lea    rdi,[rip+0x2d3e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2cf3]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x181
    je     7ce7 <node385>
    jmp    8e4d <fail_code>
00000000000082f2 <node408>:
    lea    rax,[rip+0x2dd7]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x32
    inc    rbx
    lea    rdi,[rip+0x2d09]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2cbe]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x12e
    je     661e <node302>
    jmp    8e4d <fail_code>
0000000000008327 <node409>:
    lea    rax,[rip+0x2da2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4e
    inc    rbx
    lea    rdi,[rip+0x2cd4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2c89]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x3f
    je     2269 <node63>
    cmp    rax,0x13d
    je     6a8f <node317>
    jmp    8e4d <fail_code>
0000000000008366 <node410>:
    lea    rax,[rip+0x2d63]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0xb
    inc    rbx
    lea    rdi,[rip+0x2c95]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2c4a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe8
    je     514a <node232>
    cmp    rax,0xd8
    je     4cda <node216>
    cmp    rax,0x108
    je     5ab0 <node264>
    cmp    rax,0xae
    je     407e <node174>
    cmp    rax,0xea
    je     5170 <node234>
    cmp    rax,0x10d
    je     5c77 <node269>
    cmp    rax,0x161
    je     73e7 <node353>
    cmp    rax,0x111
    je     5daf <node273>
    jmp    8e4d <fail_code>
00000000000083ef <node411>:
    lea    rax,[rip+0x2cda]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2e
    inc    rbx
    lea    rdi,[rip+0x2c0c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2bc1]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x5a
    je     28b6 <node90>
    cmp    rax,0x17a
    je     7ad2 <node378>
    cmp    rax,0x107
    je     5a9d <node263>
    cmp    rax,0x1b2
    je     88d4 <node434>
    jmp    8e4d <fail_code>
0000000000008446 <node412>:
    lea    rax,[rip+0x2c83]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2e
    inc    rbx
    lea    rdi,[rip+0x2bb5]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2b6a]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x51
    je     266f <node81>
    cmp    rax,0xbd
    je     4435 <node189>
    jmp    8e4d <fail_code>
0000000000008485 <node413>:
    lea    rax,[rip+0x2c44]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x28
    inc    rbx
    lea    rdi,[rip+0x2b76]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2b2b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xca
    je     485a <node202>
    cmp    rax,0x52
    je     26a4 <node82>
    cmp    rax,0xf
    je     15a3 <node15>
    cmp    rax,0x177
    je     7a3f <node375>
    cmp    rax,0x197
    je     82bd <node407>
    jmp    8e4d <fail_code>
00000000000084e6 <node414>:
    lea    rax,[rip+0x2be3]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x67
    inc    rbx
    lea    rdi,[rip+0x2b15]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2aca]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x6e
    je     2d2a <node110>
    cmp    rax,0x166
    je     758c <node358>
    jmp    8e4d <fail_code>
0000000000008525 <node415>:
    lea    rax,[rip+0x2ba4]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7d
    inc    rbx
    jmp    8e4d <fail_code>
0000000000008538 <node416>:
    lea    rax,[rip+0x2b91]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x34
    inc    rbx
    lea    rdi,[rip+0x2ac3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2a78]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x11
    je     1671 <node17>
    cmp    rax,0x100
    je     5920 <node256>
    jmp    8e4d <fail_code>
0000000000008577 <node417>:
    lea    rax,[rip+0x2b52]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3b
    inc    rbx
    lea    rdi,[rip+0x2a84]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2a39]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x170
    je     78e4 <node368>
    cmp    rax,0x1aa
    je     8768 <node426>
    jmp    8e4d <fail_code>
00000000000085b8 <node418>:
    lea    rax,[rip+0x2b11]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x53
    inc    rbx
    lea    rdi,[rip+0x2a43]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x29f8]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x18c
    je     7ff6 <node396>
    cmp    rax,0x18a
    je     7f1a <node394>
    cmp    rax,0x42
    je     22c4 <node66>
    cmp    rax,0x135
    je     682d <node309>
    cmp    rax,0x119
    je     609b <node281>
    jmp    8e4d <fail_code>
000000000000861b <node419>:
    lea    rax,[rip+0x2aae]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x20
    inc    rbx
    jmp    8e4d <fail_code>
000000000000862e <node420>:
    lea    rax,[rip+0x2a9b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x79
    inc    rbx
    lea    rdi,[rip+0x29cd]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2982]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1c6
    je     8e18 <node454>
    cmp    rax,0x6d
    je     2cc5 <node109>
    jmp    8e4d <fail_code>
000000000000866d <node421>:
    lea    rax,[rip+0x2a5c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x2b
    inc    rbx
    jmp    8e4d <fail_code>
0000000000008680 <node422>:
    lea    rax,[rip+0x2a49]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x39
    inc    rbx
    lea    rdi,[rip+0x297b]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2930]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xab
    je     3fb1 <node171>
    cmp    rax,0x1ad
    je     8807 <node429>
    jmp    8e4d <fail_code>
00000000000086c1 <node423>:
    lea    rax,[rip+0x2a08]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x36
    inc    rbx
    lea    rdi,[rip+0x293a]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x28ef]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x2a
    je     1d38 <node42>
    jmp    8e4d <fail_code>
00000000000086f4 <node424>:
    lea    rax,[rip+0x29d5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x56
    inc    rbx
    lea    rdi,[rip+0x2907]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x28bc]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x6a
    je     2c48 <node106>
    jmp    8e4d <fail_code>
0000000000008727 <node425>:
    lea    rax,[rip+0x29a2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6f
    inc    rbx
    lea    rdi,[rip+0x28d4]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2889]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x12d
    je     660b <node301>
    cmp    rax,0x1c4
    je     8dbe <node452>
    jmp    8e4d <fail_code>
0000000000008768 <node426>:
    lea    rax,[rip+0x2961]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x22
    inc    rbx
    lea    rdi,[rip+0x2893]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2848]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x101
    je     5933 <node257>
    cmp    rax,0x25
    je     1c03 <node37>
    cmp    rax,0xe8
    je     514a <node232>
    jmp    8e4d <fail_code>
00000000000087b3 <node427>:
    lea    rax,[rip+0x2916]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x55
    inc    rbx
    lea    rdi,[rip+0x2848]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x27fd]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe8
    je     514a <node232>
    cmp    rax,0xe9
    je     515d <node233>
    jmp    8e4d <fail_code>
00000000000087f4 <node428>:
    lea    rax,[rip+0x28d5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x50
    inc    rbx
    jmp    8e4d <fail_code>
0000000000008807 <node429>:
    lea    rax,[rip+0x28c2]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x55
    inc    rbx
    jmp    8e4d <fail_code>
000000000000881a <node430>:
    lea    rax,[rip+0x28af]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x25
    inc    rbx
    jmp    8e4d <fail_code>
000000000000882d <node431>:
    lea    rax,[rip+0x289c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x61
    inc    rbx
    lea    rdi,[rip+0x27ce]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2783]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe
    je     1590 <node14>
    cmp    rax,0x15a
    je     7276 <node346>
    cmp    rax,0x182
    je     7cfa <node386>
    cmp    rax,0x5b
    je     28c9 <node91>
    jmp    8e4d <fail_code>
0000000000008882 <node432>:
    lea    rax,[rip+0x2847]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3a
    inc    rbx
    jmp    8e4d <fail_code>
0000000000008895 <node433>:
    lea    rax,[rip+0x2834]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7a
    inc    rbx
    lea    rdi,[rip+0x2766]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x271b]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x12b
    je     65b7 <node299>
    cmp    rax,0x1a
    je     18b2 <node26>
    jmp    8e4d <fail_code>
00000000000088d4 <node434>:
    lea    rax,[rip+0x27f5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x6e
    inc    rbx
    lea    rdi,[rip+0x2727]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x26dc]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x13a
    je     69c6 <node314>
    cmp    rax,0x114
    je     5ee4 <node276>
    jmp    8e4d <fail_code>
0000000000008915 <node435>:
    lea    rax,[rip+0x27b4]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x47
    inc    rbx
    jmp    8e4d <fail_code>
0000000000008928 <node436>:
    lea    rax,[rip+0x27a1]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x3e
    inc    rbx
    lea    rdi,[rip+0x26d3]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2688]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe2
    je     4fc0 <node226>
    cmp    rax,0x11e
    je     620c <node286>
    cmp    rax,0x152
    je     7002 <node338>
    cmp    rax,0x63
    je     2aa5 <node99>
    cmp    rax,0xe5
    je     508b <node229>
    cmp    rax,0x157
    je     7165 <node343>
    jmp    8e4d <fail_code>
0000000000008997 <node437>:
    lea    rax,[rip+0x2732]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x5b
    inc    rbx
    lea    rdi,[rip+0x2664]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2619]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xe9
    je     515d <node233>
    jmp    8e4d <fail_code>
00000000000089cc <node438>:
    lea    rax,[rip+0x26fd]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x70
    inc    rbx
    jmp    8e4d <fail_code>
00000000000089df <node439>:
    lea    rax,[rip+0x26ea]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x52
    inc    rbx
    lea    rdi,[rip+0x261c]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x25d1]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x19
    je     187f <node25>
    cmp    rax,0x1c4
    je     8dbe <node452>
    cmp    rax,0xec
    je     522a <node236>
    cmp    rax,0x132
    je     6738 <node306>
    cmp    rax,0xb3
    je     41bb <node179>
    jmp    8e4d <fail_code>
0000000000008a42 <node440>:
    lea    rax,[rip+0x2687]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x48
    inc    rbx
    lea    rdi,[rip+0x25b9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x256e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xee
    je     52ac <node238>
    cmp    rax,0x13a
    je     69c6 <node314>
    cmp    rax,0xe
    je     1590 <node14>
    cmp    rax,0x19b
    je     83ef <node411>
    cmp    rax,0xa1
    je     3d55 <node161>
    cmp    rax,0x129
    je     654f <node297>
    jmp    8e4d <fail_code>
0000000000008ab1 <node441>:
    lea    rax,[rip+0x2618]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x33
    inc    rbx
    lea    rdi,[rip+0x254a]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x24ff]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x96
    je     3978 <node150>
    cmp    rax,0x57
    je     2817 <node87>
    cmp    rax,0x3a
    je     20bc <node58>
    jmp    8e4d <fail_code>
0000000000008afa <node442>:
    lea    rax,[rip+0x25cf]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x47
    inc    rbx
    jmp    8e4d <fail_code>
0000000000008b0d <node443>:
    lea    rax,[rip+0x25bc]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x37
    inc    rbx
    lea    rdi,[rip+0x24ee]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x24a3]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x168
    je     7668 <node360>
    jmp    8e4d <fail_code>
0000000000008b42 <node444>:
    lea    rax,[rip+0x2587]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4d
    inc    rbx
    lea    rdi,[rip+0x24b9]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x246e]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1a3
    je     861b <node419>
    jmp    8e4d <fail_code>
0000000000008b77 <node445>:
    lea    rax,[rip+0x2552]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x30
    inc    rbx
    lea    rdi,[rip+0x2484]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2439]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x174
    je     79c2 <node372>
    cmp    rax,0x106
    je     5a8a <node262>
    cmp    rax,0xc2
    je     4580 <node194>
    cmp    rax,0x1a9
    je     8727 <node425>
    cmp    rax,0x2b
    je     1d4b <node43>
    cmp    rax,0x41
    je     228f <node65>
    jmp    8e4d <fail_code>
0000000000008be4 <node446>:
    lea    rax,[rip+0x24e5]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x36
    inc    rbx
    lea    rdi,[rip+0x2417]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x23cc]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x194
    je     8232 <node404>
    jmp    8e4d <fail_code>
0000000000008c19 <node447>:
    lea    rax,[rip+0x24b0]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x37
    inc    rbx
    lea    rdi,[rip+0x23e2]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2397]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xd8
    je     4cda <node216>
    cmp    rax,0x1bb
    je     8b0d <node443>
    jmp    8e4d <fail_code>
0000000000008c5a <node448>:
    lea    rax,[rip+0x246f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x69
    inc    rbx
    lea    rdi,[rip+0x23a1]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2356]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x88
    je     34ac <node136>
    cmp    rax,0x146
    je     6d6a <node326>
    cmp    rax,0x35
    je     1f77 <node53>
    cmp    rax,0x141
    je     6c1f <node321>
    cmp    rax,0xf1
    je     53b3 <node241>
    cmp    rax,0x7b
    je     30fd <node123>
    jmp    8e4d <fail_code>
0000000000008cc7 <node449>:
    lea    rax,[rip+0x2402]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x4e
    inc    rbx
    lea    rdi,[rip+0x2334]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x22e9]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0xac
    je     3fc4 <node172>
    cmp    rax,0xca
    je     485a <node202>
    cmp    rax,0x1b
    je     18c5 <node27>
    cmp    rax,0xb6
    je     4278 <node182>
    cmp    rax,0x15
    je     1753 <node21>
    cmp    rax,0x22
    je     1ae0 <node34>
    cmp    rax,0x135
    je     682d <node309>
    cmp    rax,0x11d
    je     61cd <node285>
    jmp    8e4d <fail_code>
0000000000008d4a <node450>:
    lea    rax,[rip+0x237f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x20
    inc    rbx
    jmp    8e4d <fail_code>
0000000000008d5d <node451>:
    lea    rax,[rip+0x236c]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7e
    inc    rbx
    lea    rdi,[rip+0x229e]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x2253]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x2c
    je     1d5e <node44>
    cmp    rax,0x19
    je     187f <node25>
    cmp    rax,0xbb
    je     43ad <node187>
    cmp    rax,0xdd
    je     4e7d <node221>
    cmp    rax,0xbf
    je     44c3 <node191>
    jmp    8e4d <fail_code>
0000000000008dbe <node452>:
    lea    rax,[rip+0x230b]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x79
    inc    rbx
    jmp    8e4d <fail_code>
0000000000008dce <node453>:
    lea    rax,[rip+0x22fb]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x66
    inc    rbx
    lea    rdi,[rip+0x222d]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x21e2]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x1bc
    je     8b42 <node444>
    cmp    rax,0x13e
    je     6adc <node318>
    cmp    rax,0x199
    je     8327 <node409>
    jmp    8e4d <fail_code>
0000000000008e18 <node454>:
    lea    rax,[rip+0x22b1]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x7d
    inc    rbx
    lea    rdi,[rip+0x2258]        # b085 <maybe_success>
    xor    eax,eax
    call   QWORD PTR [rip+0x218b]        # afc0 <printf@GLIBC_2.2.5>
    lea    rdi,[rip+0x21d9]        # b015 <output_format>
    lea    rsi,[rip+0x228d]        # b0d0 <__TMC_END__>
    xor    eax,eax
    call   QWORD PTR [rip+0x2175]        # afc0 <printf@GLIBC_2.2.5>
    jmp    8e5c <end_code>
    lea    rdi,[rip+0x2223]        # b077 <fail>
    xor    eax,eax
    call   QWORD PTR [rip+0x2164]        # afc0 <printf@GLIBC_2.2.5>
    xor    eax,eax
    leave
    ret
    sub    rsp,0x8
    add    rsp,0x8
    ret
