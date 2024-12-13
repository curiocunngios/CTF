---
aliases:
  - VOid arguments
tags:
  - flashcard/active/ctf
---

# Void arguments
```
► 0x80493d8 <main+102>    call   vuln                        <vuln>
        arg[0]: 0xf7fc0400 —▸ 0xf7d68000 ◂— 0x464c457f # ELF magic number
        arg[1]: 0
        arg[2]: 0
        arg[3]: 0x3e8
```
The above are "arguments" of a void function {{aren't actually arguments}}. They're just values that {{happen to be on the stack}}when vuln() is called. <!--SR:!2024-12-18,4,270!2024-12-18,4,270-->