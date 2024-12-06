# Normal flow of function return 

```
Before return:
[Local Variables] <- Lower addresses
[Saved RBP     ]
[Return Address] <- RSP (Stack Pointer) points here
[...]          ] <- Higher addresses

When ret instruction executes:
- CPU pops return address from stack
- Jumps to that address
```