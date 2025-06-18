# unsetenv 
I have implemented an environment variable reader. What could possibly go wrong?

unsetenv.zip

`nc ash-chal.firebird.sh 36013`

```
Enter the name of an environment variable: ASDFASDFA
The value of the environment variable ASDFASDFA
,L�G is (null).
Enter the name of an environment variable: ASDF
The value of the environment variable ASDF
SDFA
,L�G is (null).
Enter the name of an environment variable: ASDFASDFADSF
The value of the environment variable ASDFASDFADSF
L�G is (null).
Enter feedback for this challenge below:
ASDFADSFASDF
Thanks for your feedback!
*** stack smashing detected ***: terminated
zsh: IOT instruction  ./unsetenv
```
It is just like 7a homework 

## unsetenv 
```c

undefined8 main(void)

{
  char *env;
  long in_FS_OFFSET;
  int i;
  char buffer [8];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  setbuf(stdin,(char *)0x0);
  setbuf(stdout,(char *)0x0);
  setbuf(stderr,(char *)0x0);
  unsetenv("FLAG");
  i = 3;
  while( true ) {
    if (i == 0) break;
    printf("Enter the name of an environment variable: ");
    read(0,buffer,0x20);
    env = getenv(buffer);
    printf("The value of the environment variable %s is %s.\n",buffer,env);
    i = i + -1;
  }
  puts("Enter feedback for this challenge below:");
  read(0,buffer,0x30);
  puts("Thanks for your feedback!");
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```
## spawn 
```c

undefined8 main(void)

{
  long fs_offset;
  char *output;
  FILE *f;
  long canary;
  
  canary = *(long *)(fs_offset + 0x28);
  f = fopen("/app/flag.txt","r");
  output = (char *)0x0;
  __isoc99_fscanf(f,&%ms,&output);
  fclose(f);
  setenv("FLAG",output,1);
  free(output);
  setuid(1000);
  execl("/app/unsetenv","unsetenv",0);
  if (canary != *(long *)(fs_offset + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

## Checksec 

```
┌──(kali㉿kali)-[~/Desktop/CTF/lastyearbackup/unsetenv]
└─$ checksec unsetenv 
[*] '/home/kali/Desktop/CTF/lastyearbackup/unsetenv/unsetenv'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
```
- No GOT hijacking 
- need to leak canary to be able to do buffer overflow and return 
- No shellcode injection 
- need to leak some .text addresses to defeat PIE 

The buffer size is 8 bytes, but the prgoram allows us to input in total of 0x50 bytes, easily a problem about overflowing 


```as
   0x0000000000001218 <+127>:	lea    rax,[rbp-0x10]
   0x000000000000121c <+131>:	mov    edx,0x20
   0x0000000000001221 <+136>:	mov    rsi,rax
   0x0000000000001224 <+139>:	mov    edi,0x0
   0x0000000000001229 <+144>:	call   0x1080 <read@plt>
```

`buffer` is at `rbp-0x10`


```
pwndbg> x/32xb $rbp-0x10
0x7fffffffdb00:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x0a
0x7fffffffdb08:	0x00	0x92	0xb4	0x3a	0x59	0x7c	0x46	0x2d
0x7fffffffdb10:	0x01	0x00	0x00	0x00	0x00	0x00	0x00	0x00
0x7fffffffdb18:	0x68	0x9d	0xdd	0xf7	0xff	0x7f	0x00	0x00
```

here
- `0x7fffffffdb08` is canary
- `0x0a` is newline character 

# to do:
- leak canary
1. sendline 8 'A's
2. then let's see what `%s` in printf would do for us  
3. When I entered 7 'A's with newline character on the last byte of `$rbp-0x10`, the output was just:

```
pwndbg> ni
The value of the environment variable AAAAAAA
is (null).
```
But when I input something 8 'A's with the last byte replacing the null byte of the canary, the output is 
```
pwndbg> ni
The value of the environment variable AAAAAAAA
��:Y|F- is (null).
```

It seems to be really similar to `puts` printing until the null byte is met, but the actual code is the following (decompiled with ghidra), how?
```c

    read(0,buffer,0x20);
    env = getenv(buffer);
    printf("The value of the environment variable %s is %s.\n",buffer,env);
