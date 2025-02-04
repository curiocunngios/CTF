---
aliases:
  - typical functions of C 3
tags:
  - flashcard/active/ctf/C
---

# ghidra
`*(int *)(&DAT_00301020 + local_10 * 4))`:
- `DAT_00301020` is the {{base address of an array}}
- `local_10` is the {{index variable }}
- `* 4` because each element is {{4 bytes (32-bit integer), or they are just offset by 4 bytes}}
- `(int *)` casts the address to an {{integer pointer}}
- `*` {{dereferences}} to get the value <!--SR:!2025-02-08,4,270!2025-02-08,4,270!2025-02-08,4,270!2025-02-08,4,270!2025-02-08,4,270-->


# Actual C programs
`int main(int argc, char *argv[])`:
- `argc` is the {{number of elements in argv[], i.e. number of arguments}}
- `argv` is the {{array of string storing arguments}}
- `argv[0]` is the {{program name}}
- `argv[1]` and so on are the {{arguments following the program's name}} <!--SR:!2025-02-08,4,270!2025-02-08,3,250!2025-02-08,4,270!2025-02-08,4,270-->

`fwrite("3 days have passed",1,0x12,stdout);`:
- `"3 days have passed"` - {{the source buffer to write from}}
- `1` - the size of {{each element}} in bytes
- `0x12` - the {{number of elements}} to write (18 in hex)
- `stdout` - the {{output stream}} to write to <!--SR:!2025-02-08,4,270!2025-02-07,3,250!2025-02-07,2,230!2025-02-07,3,250-->

