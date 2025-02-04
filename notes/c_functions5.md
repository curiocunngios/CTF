`pcVar1 = strchr(param_1,10);` searches for a specific character in a string:

- `strchr()` is a C string function that searches for the first occurrence of a character
- `param_1` is the string to search in
- `10` is the decimal ASCII value for newline character `\n`
- `pcVar1` will store the pointer to where the newline was found (or NULL if not found)

In C:
```c
char* pcVar1;
pcVar1 = strchr(param_1, '\n');  // same as strchr(param_1, 10)
```

Common usage is to find and remove newlines from input:
```c
char* p = strchr(buffer, '\n');
if(p != NULL) {
    *p = '\0';  // Replace newline with null terminator
}
```

So this line is likely part of input processing, probably looking for the end of a line of input to handle or remove the newline character.