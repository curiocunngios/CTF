# `fgets(flag, 0x40, file):`


- Takes 3 parameters: destination buffer, max length, file stream
- Reads up to (0x40 - 1) = 63 characters from file into flag buffer
- Stops at newline ('\n') or EOF
- Always null-terminates the string
- Safer than gets() because it has a length limit
- Keeps the newline character if it reads one

# `builtin_strncpy(str, "this is a random string.", 0x19)`:
- Takes 3 parameters: destination buffer, source string, max length
- Copies up to 0x19 (25) characters from source to destination
- If source is shorter than 0x19, fills remaining bytes with nulls
- Does NOT guarantee null-termination if source is longer than max length
- Different from regular strncpy in that it's a compiler built-in function, but behaves similarly

1. `strcat(local_98, flag)`:
- Takes 2 parameters: destination buffer, source string
- Appends source string to end of destination string
- Starts writing at destination's null terminator
- Adds null terminator at end
- Dangerous because:
  - No length limit
  - Can overflow if destination buffer isn't large enough
  - Needs destination to be null-terminated
  - Needs source to be null-terminated

