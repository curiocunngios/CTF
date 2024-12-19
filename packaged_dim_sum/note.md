# CTF Challenge description: 

## Title: Packaged dim sum
```
I ate some dim sum with my:

    brain ❌
    fork ❌
    chopsticks ✔️

Then some code ran in my stomach. Help me take it out :(
[the dim_sum I ate](zip file)
```

# The zip folder contains
## code.txt
```
this file contains 4 repeating chinese characters "山竹牛肉", some characters are the same but not exactly the same. For  example, a 山 could be larger than the other, like a varirant
```

## dim_sum 
which seems to be doing nothing when I tried running it
```
┌──(kali㉿kali)-[~/Desktop/CTF/5A_attendance]
└─$ ls -l dim_sum 
-rw-rw-r-- 1 kali kali 7256 Oct  2 07:52 dim_sum
                                                                                         
┌──(kali㉿kali)-[~/Desktop/CTF/5A_attendance]
└─$ gdb ./dim_sum   
GNU gdb (Debian 15.2-1) 15.2
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
pwndbg: loaded 175 pwndbg commands and 47 shell commands. Type pwndbg [--shell | --all] [filter] for a list.                                                                      
pwndbg: created $rebase, $base, $hex2ptr, $bn_sym, $bn_var, $bn_eval, $ida GDB functions (can be used with print/break)                                                           
Reading symbols from ./dim_sum...
(No debugging symbols found in ./dim_sum)
------- tip of the day (disable with set show-tips off) -------
Use track-got enable|info|query to track GOT accesses - useful for hijacking control flow via writable GOT/PLT
pwndbg> r
Starting program: /home/kali/Desktop/CTF/5A_attendance/dim_sum 
zsh:1: permission denied: /home/kali/Desktop/CTF/5A_attendance/dim_sum
During startup program exited with code 126.

```


Both objdump and hexdump shows just the following and nothing else
```

dim_sum:     file format elf64-x86-64

```
## Opening with ghidra
decompiler shows functions like this, some lines are just `??` so I removed them  

