```
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        PIE enabled
    Stack:      Executable
    RWX:        Has RWX segments
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```
- No got hijacking expecting __free_hook 
- shellcode injection possiion 

```
    printf("               %p               \n", &shellcode_size);
    printf("             %p             \n", *(unsigned long long *)(UwU + 0x8));
```
Here 2 addresses are leaked obviously.

Nevermind, 

```
               0x7ffcc7d570d8               
             0xe6578818e60ca400
```

The below one is not address, it is exactly the canary. Since it was dereferenced
