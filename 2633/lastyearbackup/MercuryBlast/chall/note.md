## Observation in source 

```c
case '\x7f':
    blast(mercury);
    break;
```
`\x7f` is the `delete` character, we can send raw bytes of this via python by doing something like p.send('\xf7') to get inside

```c
void blast(char* buf) {
    read(STDIN_FILENO, buf, 0x20);
    free(buf+0x10);
}
```

- `STDIN_FILENO`: just a parameter for standard input
- write 32 bytes starting from the buffer address
- `free(buf+0x10);`: freeing from a very specifci address: `buf+0x10`, from byte 16 to bytbe 23 (8 bytes)

This could be used for:

- A double-free vulnerability if the pointer points to an already freed chunk
- A fake chunk attack if you can control the contents at the target address
- An arbitrary free if you can write a valid heap address to be freed