```

/* WARNING: Removing unreachable block (ram,0x00105662) */
/* WARNING: Removing unreachable block (ram,0x001058f1) */
/* WARNING: Removing unreachable block (ram,0x001056e7) */
/* WARNING: Removing unreachable block (ram,0x001058b4) */
/* WARNING: Removing unreachable block (ram,0x001058ce) */
/* WARNING: Removing unreachable block (ram,0x001058d4) */
/* WARNING: Removing unreachable block (ram,0x001058d0) */
/* WARNING: Removing unreachable block (ram,0x001058e7) */
/* WARNING: Removing unreachable block (ram,0x001056fe) */
/* WARNING: Removing unreachable block (ram,0x00105709) */
/* WARNING: Removing unreachable block (ram,0x001057f0) */
/* WARNING: Removing unreachable block (ram,0x00105714) */
/* WARNING: Removing unreachable block (ram,0x0010571f) */
/* WARNING: Removing unreachable block (ram,0x001057bf) */
/* WARNING: Removing unreachable block (ram,0x0010572a) */
/* WARNING: Removing unreachable block (ram,0x00105735) */
/* WARNING: Removing unreachable block (ram,0x00105830) */
/* WARNING: Removing unreachable block (ram,0x00105740) */
/* WARNING: Removing unreachable block (ram,0x0010574b) */
/* WARNING: Removing unreachable block (ram,0x00105860) */
/* WARNING: Removing unreachable block (ram,0x00105756) */
/* WARNING: Removing unreachable block (ram,0x00105761) */
/* WARNING: Removing unreachable block (ram,0x0010587f) */
/* WARNING: Removing unreachable block (ram,0x00105899) */
/* WARNING: Removing unreachable block (ram,0x0010589f) */
/* WARNING: Removing unreachable block (ram,0x0010589b) */
/* WARNING: Removing unreachable block (ram,0x001058b2) */
/* WARNING: Removing unreachable block (ram,0x001058ea) */
/* WARNING: Removing unreachable block (ram,0x0010576c) */
/* WARNING: Removing unreachable block (ram,0x00105777) */
/* WARNING: Removing unreachable block (ram,0x0010578e) */
/* WARNING: Removing unreachable block (ram,0x0010577e) */
/* WARNING: Removing unreachable block (ram,0x00105810) */
/* WARNING: Removing unreachable block (ram,0x00105789) */
/* WARNING: Removing unreachable block (ram,0x001058ed) */
/* WARNING: Removing unreachable block (ram,0x00105905) */
/* WARNING: Removing unreachable block (ram,0x00105a6f) */
/* WARNING: Removing unreachable block (ram,0x00105992) */
/* WARNING: Removing unreachable block (ram,0x0010599c) */
/* WARNING: Removing unreachable block (ram,0x001059b5) */
/* WARNING: Removing unreachable block (ram,0x00105a0f) */
/* WARNING: Removing unreachable block (ram,0x00105a67) */
/* WARNING: Removing unreachable block (ram,0x00105a7e) */
/* WARNING: Removing unreachable block (ram,0x00105b3e) */
/* WARNING: Removing unreachable block (ram,0x00105bf0) */
/* WARNING: Removing unreachable block (ram,0x00105bbf) */
/* WARNING: Removing unreachable block (ram,0x00105b0a) */

undefined8 FUN_0010563d(void)

{
  return 0x15;

void FUN_00105e97(undefined4 *param_1,undefined8 param_2,undefined8 param_3,uint param_4)

{
  undefined4 uVar1;
  uint uVar2;
  undefined4 *puVar3;
  undefined uVar4;
  ulong unaff_RBP;
  
  puVar3 = (undefined4 *)((long)param_1 + unaff_RBP);
  uVar4 = *(undefined *)puVar3;
  if ((5 < param_4) && (unaff_RBP < 0xfffffffffffffffd)) {
    uVar2 = param_4 - 4;
    do {
      param_4 = uVar2;
      uVar1 = *puVar3;
      puVar3 = puVar3 + 1;
      *param_1 = uVar1;
      param_1 = param_1 + 1;
      uVar2 = param_4 - 4;
    } while (3 < param_4);
    uVar4 = *(undefined *)puVar3;
    if (param_4 == 0) {
      return;
    }
  }
  do {
    puVar3 = (undefined4 *)((long)puVar3 + 1);
    *(undefined *)param_1 = uVar4;
    param_4 = param_4 - 1;
    uVar4 = *(undefined *)puVar3;
    param_1 = (undefined4 *)((long)param_1 + 1);
  } while (param_4 != 0);
  return;
}


long FUN_00105ed5(uint *param_1,uint *param_2,undefined8 param_3,ulong param_4,char param_5,
                 undefined8 param_6,long param_7,int param_8,int *param_9)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  ulong uVar5;
  uint extraout_EDX;
  undefined8 extraout_RDX;
  undefined8 uVar6;
  uint unaff_EBX;
  ulong unaff_RBP;
  uint *puVar7;
  byte bVar8;
  bool bVar9;
  byte bVar10;
  undefined auVar11 [16];
  code *unaff_retaddr;
  
  puVar7 = param_1;
  if (param_5 != '\x02') {
LAB_00105f6b:
    *param_9 = (int)puVar7 - param_8;
    return (long)param_1 - param_7;
  }
  do {
    while( true ) {
      bVar10 = *(byte *)param_2;
      bVar8 = CARRY4(unaff_EBX,unaff_EBX);
      unaff_EBX = unaff_EBX * 2;
      if (unaff_EBX == 0) {
        uVar3 = *param_2;
        bVar9 = param_2 < (uint *)0xfffffffffffffffc;
        param_2 = param_2 + 1;
        bVar8 = CARRY4(uVar3,uVar3) || CARRY4(uVar3 * 2,(uint)bVar9);
        unaff_EBX = uVar3 * 2 + (uint)bVar9;
        bVar10 = *(byte *)param_2;
      }
      puVar7 = param_1;
      if (!(bool)bVar8) break;
      param_2 = (uint *)((long)param_2 + 1);
      *(byte *)param_1 = bVar10;
      param_1 = (uint *)((long)param_1 + 1);
    }
    do {
      iVar1 = (*unaff_retaddr)();
      uVar4 = (uint)param_4;
      uVar2 = iVar1 * 2 + (uint)bVar8;
      bVar8 = CARRY4(unaff_EBX,unaff_EBX);
      unaff_EBX = unaff_EBX * 2;
      uVar3 = extraout_EDX;
      if (unaff_EBX == 0) {
        uVar3 = *param_2;
        bVar9 = param_2 < (uint *)0xfffffffffffffffc;
        param_2 = param_2 + 1;
        bVar8 = CARRY4(uVar3,uVar3) || CARRY4(uVar3 * 2,(uint)bVar9);
        unaff_EBX = uVar3 * 2 + (uint)bVar9;
        uVar3 = (uint)*(byte *)param_2;
      }
    } while (!(bool)bVar8);
    bVar10 = uVar2 < 3;
    if (!(bool)bVar10) {
      param_1 = (uint *)((long)param_2 + 1);
      bVar10 = false;
      uVar3 = ((uVar2 - 3) * 0x100 | uVar3 & 0xff) ^ 0xffffffff;
      if (uVar3 == 0) goto LAB_00105f6b;
      unaff_RBP = (ulong)(int)uVar3;
      param_2 = param_1;
    }
    (*unaff_retaddr)();
    bVar8 = CARRY4(uVar4,uVar4) || CARRY4(uVar4 * 2,(uint)bVar10);
    iVar1 = uVar4 * 2 + (uint)bVar10;
    auVar11 = (*unaff_retaddr)();
    uVar6 = auVar11._8_8_;
    uVar3 = auVar11._0_4_;
    uVar2 = iVar1 * 2 + (uint)bVar8;
    if (uVar2 == 0) {
      uVar5 = auVar11._0_8_ & 0xffffffff;
      bVar10 = 0xfffffffd < uVar3;
      do {
        iVar1 = (int)uVar5;
        uVar3 = (*unaff_retaddr)();
        uVar2 = iVar1 * 2 + (uint)bVar10;
        uVar5 = (ulong)uVar2;
        bVar10 = CARRY4(unaff_EBX,unaff_EBX);
        unaff_EBX = unaff_EBX * 2;
        if (unaff_EBX == 0) {
          uVar4 = *param_2;
          bVar9 = param_2 < (uint *)0xfffffffffffffffc;
          param_2 = param_2 + 1;
          bVar10 = CARRY4(uVar4,uVar4) || CARRY4(uVar4 * 2,(uint)bVar9);
          unaff_EBX = uVar4 * 2 + (uint)bVar9;
        }
        uVar6 = extraout_RDX;
      } while (!(bool)bVar10);
    }
    uVar3 = uVar2 + uVar3 + (uint)(unaff_RBP < 0xfffffffffffff300);
    param_4 = (ulong)uVar3;
    FUN_00105e97(puVar7,param_2,uVar6,uVar3);
    param_1 = puVar7;
  } while( true );
}


void FUN_00106054(void)

{
  uint uVar1;
  ulong uVar2;
  code *unaff_RBP;
  long unaff_retaddr;
  ulong local_20;
  long lStack_18;
  undefined8 uStack_10;
  undefined8 local_8;
  
  syscall();
  uVar1 = *(uint *)(unaff_retaddr + 0x13);
  lStack_18 = (long)(unaff_RBP + -0xb) - (ulong)*(uint *)(unaff_RBP + -0xb);
  uStack_10 = 2;
  syscall();
  local_8 = 9;
  local_20 = (ulong)*(uint *)(unaff_retaddr + 0x13);
  (*unaff_RBP)(unaff_retaddr + 0x1f,*(undefined4 *)(unaff_retaddr + 0x17),9,&local_20,
               *(undefined4 *)(unaff_retaddr + 0x1b),0);
  uVar2 = local_20;
  local_20 = 10;
  syscall();
  (*(code *)0x9)(local_8,uVar1,5,uVar2);
  return;
}

/* WARNING: Control flow encountered bad instruction data */

void FUN_001060d0(void)

{
  FUN_00106054();
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}
```

