## Addresses in tcache
Teh addresses that tcache points to in the list, is different from the actual chunk address, {{aways offset by `0x10`}}. This is because tcache points to {{user data}}
The freed chunks:
```
Chunk 1: 0x6037f0  (actual chunk start, including header)
Chunk 2: 0x603880  (actual chunk start, including header)
```

Tcache entry:
```
0x603890 —▸ 0x603800
```
Because tcache stores pointers to the **USER DATA portion** of the chunk, not the **chunk header**.

So:
```
Chunk 1:
0x6037f0 (chunk start)
+ 0x10  (header size, 16 bytes)
= 0x603800 (user data, what tcache points to)

Chunk 2:
0x603880 (chunk start)
+ 0x10  (header size, 16 bytes)
= 0x603890 (user data, what tcache points to)
```