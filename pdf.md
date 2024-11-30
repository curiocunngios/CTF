COMP2633 Competitive Programming in Cybersecurity I
PWN 102
Shellcode and Lazy Binding
Advanced Training 4
Slides adapted from Eric Lung Sam Charles
18 Oct 2024
XU Yin Yui (@qwertyuiopp)
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Code of Ethics
- The exercises for the course should be attempted ONLY INSIDE THE SECLUDED LAB
ENVIRONMENT documented or provided. Please note that most of the attacks described in the
slides would be ILLEGAL if attempted on machines that you do not have explicit permission to
test and attack. The university, course lecturer, lab instructors, teaching assistants and the
Firebird CTF team assume no responsibility for any actions performed outside the secluded lab.
- The challenge server should be regarded as a hostile environment. You should not use your real
information when attempting challenges.
- Do not intentionally disrupt other students who are working on the challenges or disclose private
information you found on the challenge server (e.g. IP address of other students). Please let us
know if you accidentally broke the challenge.
- While you may discuss with your friends about the challenges, you must complete all the
exercises and homework by yourselves.
2
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Agenda
● Recap on previous PWN stuff
● Shellcode (aka ret2shellcode)
● More protection methods
● GOT, PLT, and Lazy binding
● Return to library (aka ret2libc)
● Homework
3


Recap on previous PWN stuff
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Last PWN Class
● Dynamic and static analysis
○ Objdump
○ ltrace, strace, gdb
● Commands in pwndbg
○ r, disass, b *, ni, si …
● Commands in pwntools
○ process, send, recv, sendline, recvline, gdb.attach, p64 …
5


Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Last PWN Class
Buffer Overflow Attack (x64)
● We can overwrite a stack frame’s return pointer to
control the instruction pointer ($rip) and jump to the
instruction you want to go
● If you can control the instruction pointer
= you can control the program flow
6


Stack High Address
Low Address
Buffer 1
Buffer 2
old rbp
old rip
Data
Shellcode (aka ret2shellcode)
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
What is shellcode?
Shellcode is code that gives you a shell when it is run in a program
If you get a shell, you can run any shell commands (e.g. ls /, cat flag.txt, rm –rf *(?), …) on the
computer that is running the program!
● e.g. install a backdoor, install malware, print a flag (in CTFs)
8


Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
How to create shellcode?
1. Write assembly code that launches a shell
2. Translate with an assembler to convert
into machine code (bytes)
9
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Shellcode
You can easily generate shellcode in pwntools
shellcraft.amd64.linux.sh() : Returns a ready-to-use assembly code to launch a shell
(in string format)
asm(shellcraft.amd64.linux.sh()) : Translates the assembly code into machine code and
returns it as bytes (48 bytes in machine code)
10
Note:
In pwntools make sure you run
context.binary = <path to binary>
 or
