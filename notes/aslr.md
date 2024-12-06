ASLR and libc leaking:
ASLR (Address Space Layout Randomization) randomizes where libc is loaded in memory


To defeat it, we need to:
- Leak an address of a libc function (using puts/printf)
- Calculate the base address of libc
- Calculate the exact addresses of functions we want to use (like system)