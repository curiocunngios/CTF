puts_plt = 0x400560


- PLT (Procedure Linkage Table) is like a "jump table"
- When your program calls puts(), it first goes through this table
- Think of it as the "entrance" to the puts function
- We got this address from your plt command output:

```
pwndbg> plt
...
0x400560: puts@plt
...
```
