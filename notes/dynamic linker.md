```less
When program starts:
- Binary has external functions like puts() but doesn't know their real addresses
- Dynamic linker (ld.so) is responsible for "linking" these at runtime

Example of first puts() call:
1. Program: "I need puts() but I only have puts@plt stub"
2. Dynamic linker: 
   - "Ok, let me check where puts is in libc.so"
   - "Found it at 0x7ffff7a649c0"
   - "I'll write this address to puts@got"
3. Now puts@got contains real address for future use
```

