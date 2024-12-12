---
aliases:
  - Address Space Layout Randomization
tags:
  - flashcard/active/ctf
---
# ASLR
ASLR stands for {{Address Space Layout Randomization}}. It randomizes where {{libc is loaded in memory}} to get protected from attacks that make use of libc address maliciously. For example, adding proper offset to call system() function for shell.


## Strategy to defeat ASLR  

- Leak an address of a {{libc function (using puts/printf)}}
- Calculate the {{base address of libc}} with offsets of that libc function. {{Which is different for different libc version}}
- Calculate the {{exact addresses}} of functions we want to use. For example, {{system}} 