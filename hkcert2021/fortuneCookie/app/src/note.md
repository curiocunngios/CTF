# vulnerabilities 

```c
void read_cookie() {
    long long idx;
    
    printf("Which cookie?[0-%d]: ", cookie_num-1);
    scanf("%llu", &idx);


    // allows negative index 
    if (idx >= cookie_num) {
        _abort("Invalid index!");
    }

    printf("%s\n\n", msg[idx]);
}
```
allows reading negative indexed arrays, reading secret memory regions
# checksec 
```
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
```
- no GOT hijacking except `free`
