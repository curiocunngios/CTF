---
aliases:
  - typical functions of C
tags:
  - flashcard/active/ctf/C
---

`fgets(choice, 2, stdin)`:
It reads input from the user with these parameters
- `choice`: {{destination buffer where input will be stored}}
- `2`: {{maximum number of characters to read. 1 space is reserved for null termninator `b'\x00'`}}
- `stdin`: read from {{standard input}} <!--SR:!2025-02-21,17,292!2025-02-14,10,272!2025-02-16,12,270-->

`getchar()`:
- Reads and returns {{the next single character from the input stream}}
- usually used to {{consume the leftover newline character}} that `fgets` doesn't read <!--SR:!2025-02-14,10,271!2025-02-17,13,271-->

`char *ptr = strstr(buffer, "UwU");`:
- searches for the {{first occurrence of the string "UwU" in buffer}}
- It returns:
  - A pointer to {{the first character of "UwU" in buffer if found}}
  - {{NULL}} if "UwU" is not found in buffer <!--SR:!2025-02-11,7,251!2025-02-10,6,251!2025-02-18,14,292-->

`if (strcmp(UwU, "UwU") != 0)`:
- It means {{"If the string in variable `UwU` is NOT equal to `'UwU'`"}}
- It compares two strings {{character by character}}.
- It returns:
  - {{0}} if the strings are identical
  - {{Negative}} if first string is "less than" second string (ASCII number)
  - Positive if first string is "greater than" second string <!--SR:!2025-02-14,10,271!2025-02-10,6,251!2025-02-21,17,292!2025-02-18,14,290-->

`strtol(addr, NULL, 0)`:
- Converts the string in `addr` to a {{long integer}}
- The 0 base parameter means it {{auto-detects the base}}:
  - If string starts with "0x" -> treats as hex (base 16)
  - If starts with "0" -> treats as {{octal (base 8)}}
  - Otherwise -> treats as {{decimal (base 10)}} <!--SR:!2025-02-11,7,251!2025-02-12,8,251!2025-02-14,10,271!2025-02-16,12,271-->

`*(unsigned long long *)(void *)strtol(addr, NULL, 0))`:
- `(void *)`: {{Casts the resulting number to a void pointer}}, which means it treats the number. For example, 0x12345678 as a memory address
- `(unsigned long long *)`: Casts the void pointer to an unsigned long long pointer.
- `* operator`: {{Dereferences the pointer}} - {{reads the value at that memory address}} <!--SR:!2025-02-12,8,251!2025-02-18,14,291!2025-02-12,8,250-->


`Printing as pointer (%p)`:
```C
int *ptr = (int *)0x12345678;
printf("%p", ptr);  // Prints: 0x12345678
```
- ptr gets {{pushed onto the stack as an argument}}
- When printf sees %p, it looks for the {{next argument on the stack}}
```C
printf("%p %p");
```
- each `%p` {{moves forward to read the next value on the stack}}
```
printf("%p %p");
```
What it would do:
```
Stack (example):
[    0x11111111    ] <- First %p reads this
[    0x22222222    ] <- Second %p reads this
[    0x33333333    ]
[    0x44444444    ]
```
<!--SR:!2025-02-17,13,271!2025-02-11,7,250!2025-02-06,2,230-->

`atoi(input)`:
Converts a string (ASCII) to {{integer}}
```C
char input[] = "123";
int num = atoi(input);  
```
num becomes {{integer 123}}
```C
char input2[] = "abc";
int num2 = atoi(input2);  
```
num2 becomes {{0 (invalid input)}}
```C
char input3[] = "123abc";
int num3 = atoi(input3);  
```
num3 becomes {{integer 123 (stops at non-digit)}} <!--SR:!2025-02-16,12,271!2025-02-15,11,270!2025-02-17,13,270!2025-02-15,11,270-->

`FILE *f = fopen("flag.txt", "r")`:
- Opens a file and returns a {{file pointer}}
- "r" means open for {{reading}} <!--SR:!2025-02-14,10,270!2025-02-17,13,271-->


