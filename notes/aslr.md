---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - binary exploitation
  - GOT leak
  - protection
tags:
  - flashcard/active/ctf/hi
  - function/index
  - language/in/English
---
# ASLR
ASLR ::: stands for "Address Space Layout Randomization" which randomizes where libc is loaded in memory   
To get protection from attacks that make use of libc address maliciously. For example, adding proper offset to call system() function for shell.


## How to defeat ASLR  
??  
- Leak an address of a libc function (using puts/printf)
- Calculate the base address of libc 
- Calculate the exact addresses of functions we want to use (like system)