context.arch = ‘amd64’
before calling asm()
Reference: https://docs.pwntools.com/en/stable/shellcraft/amd64.html
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Not enough buffer space?
But sometimes, you would want the payload to be shorter, or to do other things.
So you need to make your own shellcode and translate it through asm().
Pwntools Cheatsheet: https://gist.github.com/anvbis/64907e4f90974c4bdd930baeb705dedf 11
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Running a shellcode attack
1. Inject shellcode into the program
○ Buffer overflow on stack
○ User input into an array
○ etc.
2. Set RIP to point to the starting location of the injected shellcode
3. ???
4. Profit!
12
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Attendance Flag [UwUShell]
The king of UwU is back!! ─=≡Σ((( つ•̀ω•́)つ
Can you try to get the flag? (≖ᴗ≖๑)
Hints: Buffer Overflow
You have three days to submit this flag
Due in on 22/10/2024 11:59 PM
Flags for both sessions are the same.
13
Command nc chal.firebird.sh 35026
File https://files.firebird.sh/chal-2024/06/UwUShell
Source https://files.firebird.sh/chal-2024/06/UwUShell.c
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Maybe useful in some CTF competitions…?
Other than using pwntools to generate shellcodes,
you can find some pre-built shellcodes online, like
Shell-storm : https://shell-storm.org/shellcode/index.html
Google : https://www.google.com/
…
14
More protection methods
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Protection methods
We learned about the canary and PIE in the last PWN lecture
● Canary
○ Randomized bytes that is placed between old RBP and local variables,
to prevent buffer overflow
○ If the program fins out it was changed, then it will crash!
● PIE
○ Randomizes the location of the binary in memory
i.e. the data, bss, text segment
16
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Protection methods
What other protection methods are out there that we will need to defeat?
● ASLR
● NX
● RELRO (discuss later)
Recap: You can use checksec to view the protections on a binary
17
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
PIE (Address Space Layout Randomization)
A binary-based protection that enhances the security of ASLR.
It randomizes the location of binary in memory, specifically:
● Text section: machine code instructions
● Data section: global variables
● BSS section: uninitialized global variables
If PIE is enabled, all these sections will become offset by some random number.
To bypass it, you need to leak an absolute address from these sections first to
calculate the offset
18
BSS Segment
Data Segment
Text Segment
…
Random Offset
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
ASLR (Address Space Layout Randomization)
An OS-level protection enabled on most OSes.
Every time the binary is run, the addresses of the stack, heap, and libraries are offset by some
random number.
● Makes executing our shellcode a bit more difficult because we longer know the absolute
address of our shellcode
● In Linux, you can enable it through:
echo 2 | sudo tee /proc/sys/kernel/randomize_va_space
● Or disable it by:
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
Can be defeated by leaking absolute address and calculating offsets in the respective regions.
(or NOP sled if you are lucky (not covered))
19
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
20
Random offset
BSS Segment
Data Segment
Random offset
…
1
st run
Heap
Library
Random offset
Random offset
Reserved by Kernel
Random offset
BSS Segment
Data Segment
Random offset
…
2
nd run
Heap
Library
Random offset
Random offset
Reserved by Kernel
Random offset
BSS Segment
Data Segment
Random offset
…
3
rd run
Heap
Library
Random offset
Random offset
Reserved by Kernel
Stack Stack
Stack
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
ASLR and PIE
21
ASLR ASLR + PIE PIE
Not actually randomized
due to disabled ASLR
code code code
heap heap heap
library library
library
stack stack
stack
(random)
(random)
(random)
(constant)
(random)
(random)
(random)
(random)
(constant)
(constant)
(constant)
(constant)
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
NX (No-Execute)
There are no sections in the binary that are both writeable AND executable.
If the program tries to run code in a section that is not executable, it will crash!
Most binaries will have this protection mode, meaning that the shellcode attack just now will likely
be impossible
● Unless you change a section’s rwx flags during execution… (not covered)
22
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
23
Without NX With NX
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
What we have learned
● Shellcode injection
● Protection methods
○ Canary
○ PIE
○ ASLR
○ NX
24
GOT, PLT, and Lazy binding
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Static vs Dynamic linking
C library (called libc for short) contains code for useful functions like printf(), read(), malloc()…, etc
If a program uses libc functions, it means the code of the libc functions need to be included in the
process somehow.
There are two ways of including
the library functions.
26
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Static linking
27
Entire library’s code is placed into the code section,
along with the program’s code upon compilation
When you run the program, all the library code is
already in the binary.
BSS Segment
Data Segment
Text Segment
Heap
Stack
All library code
is included here
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Dynamic linking
28
Library’s code is loaded into memory between the stack and heap
upon runtime
Main advantage over static linking: Saves a lot of space.
● No need to include a copy of the library with every binary
● If the binary already exists on a computer, it can be shared
between processes
In 64-bit binaries, the library file is usually located at
/lib/x86_64-linux-gnu/libc-<version>.so
Depending on how up-to-date your OS is, the version will be different.
● You can check by running sudo ldd --version
BSS Segment
Data Segment
Text Segment
Heap
Stack
Library
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
File size comparison
29
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
function calls in a statically linked binary
30
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
function calls in a dynamically linked binary
31
@plt ????
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
GOT and PLT
The problem in dynamic linking: We need to calculate the addresses of the functions inside libc!
● The program doesn’t know libc’s version, so the location of each function inside libc needs to be
calculated somehow
● Also, if ASLR is running, then the offset of libc will be different every time the program runs
What if go through the program’s code, and look for every libc function call, and replace the address
with the correct address in libc?
-> slow…………
32
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
GOT and PLT
Solution: Global Offset Table (GOT)
● An array of libc function addresses, that we can update as the program runs!
When the program calls a libc function,
it calls that function’s entry in the Procedure Linkage Table (PLT)
● An area in the program which contains instructions to find and jump to
 the correct address, using the GOT
GOT is an array of addresses, while PLT is a table of instructions.
33
BSS Segment
Data Segment
Text Segment
Heap
Stack
Library
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
34
Program …
Code
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
35
Program
Code
…
PLT
GOT
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
36
…
Jump to the address inside the GOT,
which points to 0x401030
Now those instructions will overwrite
the GOT with the correct address
Program
Code
PLT
GOT
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
37
Program …
Code
PLT
GOT
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
38
Program …
Code
PLT
GOT
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
39
…
dl_runtime_resolve Jump to dl_runtime_resolve,
which updates the GOT entry with the
correct libc address for puts()
Then, it jump to puts()
Program
Code
PLT
GOT
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
How does dl_runtime_resolve work?
Learn more about dl_runtime_resolve: https://syst3mfailure.io/ret2dl_resolve/ 40
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
41
…
Now the GOT entry for puts is updated!
Next time we call puts@plt again, we jump
straight to the correct address for puts()
(Tip: libc addresses usually start with 0x7f)
Program
Code
PLT
GOT
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
GOT and PLT summary
42
First call:
Later call:
call puts() PLT GOT PLT dl_runtime_resolve puts()
call puts() PLT GOT puts()
Facts: PLT → Jump to the addr. in GOT
GOT → Initially, store addr. of instruction which jump to dl_runtime_resolve
dl_runtime_resolve → calculate and overwrite addr. in GOT to runtime addr. of puts
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Lazy binding in the PLT and GOT
Lazy binding: We don’t update addresses in the GOT until we run the function for the first time!
● Depending on how the program runs, it might not need to call certain libc functions
○ e.g. an if condition, where on branch calls puts() and the other branch calls printf()
● Save time spent on calling dl_runtime_resolve
Question: What if we change the GOT by ourselves?
● If we want lazy binding to be possible, that means the GOT needs to be writeable
● GOT hijacking!
43
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
44
…
Next time you call puts(),
0xdeadbeaf evil_func() you call evil_func()
Program
Code
PLT
GOT
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Prerequisites to GOT hijacking
1. Ensure that the binary isn’t using Full RELRO
○ Stands for “Relocation Read Only”
○ Full RELRO load all address before main(), then makes GOT read-only
2. Since the GOT is located at the code section, you need to defeat PIE by leaking an address in
code or data section (unless the binary doesn’t have PIE)
3. Get arbitrary write primitive
4. Overwrite an entry in the GOT
5. Call the hijacked function
45
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Getting useful addresses in pwntools?
● elf = ELF(<path to binary>) ELF ‘object’ that contains useful info in the binary
● elf.symbols[<symbol name>] Get integer value of address of a symbol (global variable, function …)
● elf.got[<function name>] Get integer value of address of a GOT entry
● elf.address The base address of the binary
○ e.g. elf.address = leak_addr_of_main – elf.symbols[‘main’]
Reading addresses in pwntools
46
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
(btw, next slide is your favourite exercise)
Any questions?
47
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Scored Exercise [Echo Wall]
Now in front of you is the world-famous attraction, the Echo Wall! (｢･ω･)｢
If you shout ”flag”, it will echo “flag” back. (≖ᴗ≖๑)
Deadline for this is in two weeks.
Hints: How to calculate other addresses using the mysterious address on the wall?
48
Command nc chal.firebird.sh 35027
File https://files.firebird.sh/chal-2024/06/EchoWall.zip
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
More on GOT Hijacking
49
If you overwrite GOT entries with functions that take parameters, let say
puts@got -> int foo1(const char* var1)
Then later when you call puts(“/bin/sh”),
“/bin/sh” will be passed to foo1 i.e., foo1(“bin/sh”)
In such cases, you need to consider what GOT entry to overwrite to be able to
control the parameters passed.
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
What we have learned
● Static & Dynamic linking
● Lazy binding for Dynamic linking
○ PLT
○ GOT
● RELRO
○ No RELRO (GOT hijacking)
○ Partial RELRO (GOT hijacking)
○ Full RELRO (GG we cannot do hijacking )
50
Return to Library (aka ret2libc)
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Return to Library (ret2libc)
52
What if we cannot run shellcode, and the program doesn’t contain a
convenient function that prints out the flag for you?
Thankfully, there are some useful functions inside libc.
system() or execve(): Executes whatever shell command you give it
● system(“/bin/sh”): Launches a shell
● execve(“/bin/sh”, NULL, NULL): does the same thing
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Return to Library (ret2libc)
53
How do we know the address of system()?
● ASLR will randomize the base address of the entire libc code
● The program is using an unknown version of libc, so we don’t know where the function is
We will need to leak the address of any function in libc.
● We search through a database of libc versions to find the version which contains that function at
that address
● Then, with the knowledge of that leaked function’s address and the libc’s version, we can
calculate the address of system()!
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Return to Library (ret2libc)
54
BSS Segment
Heap
Stack
Library
…
base (0xf7e14000)
printf (0xf7e5d690)
system (base + 0x3ad80)
Steps to calculate the address of system()
1. printf : 0xf7e5d690 (0x49590)
2. libc base : 0xf7e5d690 - 0x49590 = 0xf7e14000
3. system : 0xf7e14000 + 0x3ad80 = 0xf7e4ed80
Try to leak this
Find the offset with tools
* libc’s base address always ends in
0x000. If it doesn’t, then you
calculated it incorrectly
(or wrong libc version)
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
system() = puts() – 0x80ed0 + 0x50d60
Return to Library (ret2libc)
55
Libc database: https://libc.rip/
Input the leaked libc address and specify which function it is, and it will find all possible versions
● Don’t need to input the entire address – last 3 or 4 bytes is fine
base addr. offset
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Return to Library (ret2libc)
56
How to leak a libc address?
● Print out an address in the GOT
○ You will need to defeat PIE first so that you know the exact address of the GOT!
● Look around on the stack for any addresses that happen to be in libc
○ return addresses that aren’t overwritten yet
○ pointers to special data structures inside libc, like fastbins or heaps
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Leaking the GOT
57
Somehow you will need to print out an entry in the GOT.
E.g. puts(0x404030), printf(0x404030), printf(“%s”, 0x404030)
● Prints out the address in bytes.
Convert bytes into integer in pwntools with int.from_bytes(<bytes string>, ‘little’)
If you can leak it as a hex string, e.g. printf(“%x”, 0x7ffff7e09400), use int(<hex string>, 16)
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Return to Library (ret2libc)
58
Now that we can calculate the address of system(), we need to be able to call it with the first
argument as “/bin/sh” (or just “sh”)
Note: libc actually contains the string “/bin/sh”, you can find it on the libc database site as well,
or use next(libc.search('/bin/sh’)) in pwntools
(you will make use of this in next pwn lecture UwU)
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Recap: Function arguments
59
When a function is called, its arguments go in order according to the table.
First argument goes into RDI, second argument into RSI, etc.
After the 6th argument, any remaining arguments are pushed onto the stack
(last one is pushed on first, until you have pushed the 7th argument on the
stack)
Arg # Location
1 RDI
2 RSI
3 RDX
4 RCX
5 R8
6 R9
7 RBP + 0x10
8 RBP + 0x18
… …
Reference: http://6.s081.scripts.mit.edu/sp18/x86-64-architecture-guide.html
Reminder:
RBP + 0x8 = old rip
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Recap: Function arguments
60
e.g.
printf(“You get a string %s! You get a string %s! Everybody gets a string %s %s!”, st1, st2, st3, st4);
RDI RSI RDX RCX R8 R9 RBP+0x10 …
Address of
“You get
a…”
Address of
st1
Address of
st2
Address of
st3
Address of
st4
Doesn’t
matter
Doesn’t
matter
Doesn’t
matter
Reference: http://6.s081.scripts.mit.edu/sp18/x86-64-architecture-guide.html
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
How to call system(“/bin/sh”)?
61
system(“/bin/sh”)
RDI RSI RDX RCX R8 R9 RBP+0x10 …
Address of
a string
with
“/bin/sh”
Doesn’t
matter
Doesn’t
matter
Doesn’t
matter
Doesn’t
matter
Doesn’t
matter
Doesn’t
matter
Doesn’t
matter
You can somehow change RDI to be the address of the “/bin/sh” string inside libc
Or if you can’t change the value of RDI, you could change the value inside the memory it points to instead!
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
“Echo” Exercise [Echo Wall]
When the wall is repaired, you are back here, the Echo Wall! Again! (｢･ω･)｢
Can you still get the flag without "UwU_win()" ? (≖ᴗ≖๑)
Hints: GOT hijacking with ret2libc!
62
Command nc chal.firebird.sh 35027
File https://files.firebird.sh/chal-2024/06/EchoWall.zip
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
OneGadget
63
Quick shortcut for getting a shell
Checks a version of libc and looks for any code that
launches a shell inside the library
(by calling execve(“/bin/sh”, NULL, NULL))
If you can set the RIP to the onegadget and ensure the
requirements are fulfilled, then you can pwn!
Github Repo: https://github.com/david942j/one_gadget
Homework
Again, Your Favourite Part :)
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
UwUShell-- (HW 6A-i)
You successfully arrived in front of the king of UwU! ─=≡Σ((( つ•̀ω•́)つ
Can you make him marvel at the power of your shellcode and get the flag? (≖ᴗ≖๑)
65
Command nc chal.firebird.sh 35028
File https://files.firebird.sh/chal-2024/06/UwUShell--
Source https://files.firebird.sh/chal-2024/06/UwUShell--.c
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
If your shellcode is too long to fit in the buffer, there are some common solutions:
1. pop & push instead of mov
• be careful that don’t overwrite your shellcode when using push
2. Use “smaller register”
• only if the higher bits of the register are already the values you want
3. xor reg, reg instead of mov reg, 0
4. Make use of existing value (value on stack/register)
5. “Link” multiple buffers through jmp
6. ……
Tips for shorten shellcode
66
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Examples:
1. pop & push instead of mov
2. Use “smaller register”
3. xor reg, reg instead of mov reg, 0
4. Make use of existing value
5. “Link” multiple buffer by using jmp
6. ……
Shorter shellcode (cont.)
67
mov rax, 0x1
(7 bytes)
push 0x1
pop rax
(3 bytes)
sub rax, 16
(4 bytes)
sub al, 16
(2 bytes)
mov rsi, 0
(7 bytes)
xor rsi, rsi
(3 bytes)
jmp rax
/
jmp .+0x30
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
1. Here is the visualization of UwU_main’s stack frame (maybe helpful?)
2. If you cannot construct a short enough shellcode by yourself,
Google is powerful (but you still need to modify it to fit in the stack)
3. Make use of every modifiable space!
For code golf:
1. Do we have to put the "/bin/sh" part in shellcode?
Free hints release to celebrate midterm!
68
canary
…….
variable 1
variable 2
old rbp
old rip (return addr)
…….
direction of
data writing
and
program
execution
(High address)
(Low address)
Figure out the size and who they are by yourself!
ρ(・ω・、)
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Game of UwU (HW 6A-ii)
Do you want to Play a game!! (❍ᴥ❍ʋ)
Let play "Game of UwU”
Hint: GOT hijacking by relative write ( ～'ω')～
69
Command nc chal.firebird.sh 35029
File https://files.firebird.sh/chal-2024/06/GameOfUwU.zip
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Notes for Game of UwU
Since the server binary is unable to use gdb to debug because of system("clear"),
the king of UwU is so nice that gives you a version for you to debug
GameOfUwU_noclear https://files.firebird.sh/chal-2024/06/GameOfUwU_noclear.zip
Both Exercise & Homeworks are due in two weeks:
November 1st 11:59 PM
70
Notes from the next Track A class
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
ROPGadget
72
Next week, we will be teaching how to do Return-Oriented Programming (ROP) (an extremely fun topic)
ROPGadget will be very handy for us to find the addresses of different gadgets used in ROP
If you used my shell script provided in week 4, it should have been installed on your computer
If not, just type sudo pip install ropgadget in your kali linux to install it
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
What we have learned
1. Control the program flow
○ Buffer overflow
■ overwrite return address
○ GOT hijacking
■ only if No/Partial RELRO
2. Get the Shell
○ ret2win
■ Only if author kindly enough
○ ret2shellcode
■ Only if NX disable
○ ret2libc
■ need to care about the function parameter (ROP  next pwn class)
■ unless the one-gadget works
73
Thank You for Listening!!!
If you have any questions, feel free to
DM us, or email us.
Zoom - Next Up:
Track B: Crypto 102
Appendix A - Docker 101
If I already overrun, you may need to read it by yourself
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
What is Docker
76
Docker provides a virtual environment.
It creates isolated containers that simulate environments for applications.
● In most of the real CTF competitions, they only provide the Dockerfile, but not libc file.
● Instead of leaking address and searching version on libc database, you can directly grab the libc
file from the docker if Dockerfile is provided
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Install Docker on kali
77
Install docker:
● sudo apt update
● sudo apt install -y docker.io
● sudo systemctl enable docker –now
Add yourself to the docker group (so that you don’t need to add sudo when using docker command
● sudo usermod -aG docker $USER
You may run this to check if docker is installed successfully:
● docker --version
Source: https://www.kali.org/docs/containers/installing-docker-on-kali/
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Grab libc from docker
78
Build a temporary container running the same Ubuntu version as the Dockerfile.
● docker run -it --rm -v $(pwd):/chal --platform linux/amd64 <image-version>
Example: Image-version:
ubuntu:22.04
docker run -it --rm -v $(pwd):/chal --platform linux/amd64 ubuntu:22.04
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Grab libc from docker (Cont.)
Now we already build a temporary container by using
● docker run -it --rm -v $(pwd):/chal --platform linux/amd64 ubuntu:22.04
● The parameter –v $(pwd):/chal will “link” your local folder to /chal file in the container
● /chal in docker and ~/Desktop/GameOfUwU in local machine share same content
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Grab libc from docker (Cont.)
Copy libc.so.6 into /chal folder
● Always don’t use mv don’t ask me why I mention this.
● Libc file path:
○ /lib/x86_64-linux-gnu/libc.so.6
● cp /lib/x86_64-linux-gnu/libc.so.6 /chal
● Now the libc file should be found on your local machine
● Patch the ELF with this libc (e.g pwninit)
● Happy pwning ~ This stupid guy do mv <libc file> <somewhere>
on his local kali machine
Firebird CTF Team COMP2633 Competitive Programming in Cybersecurity I
Conclusion
81
1. Identify the image version in Dockerfile
2. Run docker run -it --rm -v $(pwd):/chal --platform linux/amd64 <image-version>
3. Run cp /lib/x86_64-linux-gnu/libc.so.6 /chal
4. Now you should see the libc file in your folder