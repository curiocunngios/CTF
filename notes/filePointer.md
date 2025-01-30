---
aliases:
  - file pointer
  - Pointer to a file
tags:
  - flashcard/active/ctf/C
---

# File pointer
A file pointer is like a {{bookmark or cursor that keeps track of your position in a file}}. It contains:
- The {{current position in the file}}
- The file's path/name
- Mode (read/write)
- Buffering information <!--SR:!2025-02-02,3,250!2025-02-02,3,250-->

```C
FILE *f = fopen("test.txt", "r");

// File contents: "Hello\nWorld"
//                ^
// File pointer starts here (position 0)
```


