# Input buffer

The input buffer (stdin buffer) is a {{separate memory area managed by the C standard I/O library (stdio)}}. It's not part of {{program's stack frame}}. Think of it as a {{temporary holding area for input}} before your program processes it.

## visualization of input buffer:
```
Memory Layout:
+------------------------+
|       Stack Frame      |
|  +------------------+ |
|  | choice[2]        | |    Program's memory
|  | ['1', '\0']      | |
|  +------------------+ |
+------------------------+

+------------------------+
|    stdin buffer        |
|  ["23\n"]             |    Managed by stdio
|                       |    (separate from your program memory)
+------------------------+
```
When you type "123" + Enter:
1. The full input "123\n" goes to the {{stdin buffer}} first
2. `fgets(choice, 2, stdin)` does:
   - Reads "1" from {{stdin buffer}} into `choice` array (on stack)
   - Adds '\0' to `choice` array
   - Leaves {{"23\n"}} in stdin buffer
3. The remaining "23\n" stays in the stdin buffer, not in your program's stack memory

This is why buffer overflow attacks typically target program buffers (like arrays on the stack) rather than input buffers - because input buffers are managed by the C library and are separate from your program's executable memory space.
    