```

claude: `This is happening because getenv and printf both rely on null-terminated strings.` 

`printf will keep printing characters for the %s format until it hits a null byte`



# to do 2:

now I got both the return address leaked and the canary, we can do the buffer overflow

But before that, theres one more round of "enter the name of an environment variable, let's see what else we can get here, I am expecting a libc function on the stack?

oh wait

what I have just leaked: `0x7f648cb5bd68` was just a libc address 

```
00:0000│ rsp 0x7fff4816a110 ◂— 0
01:0008│-018 0x7fff4816a118 ◂— 0x18cd67030
02:0010│-010 0x7fff4816a120 ◂— 0x4141414141414141 ('AAAAAAAA')
03:0018│-008 0x7fff4816a128 ◂— 0x4141414141414141 ('AAAAAAAA')
04:0020│ rbp 0x7fff4816a130 ◂— 0xa41414141414141 ('AAAAAAA\n')
05:0028│+008 0x7fff4816a138 —▸ 0x7f648cb5bd68 (__libc_start_call_main+120) ◂— mov edi, eax
06:0030│+010 0x7fff4816a140 —▸ 0x7fff4816a230 —▸ 0x7fff4816a238 ◂— 0x38 /* '8' */
07:0038│+018 0x7fff4816a148 —▸ 0x55dd1d612199 (main) ◂— push rbp
```
it is `07:0038│+018 0x7fff4816a148 —▸ 0x55dd1d612199 (main) ◂— push rbp` the main address lol 

so anyways, it returns to `__libc_start_call_main` after the function which is normal as it is not a function called by main, the function is just `main` itself

what we can do here:
1. grab the remain address
2. overwrite the return address back to main
3. do bad things again

Or:
just use the leaked libc function address to calculate libc system and we ret2libc at the feedback section



the few problems which I have encountered :

1. libc I got from dockerfile seems to be problematic 
```
┌──(kali㉿kali)-[~/Desktop/CTF/lastyearbackup/unsetenv]
└─$ ./unsetenv_patched
./unsetenv_patched: ./libc.so.6: version `GLIBC_2.34' not found (required by ./unsetenv_patched)
```
2. libc.sym['__libc_start_call_main'] do not get me the offset of the symbol, key missing even tho it should be a libc address 
3. cannot leak `.text` addresses i.e. `main` before feedback to get the correct elf.address for elf.plt/got['func']



# todo3

1. get correct libc, 2.38
2. get libc base 
3. finds ways to execute `spawn`, whether patching, creating /app/flag.txt etc.   


# options 

1. recommended to try and perhaps debug inside the docker `
2. leak .text and stack address and do bad things with them 
3. rop chain to find FLAG string and put it back inside the getenv 
4. look through stack one line by line via `ni` see how the variable is unset 


when the flag is FLAG=aaabbb 
```
0x7ff392683612 <puts+114>    mov    rsi, rbp       RSI => 0x7fff3a2c4fc7 ◂— 0x6161613d47414c46 ('FLAG=aaa')
► 0x7ff392683615 <puts+117>    call   qword ptr [r14 + 0x38]      <_IO_file_xsputn>
  rdi: 0x7ff3927ff5c0 (_IO_2_1_stdout_) ◂— 0xfbad2887
  rsi: 0x7fff3a2c4fc7 ◂— 'FLAG=aaabbb'
  rdx: 0xb
  rcx: 0x7ff39271b214 (write+20) ◂— cmp rax, -0x1000 /* 'H=' */
```

when the flag is FLAG=flag{testing_testing~}
```
  0x7f9c4f283612 <puts+114>    mov    rsi, rbp       RSI => 0x7ffcb0db7fc7 ◂— 0x6e69747365745f67 ('g_testin')
 ► 0x7f9c4f283615 <puts+117>    call   qword ptr [r14 + 0x38]      <_IO_file_xsputn>
        rdi: 0x7f9c4f3ff5c0 (_IO_2_1_stdout_) ◂— 0xfbad2887
        rsi: 0x7ffcb0db7fc7 ◂— 'g_testing~}'
        rdx: 0xb
        rcx: 0x7f9c4f31b214 (write+20) ◂— cmp rax, -0x1000 /* 'H=' */
```

