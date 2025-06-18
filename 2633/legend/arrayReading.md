# `read` array reading 

On the stack (which grows downward), "after" means higher addresses. Here's a visual of your stack frame:  

```asciidoc
Higher addresses
+------------------+
| day[3]           |
| day[2]           |
| day[1]           |
| day[0]           |
+------------------+
| buffer[23]       |
| ...              |
| buffer[0]        |
+------------------+
| canary           |
+------------------+
Lower addresses
```
When puts(buffer) runs, it reads upward (toward higher addresses) until it finds a null byte.  


Yo i actually did it 
```
[*] Switching to interactive mode
 of the last day
24 hours remaining
So this is what you tried to do to escape?
BBBBBBBBBBBBBBBBBBBBBBBB
3 days have passedDawn of the first day
72 hours remaining

```


first loop
day1: leak canary
day2: leak return address (for calculating base address to defeat pie)
day3 (last day): go into second loop with stack alignment

Second loop
day1: did nothing lol was kinda just testing, the overflow seems quite weird here that it doesn't cover the previous overwrite
day2: leak return address( this time for libc function leak, because the return address is `__libc_start_main` a libc function)
day3: get into system with day2's libc base leak 