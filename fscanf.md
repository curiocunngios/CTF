# `__isoc99_fscanf` 

It is the internal name for the `fscanf` function in C that follows the ISO C99 standard. It's essentially the same as `fscanf`.

The function reads formatted input from a stream according to a format string. In this case:

- `local_18` is likely a FILE pointer (the input stream)
- `&DAT_00102014` is probably the format string (like "%d", "%s", etc.) stored at that memory address
- `&local_20` is the address where the scanned value will be stored

This is similar to `scanf` but instead of reading from standard input (stdin), it reads from a specified file stream.

Looking at the decompiled code, this is probably equivalent to something like:
```c
fscanf(file_pointer, format_string, &variable);
```

Without seeing more context (like what's at `DAT_00102014`), I can't tell exactly what format is being read, but it's likely reading some kind of input value from a file and storing it in the variable `local_20`.

Would you like me to explain more about how fscanf works or would you like to share more context about the challenge?