commands I tested with the elf dim_sum 
```
┌──(kali㉿kali)-[~/Desktop/CTF/5A_attendance]
└─$ strings dim_sum     
UPX!
tdoG
/lib64
nux-x86-
so.2
mgUa
aCb/o
ocal    __cxa_f
trcspn
art_ma
fope
_k>CNch!
puts
fflush,diDi
c99^wslnf'/o<
C_2.7   34
JITM_debgRt
_*(     }
d@`L
PTE1
u+UH
zh_HK.UTF8
code.txt
Input t
he pass': 
You didn't
? sanity c(ck!7Now i
bory'g har
Great
! Mayb6ydsh
ld use
;*3$"?D
2Vfv
USQRH
W^YH
PROT_EXEC|PROT_WRITE failed.
_j<X
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
$Id: UPX 4.22 Copyright (C) 1996-2024 the UPX Team. All Rights Reserved. $
_RPWQM)
j"AZR^j
PZS^
/proc/self/exe
IuDSWH
s2V^
XAVAWPH
YT_j
AY^_
D$ [I
UPX!u
slIT$}
}aw993u
([]A\A]
I[8k
(L      "
tL      n
+xHf
p(E1[$1
fFj9
~*"|]
I5(Ag
@bQs
 k1(
=(I[u
A^A_)
m@S r6
ck5?
JAPC
JG=,1
SRVW
RY?WVj,4
GCC: (Debian 13.2.0-
.shstrtab       interp
/.gnu.prop
build-idABI-;g
[;haK   dynsym
vEsion
rela(   plt
$odam
eh_frame_hl
:_ar
y1{on
}6Gbss
com;
QC'/
}Spa
UPX!
UPX!

┌──(kali㉿kali)-[~/Desktop/CTF/5A_attendance]
└─$ ls -la dim_sum
-rwxrwxr-x 1 kali kali 7256 Oct  2 07:52 dim_sum
                                                                                         
┌──(kali㉿kali)-[~/Desktop/CTF/5A_attendance]
└─$ file dim_sum 
dim_sum: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), statically linked, no section header
```


readelf dump:
```
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Shared object file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x5e60
  Start of program headers:          64 (bytes into file)
  Start of section headers:          0 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         3
  Size of section headers:           0 (bytes)
  Number of section headers:         0
  Section header string table index: 0

There are no sections in this file.

There are no section groups in this file.

Program Headers:
  Type           Offset             VirtAddr           PhysAddr
                 FileSiz            MemSiz              Flags  Align
  LOAD           0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000001000 0x0000000000004090  RW     0x1000
  LOAD           0x0000000000000000 0x0000000000005000 0x0000000000005000
                 0x000000000000192d 0x000000000000192d  R E    0x1000
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RW     0x10

There is no dynamic section in this file.

There are no relocations in this file.
No processor specific unwind information to decode

Dynamic symbol information is not available for displaying symbols.

No version information found in this file.
```

How can i proceed with the challenge?