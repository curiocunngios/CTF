# Below is the assembly of the executable 
```as

./ret2win:     file format elf64-x86-64




Disassembly of section .plt:

0000000000400540 <.plt>:
  400540:	ff 35 c2 0a 20 00    	push   QWORD PTR [rip+0x200ac2]        # 601008 <_GLOBAL_OFFSET_TABLE_+0x8>
  400546:	ff 25 c4 0a 20 00    	jmp    QWORD PTR [rip+0x200ac4]        # 601010 <_GLOBAL_OFFSET_TABLE_+0x10>
  40054c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000000400550 <puts@plt>:
  400550:	ff 25 c2 0a 20 00    	jmp    QWORD PTR [rip+0x200ac2]        # 601018 <puts@GLIBC_2.2.5>
  400556:	68 00 00 00 00       	push   0x0
  40055b:	e9 e0 ff ff ff       	jmp    400540 <.plt>

0000000000400560 <system@plt>:
  400560:	ff 25 ba 0a 20 00    	jmp    QWORD PTR [rip+0x200aba]        # 601020 <system@GLIBC_2.2.5>
  400566:	68 01 00 00 00       	push   0x1
  40056b:	e9 d0 ff ff ff       	jmp    400540 <.plt>

0000000000400570 <printf@plt>:
  400570:	ff 25 b2 0a 20 00    	jmp    QWORD PTR [rip+0x200ab2]        # 601028 <printf@GLIBC_2.2.5>
  400576:	68 02 00 00 00       	push   0x2
  40057b:	e9 c0 ff ff ff       	jmp    400540 <.plt>

0000000000400580 <memset@plt>:
  400580:	ff 25 aa 0a 20 00    	jmp    QWORD PTR [rip+0x200aaa]        # 601030 <memset@GLIBC_2.2.5>
  400586:	68 03 00 00 00       	push   0x3
  40058b:	e9 b0 ff ff ff       	jmp    400540 <.plt>

0000000000400590 <read@plt>:
  400590:	ff 25 a2 0a 20 00    	jmp    QWORD PTR [rip+0x200aa2]        # 601038 <read@GLIBC_2.2.5>
  400596:	68 04 00 00 00       	push   0x4
  40059b:	e9 a0 ff ff ff       	jmp    400540 <.plt>

00000000004005a0 <setvbuf@plt>:
  4005a0:	ff 25 9a 0a 20 00    	jmp    QWORD PTR [rip+0x200a9a]        # 601040 <setvbuf@GLIBC_2.2.5>
  4005a6:	68 05 00 00 00       	push   0x5
  4005ab:	e9 90 ff ff ff       	jmp    400540 <.plt>

Disassembly of section .text:


0000000000400697 <main>:
  400697:	55                   	push   rbp
  400698:	48 89 e5             	mov    rbp,rsp
  
  
  
  40069b:	48 8b 05 b6 09 20 00 	mov    rax,QWORD PTR [rip+0x2009b6]        # 601058 <stdout@GLIBC_2.2.5>
  4006a2:	b9 00 00 00 00       	mov    ecx,0x0 
  4006a7:	ba 02 00 00 00       	mov    edx,0x2 
  4006ac:	be 00 00 00 00       	mov    esi,0x0 
  4006b1:	48 89 c7             	mov    rdi,rax
  4006b4:	e8 e7 fe ff ff       	call   4005a0 <setvbuf@plt>
  4006b9:	bf 08 08 40 00       	mov    edi,0x400808
  4006be:	e8 8d fe ff ff       	call   400550 <puts@plt>
  4006c3:	bf 20 08 40 00       	mov    edi,0x400820
  4006c8:	e8 83 fe ff ff       	call   400550 <puts@plt>
  4006cd:	b8 00 00 00 00       	mov    eax,0x0
  4006d2:	e8 11 00 00 00       	call   4006e8 <pwnme>
  4006d7:	bf 28 08 40 00       	mov    edi,0x400828
  4006dc:	e8 6f fe ff ff       	call   400550 <puts@plt>
  4006e1:	b8 00 00 00 00       	mov    eax,0x0
  4006e6:	5d                   	pop    rbp
  4006e7:	c3                   	ret

00000000004006e8 <pwnme>:
  4006e8:	55                   	push   rbp
  4006e9:	48 89 e5             	mov    rbp,rsp
  4006ec:	48 83 ec 20          	sub    rsp,0x20
  4006f0:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  4006f4:	ba 20 00 00 00       	mov    edx,0x20
  4006f9:	be 00 00 00 00       	mov    esi,0x0
  4006fe:	48 89 c7             	mov    rdi,rax
  400701:	e8 7a fe ff ff       	call   400580 <memset@plt>
  400706:	bf 38 08 40 00       	mov    edi,0x400838
  40070b:	e8 40 fe ff ff       	call   400550 <puts@plt>
  400710:	bf 98 08 40 00       	mov    edi,0x400898
  400715:	e8 36 fe ff ff       	call   400550 <puts@plt>
  40071a:	bf b8 08 40 00       	mov    edi,0x4008b8
  40071f:	e8 2c fe ff ff       	call   400550 <puts@plt>
  400724:	bf 18 09 40 00       	mov    edi,0x400918
  400729:	b8 00 00 00 00       	mov    eax,0x0
  40072e:	e8 3d fe ff ff       	call   400570 <printf@plt>
  400733:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  400737:	ba 38 00 00 00       	mov    edx,0x38
  40073c:	48 89 c6             	mov    rsi,rax
  40073f:	bf 00 00 00 00       	mov    edi,0x0
  400744:	e8 47 fe ff ff       	call   400590 <read@plt>
  400749:	bf 1b 09 40 00       	mov    edi,0x40091b
  40074e:	e8 fd fd ff ff       	call   400550 <puts@plt>
  400753:	90                   	nop
  400754:	c9                   	leave
  400755:	c3                   	ret

0000000000400756 <ret2win>:
  400756:	55                   	push   rbp
  400757:	48 89 e5             	mov    rbp,rsp
  40075a:	bf 26 09 40 00       	mov    edi,0x400926
  40075f:	e8 ec fd ff ff       	call   400550 <puts@plt>
  400764:	bf 43 09 40 00       	mov    edi,0x400943
  400769:	e8 f2 fd ff ff       	call   400560 <system@plt>
  40076e:	90                   	nop
  40076f:	5d                   	pop    rbp
  400770:	c3                   	ret
  400771:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  400778:	00 00 00 
  40077b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

```

