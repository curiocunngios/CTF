A weird string that seemed to be encoded or some shit is present in the challenge description

```
5d8a8d81094757190a07cc217683e0972713401648b0fdbb4116a20f2bd677009230db8c8990b3b6033b9fabcec2b1f908f1fbc284d29e8ba7de8b6d370a9262
```

program behaviour:

You input some string and the program output a some long strings with same length and similar format to the one on the challenge's page

```
──(kali㉿kali)-[~/Desktop/CTF/iforgor]
└─$ ./program
1
0ae6ece6720e62463d6ffd5229b096f21e20152e5195f8871d21f010048d3217d6038eb490b5b68a5f0ccdb4e199f4ee4cc2aefa9df79bb7fbe9d9721851d775                                                                                                
┌──(kali㉿kali)-[~/Desktop/CTF/iforgor]
└─$ ./program
2
09e6ece6720e62463d6ffd5229b096f21d20152e5195f8871d21f010048d3217d5038eb490b5b68a5f0ccdb4e199f4ee4fc2aefa9df79bb7fbe9d9721851d775                                                                                                
┌──(kali㉿kali)-[~/Desktop/CTF/iforgor]
└─$ ./program
hi
538fece6720e62463d6ffd5229b096f24749152e5195f8871d21f010048d32178f6a8eb490b5b68a5f0ccdb4e199f4ee15abaefa9df79bb7fbe9d9721851d775
```

The outputs are not randomized. So I guess it's about finding an input (potentially flag) that produces the string on the challenge description 

The output of `objdump -d program -M intel > source`

