puts_got = 0x601018:

- GOT (Global Offset Table) stores the real addresses of functions
- When puts is called first time, its real address is stored here
- We got this from your got command output:

```
pwndbg> got
...
[0x601018] puts@GLIBC_2.2.5 ...
...
```
