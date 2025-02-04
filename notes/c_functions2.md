---
aliases:
  - typical functions of C 2
tags:
  - flashcard/active/ctf/C
---

`scanf("%llu", &shellcode_size)`:
1. `%llu` means:
- ll = {{"long long"}} (typically 64-bit)
- u = {{"unsigned"}}
- Combined: reads an unsigned long long integer
2. &shellcode_size is:
- The {{address}} where the input number will be stored
- Must match the format specifier type <!--SR:!2025-02-19,14,290!2025-02-19,14,290!2025-02-06,2,230-->

`sprintf(buffer1, "Wlid %s appeared!", encountered);`:
- `sprintf` {{writes formatted text to a string buffer}}
1. `buffer1`: {{destination buffer where the result will be stored}}
2. `"Wild %s appeared!"`: {{format string where %s is a placeholder for a string, this goes into destination buffer}}
3. `encountered`: {{string that will replace %s}} <!--SR:!2025-02-14,10,270!2025-02-16,12,270!2025-02-21,16,290!2025-02-17,13,270-->

`strcpy(buffer2, "");`:
- `strcpy`: {{It copies the empty string "" to the buffer}}
- Now buffer2 contains {{'\0' the null terminator}} <!--SR:!2025-02-18,13,290!2025-02-22,17,290-->

`printf("| %-10s |\n", "Hi");`:
```c
printf("| %-10s |\n", "Hi");    // "| Hi        |"
printf("| %10s |\n", "Hi");     // "|         Hi|"
```
- `%-10s` : {{left-aligns the text padded with white spaces}} <!--SR:!2025-02-13,9,270-->


`rand() % 6`:
- generate a number {{between 0 and 5, inclusive}}
- `rand()`: Generates a random integer (typically 0 to RAND_MAX, which is often 32767)
- `%6`: gives remainder when divided by 6 (always 0-5) <!--SR:!2025-02-20,15,290-->

`TEAM[index-1][strcspn(TEAM[index-1], "\n")] = 0;`:
- It is used to {{replace newlien character with a null terminator}}
- `strcspn(TEAM[index-1], "\n")` {{returns the position of the first newline character. If no newline character is found, returns the length of the string}} <!--SR:!2025-02-18,13,290!2025-02-07,3,250-->