```as

program:     file format elf64-x86-64


Disassembly of section .init:

0000000000001000 <.init>:
    1000:	48 83 ec 08          	sub    rsp,0x8
    1004:	48 8b 05 c5 2f 00 00 	mov    rax,QWORD PTR [rip+0x2fc5]        # 3fd0 <__cxa_finalize@plt+0x2f70>
    100b:	48 85 c0             	test   rax,rax
    100e:	74 02                	je     1012 <strlen@plt-0x1e>
    1010:	ff d0                	call   rax
    1012:	48 83 c4 08          	add    rsp,0x8
    1016:	c3                   	ret

Disassembly of section .plt:

0000000000001020 <strlen@plt-0x10>:
    1020:	ff 35 ca 2f 00 00    	push   QWORD PTR [rip+0x2fca]        # 3ff0 <__cxa_finalize@plt+0x2f90>
    1026:	ff 25 cc 2f 00 00    	jmp    QWORD PTR [rip+0x2fcc]        # 3ff8 <__cxa_finalize@plt+0x2f98>
    102c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000000001030 <strlen@plt>:
    1030:	ff 25 ca 2f 00 00    	jmp    QWORD PTR [rip+0x2fca]        # 4000 <__cxa_finalize@plt+0x2fa0>
    1036:	68 00 00 00 00       	push   0x0
    103b:	e9 e0 ff ff ff       	jmp    1020 <strlen@plt-0x10>

0000000000001040 <printf@plt>:
    1040:	ff 25 c2 2f 00 00    	jmp    QWORD PTR [rip+0x2fc2]        # 4008 <__cxa_finalize@plt+0x2fa8>
    1046:	68 01 00 00 00       	push   0x1
    104b:	e9 d0 ff ff ff       	jmp    1020 <strlen@plt-0x10>

0000000000001050 <__isoc99_scanf@plt>:
    1050:	ff 25 ba 2f 00 00    	jmp    QWORD PTR [rip+0x2fba]        # 4010 <__cxa_finalize@plt+0x2fb0>
    1056:	68 02 00 00 00       	push   0x2
    105b:	e9 c0 ff ff ff       	jmp    1020 <strlen@plt-0x10>

Disassembly of section .plt.got:

0000000000001060 <__cxa_finalize@plt>:
    1060:	ff 25 7a 2f 00 00    	jmp    QWORD PTR [rip+0x2f7a]        # 3fe0 <__cxa_finalize@plt+0x2f80>
    1066:	66 90                	xchg   ax,ax

Disassembly of section .text:

0000000000001070 <.text>:
    1070:	31 ed                	xor    ebp,ebp
    1072:	49 89 d1             	mov    r9,rdx
    1075:	5e                   	pop    rsi
    1076:	48 89 e2             	mov    rdx,rsp
    1079:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
    107d:	50                   	push   rax
    107e:	54                   	push   rsp
    107f:	45 31 c0             	xor    r8d,r8d
    1082:	31 c9                	xor    ecx,ecx
    1084:	48 8d 3d ce 00 00 00 	lea    rdi,[rip+0xce]        # 1159 <__cxa_finalize@plt+0xf9>
    108b:	ff 15 2f 2f 00 00    	call   QWORD PTR [rip+0x2f2f]        # 3fc0 <__cxa_finalize@plt+0x2f60>
    1091:	f4                   	hlt
    1092:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    1099:	00 00 00 
    109c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    10a0:	48 8d 3d 81 2f 00 00 	lea    rdi,[rip+0x2f81]        # 4028 <__cxa_finalize@plt+0x2fc8>
    10a7:	48 8d 05 7a 2f 00 00 	lea    rax,[rip+0x2f7a]        # 4028 <__cxa_finalize@plt+0x2fc8>
    10ae:	48 39 f8             	cmp    rax,rdi
    10b1:	74 15                	je     10c8 <__cxa_finalize@plt+0x68>
    10b3:	48 8b 05 0e 2f 00 00 	mov    rax,QWORD PTR [rip+0x2f0e]        # 3fc8 <__cxa_finalize@plt+0x2f68>
    10ba:	48 85 c0             	test   rax,rax
    10bd:	74 09                	je     10c8 <__cxa_finalize@plt+0x68>
    10bf:	ff e0                	jmp    rax
    10c1:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    10c8:	c3                   	ret
    10c9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    10d0:	48 8d 3d 51 2f 00 00 	lea    rdi,[rip+0x2f51]        # 4028 <__cxa_finalize@plt+0x2fc8>
    10d7:	48 8d 35 4a 2f 00 00 	lea    rsi,[rip+0x2f4a]        # 4028 <__cxa_finalize@plt+0x2fc8>
    10de:	48 29 fe             	sub    rsi,rdi
    10e1:	48 89 f0             	mov    rax,rsi
    10e4:	48 c1 ee 3f          	shr    rsi,0x3f
    10e8:	48 c1 f8 03          	sar    rax,0x3
    10ec:	48 01 c6             	add    rsi,rax
    10ef:	48 d1 fe             	sar    rsi,1
    10f2:	74 14                	je     1108 <__cxa_finalize@plt+0xa8>
    10f4:	48 8b 05 dd 2e 00 00 	mov    rax,QWORD PTR [rip+0x2edd]        # 3fd8 <__cxa_finalize@plt+0x2f78>
    10fb:	48 85 c0             	test   rax,rax
    10fe:	74 08                	je     1108 <__cxa_finalize@plt+0xa8>
    1100:	ff e0                	jmp    rax
    1102:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    1108:	c3                   	ret
    1109:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    1110:	f3 0f 1e fa          	endbr64
    1114:	80 3d 0d 2f 00 00 00 	cmp    BYTE PTR [rip+0x2f0d],0x0        # 4028 <__cxa_finalize@plt+0x2fc8>
    111b:	75 2b                	jne    1148 <__cxa_finalize@plt+0xe8>
    111d:	55                   	push   rbp
    111e:	48 83 3d ba 2e 00 00 	cmp    QWORD PTR [rip+0x2eba],0x0        # 3fe0 <__cxa_finalize@plt+0x2f80>
    1125:	00 
    1126:	48 89 e5             	mov    rbp,rsp
    1129:	74 0c                	je     1137 <__cxa_finalize@plt+0xd7>
    112b:	48 8b 3d ee 2e 00 00 	mov    rdi,QWORD PTR [rip+0x2eee]        # 4020 <__cxa_finalize@plt+0x2fc0>
    1132:	e8 29 ff ff ff       	call   1060 <__cxa_finalize@plt>
    1137:	e8 64 ff ff ff       	call   10a0 <__cxa_finalize@plt+0x40>
    113c:	c6 05 e5 2e 00 00 01 	mov    BYTE PTR [rip+0x2ee5],0x1        # 4028 <__cxa_finalize@plt+0x2fc8>
    1143:	5d                   	pop    rbp
    1144:	c3                   	ret
    1145:	0f 1f 00             	nop    DWORD PTR [rax]
    1148:	c3                   	ret
    1149:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    1150:	f3 0f 1e fa          	endbr64
    1154:	e9 77 ff ff ff       	jmp    10d0 <__cxa_finalize@plt+0x70>
    1159:	55                   	push   rbp
    115a:	48 89 e5             	mov    rbp,rsp
    115d:	53                   	push   rbx
    115e:	48 81 ec 28 02 00 00 	sub    rsp,0x228
    1165:	48 8d 45 90          	lea    rax,[rbp-0x70]
    1169:	48 89 c6             	mov    rsi,rax
    116c:	48 8d 05 91 0e 00 00 	lea    rax,[rip+0xe91]        # 2004 <__cxa_finalize@plt+0xfa4>
    1173:	48 89 c7             	mov    rdi,rax
    1176:	b8 00 00 00 00       	mov    eax,0x0
    117b:	e8 d0 fe ff ff       	call   1050 <__isoc99_scanf@plt>
    1180:	c7 85 50 ff ff ff 3d 	mov    DWORD PTR [rbp-0xb0],0x3d
    1187:	00 00 00 
    118a:	c7 85 54 ff ff ff a4 	mov    DWORD PTR [rbp-0xac],0xa4
    1191:	00 00 00 
    1194:	c7 85 58 ff ff ff e5 	mov    DWORD PTR [rbp-0xa8],0xe5
    119b:	00 00 00 
    119e:	c7 85 5c ff ff ff 14 	mov    DWORD PTR [rbp-0xa4],0x14
    11a5:	00 00 00 
    11a8:	c7 85 60 ff ff ff c6 	mov    DWORD PTR [rbp-0xa0],0xc6
    11af:	00 00 00 
    11b2:	c7 85 64 ff ff ff f9 	mov    DWORD PTR [rbp-0x9c],0xf9
    11b9:	00 00 00 
    11bc:	c7 85 68 ff ff ff c8 	mov    DWORD PTR [rbp-0x98],0xc8
    11c3:	00 00 00 
    11c6:	c7 85 6c ff ff ff 23 	mov    DWORD PTR [rbp-0x94],0x23
    11cd:	00 00 00 
    11d0:	c7 85 70 ff ff ff 9b 	mov    DWORD PTR [rbp-0x90],0x9b
    11d7:	00 00 00 
    11da:	c7 85 74 ff ff ff 9a 	mov    DWORD PTR [rbp-0x8c],0x9a
    11e1:	00 00 00 
    11e4:	c7 85 78 ff ff ff c1 	mov    DWORD PTR [rbp-0x88],0xc1
    11eb:	00 00 00 
    11ee:	c7 85 7c ff ff ff 20 	mov    DWORD PTR [rbp-0x84],0x20
    11f5:	00 00 00 
    11f8:	c7 45 80 4e 00 00 00 	mov    DWORD PTR [rbp-0x80],0x4e
    11ff:	c7 45 84 0d 00 00 00 	mov    DWORD PTR [rbp-0x7c],0xd
    1206:	c7 45 88 42 00 00 00 	mov    DWORD PTR [rbp-0x78],0x42
    120d:	c7 45 8c 2d 00 00 00 	mov    DWORD PTR [rbp-0x74],0x2d
    1214:	c7 85 10 ff ff ff 06 	mov    DWORD PTR [rbp-0xf0],0x6
    121b:	00 00 00 
    121e:	c7 85 14 ff ff ff 42 	mov    DWORD PTR [rbp-0xec],0x42
    1225:	00 00 00 
    1228:	c7 85 18 ff ff ff 09 	mov    DWORD PTR [rbp-0xe8],0x9
    122f:	00 00 00 
    1232:	c7 85 1c ff ff ff f2 	mov    DWORD PTR [rbp-0xe4],0xf2
    1239:	00 00 00 
    123c:	c7 85 20 ff ff ff b4 	mov    DWORD PTR [rbp-0xe0],0xb4
    1243:	00 00 00 
    1246:	c7 85 24 ff ff ff f7 	mov    DWORD PTR [rbp-0xdc],0xf7
    124d:	00 00 00 
    1250:	c7 85 28 ff ff ff aa 	mov    DWORD PTR [rbp-0xd8],0xaa
    1257:	00 00 00 
    125a:	c7 85 2c ff ff ff 65 	mov    DWORD PTR [rbp-0xd4],0x65
    1261:	00 00 00 
    1264:	c7 85 30 ff ff ff a6 	mov    DWORD PTR [rbp-0xd0],0xa6
    126b:	00 00 00 
    126e:	c7 85 34 ff ff ff f5 	mov    DWORD PTR [rbp-0xcc],0xf5
    1275:	00 00 00 
    1278:	c7 85 38 ff ff ff 3c 	mov    DWORD PTR [rbp-0xc8],0x3c
    127f:	00 00 00 
    1282:	c7 85 3c ff ff ff 72 	mov    DWORD PTR [rbp-0xc4],0x72
    1289:	00 00 00 
    128c:	c7 85 40 ff ff ff 67 	mov    DWORD PTR [rbp-0xc0],0x67
    1293:	00 00 00 
    1296:	c7 85 44 ff ff ff bd 	mov    DWORD PTR [rbp-0xbc],0xbd
    129d:	00 00 00 
    12a0:	c7 85 48 ff ff ff d4 	mov    DWORD PTR [rbp-0xb8],0xd4
    12a7:	00 00 00 
    12aa:	c7 85 4c ff ff ff df 	mov    DWORD PTR [rbp-0xb4],0xdf
    12b1:	00 00 00 
    12b4:	c7 45 ec 00 00 00 00 	mov    DWORD PTR [rbp-0x14],0x0
    12bb:	eb 1d                	jmp    12da <__cxa_finalize@plt+0x27a>
    12bd:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
    12c0:	48 98                	cdqe
    12c2:	0f b6 44 05 90       	movzx  eax,BYTE PTR [rbp+rax*1-0x70]
    12c7:	0f be d0             	movsx  edx,al
    12ca:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
    12cd:	48 98                	cdqe
    12cf:	89 94 85 10 fe ff ff 	mov    DWORD PTR [rbp+rax*4-0x1f0],edx
    12d6:	83 45 ec 01          	add    DWORD PTR [rbp-0x14],0x1
    12da:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
    12dd:	48 63 d8             	movsxd rbx,eax
    12e0:	48 8d 45 90          	lea    rax,[rbp-0x70]
    12e4:	48 89 c7             	mov    rdi,rax
    12e7:	e8 44 fd ff ff       	call   1030 <strlen@plt>
    12ec:	48 39 c3             	cmp    rbx,rax
    12ef:	72 cc                	jb     12bd <__cxa_finalize@plt+0x25d>
    12f1:	48 8d 45 90          	lea    rax,[rbp-0x70]
    12f5:	48 89 c7             	mov    rdi,rax
    12f8:	e8 33 fd ff ff       	call   1030 <strlen@plt>
    12fd:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
    1300:	eb 14                	jmp    1316 <__cxa_finalize@plt+0x2b6>
    1302:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
    1305:	48 98                	cdqe
    1307:	c7 84 85 10 fe ff ff 	mov    DWORD PTR [rbp+rax*4-0x1f0],0x0
    130e:	00 00 00 00 
    1312:	83 45 e8 01          	add    DWORD PTR [rbp-0x18],0x1
    1316:	83 7d e8 3f          	cmp    DWORD PTR [rbp-0x18],0x3f
    131a:	7e e6                	jle    1302 <__cxa_finalize@plt+0x2a2>
    131c:	c7 45 e4 00 00 00 00 	mov    DWORD PTR [rbp-0x1c],0x0
    1323:	eb 5a                	jmp    137f <__cxa_finalize@plt+0x31f>
    1325:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
    1328:	48 98                	cdqe
    132a:	8b 94 85 10 fe ff ff 	mov    edx,DWORD PTR [rbp+rax*4-0x1f0]
    1331:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
    1334:	48 98                	cdqe
    1336:	8b 84 85 10 ff ff ff 	mov    eax,DWORD PTR [rbp+rax*4-0xf0]
    133d:	31 c2                	xor    edx,eax
    133f:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
    1342:	48 98                	cdqe
    1344:	8b 84 85 50 ff ff ff 	mov    eax,DWORD PTR [rbp+rax*4-0xb0]
    134b:	31 c2                	xor    edx,eax
    134d:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
    1350:	48 98                	cdqe
    1352:	89 94 85 d0 fd ff ff 	mov    DWORD PTR [rbp+rax*4-0x230],edx
    1359:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
    135c:	48 98                	cdqe
    135e:	8b 84 85 d0 fd ff ff 	mov    eax,DWORD PTR [rbp+rax*4-0x230]
    1365:	89 c6                	mov    esi,eax
    1367:	48 8d 05 99 0c 00 00 	lea    rax,[rip+0xc99]        # 2007 <__cxa_finalize@plt+0xfa7>
    136e:	48 89 c7             	mov    rdi,rax
    1371:	b8 00 00 00 00       	mov    eax,0x0
    1376:	e8 c5 fc ff ff       	call   1040 <printf@plt>
    137b:	83 45 e4 01          	add    DWORD PTR [rbp-0x1c],0x1
    137f:	83 7d e4 0f          	cmp    DWORD PTR [rbp-0x1c],0xf
    1383:	7e a0                	jle    1325 <__cxa_finalize@plt+0x2c5>
    1385:	c7 45 e0 01 00 00 00 	mov    DWORD PTR [rbp-0x20],0x1
    138c:	e9 c8 00 00 00       	jmp    1459 <__cxa_finalize@plt+0x3f9>
    1391:	c7 45 dc 00 00 00 00 	mov    DWORD PTR [rbp-0x24],0x0
    1398:	eb 42                	jmp    13dc <__cxa_finalize@plt+0x37c>
    139a:	8b 85 50 ff ff ff    	mov    eax,DWORD PTR [rbp-0xb0]
    13a0:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
    13a3:	c7 45 d8 01 00 00 00 	mov    DWORD PTR [rbp-0x28],0x1
    13aa:	eb 20                	jmp    13cc <__cxa_finalize@plt+0x36c>
    13ac:	8b 45 d8             	mov    eax,DWORD PTR [rbp-0x28]
    13af:	8d 48 ff             	lea    ecx,[rax-0x1]
    13b2:	8b 45 d8             	mov    eax,DWORD PTR [rbp-0x28]
    13b5:	48 98                	cdqe
    13b7:	8b 94 85 50 ff ff ff 	mov    edx,DWORD PTR [rbp+rax*4-0xb0]
    13be:	48 63 c1             	movsxd rax,ecx
    13c1:	89 94 85 50 ff ff ff 	mov    DWORD PTR [rbp+rax*4-0xb0],edx
    13c8:	83 45 d8 01          	add    DWORD PTR [rbp-0x28],0x1
    13cc:	83 7d d8 0f          	cmp    DWORD PTR [rbp-0x28],0xf
    13d0:	7e da                	jle    13ac <__cxa_finalize@plt+0x34c>
    13d2:	8b 45 d0             	mov    eax,DWORD PTR [rbp-0x30]
    13d5:	89 45 8c             	mov    DWORD PTR [rbp-0x74],eax
    13d8:	83 45 dc 01          	add    DWORD PTR [rbp-0x24],0x1
    13dc:	83 7d dc 02          	cmp    DWORD PTR [rbp-0x24],0x2
    13e0:	7e b8                	jle    139a <__cxa_finalize@plt+0x33a>
    13e2:	c7 45 d4 00 00 00 00 	mov    DWORD PTR [rbp-0x2c],0x0
    13e9:	eb 64                	jmp    144f <__cxa_finalize@plt+0x3ef>
    13eb:	8b 45 e0             	mov    eax,DWORD PTR [rbp-0x20]
    13ee:	c1 e0 04             	shl    eax,0x4
    13f1:	89 c2                	mov    edx,eax
    13f3:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
    13f6:	01 d0                	add    eax,edx
    13f8:	48 98                	cdqe
    13fa:	8b 94 85 10 fe ff ff 	mov    edx,DWORD PTR [rbp+rax*4-0x1f0]
    1401:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
    1404:	48 98                	cdqe
    1406:	8b 84 85 d0 fd ff ff 	mov    eax,DWORD PTR [rbp+rax*4-0x230]
    140d:	31 c2                	xor    edx,eax
    140f:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
    1412:	48 98                	cdqe
    1414:	8b 84 85 50 ff ff ff 	mov    eax,DWORD PTR [rbp+rax*4-0xb0]
    141b:	31 c2                	xor    edx,eax
    141d:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
    1420:	48 98                	cdqe
    1422:	89 94 85 d0 fd ff ff 	mov    DWORD PTR [rbp+rax*4-0x230],edx
    1429:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
    142c:	48 98                	cdqe
    142e:	8b 84 85 d0 fd ff ff 	mov    eax,DWORD PTR [rbp+rax*4-0x230]
    1435:	89 c6                	mov    esi,eax
    1437:	48 8d 05 c9 0b 00 00 	lea    rax,[rip+0xbc9]        # 2007 <__cxa_finalize@plt+0xfa7>
    143e:	48 89 c7             	mov    rdi,rax
    1441:	b8 00 00 00 00       	mov    eax,0x0
    1446:	e8 f5 fb ff ff       	call   1040 <printf@plt>
    144b:	83 45 d4 01          	add    DWORD PTR [rbp-0x2c],0x1
    144f:	83 7d d4 0f          	cmp    DWORD PTR [rbp-0x2c],0xf
    1453:	7e 96                	jle    13eb <__cxa_finalize@plt+0x38b>
    1455:	83 45 e0 01          	add    DWORD PTR [rbp-0x20],0x1
    1459:	83 7d e0 03          	cmp    DWORD PTR [rbp-0x20],0x3
    145d:	0f 8e 2e ff ff ff    	jle    1391 <__cxa_finalize@plt+0x331>
    1463:	b8 00 00 00 00       	mov    eax,0x0
    1468:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
    146c:	c9                   	leave
    146d:	c3                   	ret

Disassembly of section .fini:

0000000000001470 <.fini>:
    1470:	48 83 ec 08          	sub    rsp,0x8
    1474:	48 83 c4 08          	add    rsp,0x8
    1478:	c3                   	ret
```

How should I approach the challenge and get the flag?
The challenge author seems to be suggesting using ghidra (But I have never used it before, perhaps it's a chance to learn, what do you think?)