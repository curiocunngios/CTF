


## Normal flow when calling puts("hello"):
```xl
1. Code calls puts@plt
2. First time:
   puts@plt -> dynamic linker -> resolves real puts address -> stores in puts@got
   Future calls: puts@plt -> puts@got -> real puts in libc

3. So it goes: 
   puts@plt -> checks puts@got -> jumps to 0x7ffff7a649c0 (real puts in libc)
```