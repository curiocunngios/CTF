# heap 

## location of heap 

```
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
             Start                End Perm     Size Offset File
    0x55861c600000     0x55861c601000 r-xp     1000      0 /home/kali/Desktop/CTF/3633/exercises/heap_experiment                                                                                              
    0x55861c800000     0x55861c801000 r--p     1000      0 /home/kali/Desktop/CTF/3633/exercises/heap_experiment
    0x55861c801000     0x55861c802000 rw-p     1000   1000 /home/kali/Desktop/CTF/3633/exercises/heap_experiment                                                                                              
    0x55861ec79000     0x55861ec9a000 rw-p    21000      0 [heap]
    0x7fbad9a00000     0x7fbae9a01000 rw-p 10001000      0 [anon_7fbad9a00]
    0x7fbae9af5000     0x7fbae9af8000 rw-p     3000      0 [anon_7fbae9af5]
    0x7fbae9af8000     0x7fbae9b20000 r--p    28000      0 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7fbae9b20000     0x7fbae9c85000 r-xp   165000  28000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7fbae9c85000     0x7fbae9cdb000 r--p    56000 18d000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7fbae9cdb000     0x7fbae9cdf000 r--p     4000 1e2000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7fbae9cdf000     0x7fbae9ce1000 rw-p     2000 1e6000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7fbae9ce1000     0x7fbae9cee000 rw-p     d000      0 [anon_7fbae9ce1]
    0x7fbae9d06000     0x7fbae9d08000 rw-p     2000      0 [anon_7fbae9d06]
    0x7fbae9d08000     0x7fbae9d0c000 r--p     4000      0 [vvar]
    0x7fbae9d0c000     0x7fbae9d0e000 r-xp     2000      0 [vdso]
    0x7fbae9d0e000     0x7fbae9d0f000 r--p     1000      0 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7fbae9d0f000     0x7fbae9d36000 r-xp    27000   1000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2                                                                                                     
    0x7fbae9d36000     0x7fbae9d41000 r--p     b000  28000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7fbae9d41000     0x7fbae9d43000 r--p     2000  33000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7fbae9d43000     0x7fbae9d45000 rw-p     2000  35000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2                                                                                                     
    0x7ffcb966b000     0x7ffcb968c000 rw-p    21000      0 [stack]

```

it is located after the `.text` and `.data`, `.rodata` segment, with an offset between them (between the eend of `.data` segment specifically)
## allocation 



```
pwndbg> heap
Allocated chunk | PREV_INUSE
Addr: 0x55a4b04a1000
Size: 0x290 (with flag bits: 0x291)

Allocated chunk | PREV_INUSE
Addr: 0x55a4b04a1290
Size: 0x30 (with flag bits: 0x31)

Top chunk | PREV_INUSE
Addr: 0x55a4b04a12c0
Size: 0x20d40 (with flag bits: 0x20d41)

```

```
Allocated chunk | PREV_INUSE
Addr: 0x55a4b04a1290
Size: 0x30 (with flag bits: 0x31)
```
this is allocated after running the below code

```c
   11 void heap_partition() {
   12     malloc(0x20);
   13     // Break Point 1 - one allocated heap chunk

```

"cut" from the previous `top` of the `Top chunk`. Allocated with 0x30 bytes because of 0x10 sized header 

this:
```
pwndbg> heap
Allocated chunk | PREV_INUSE
Addr: 0x55a4b04a1000
Size: 0x290 (with flag bits: 0x291)
```
is used for `tcache` (learn later)


### `malloc`

```c
char *ptr = malloc(0x80);
```

Sequence is:
1. malloc finds/creates a chunk of size 0x90 (0x80 + 0x10 for header)
2. But `ptr` gets the address **AFTER the header**
3. Address returned to your program is offset by 0x10 from the {{chunk start}}

Example: A chunk created at `0x6037f0`
```
Memory layout:
0x6037f0: [prev_size][size]     <-- Chunk start (heap metadata)
0x603800: [user data..........]  <-- Address returned to program, tcache would point to 
```
Because:
1. Your program only need to use addresses starting from {{user data}}
2. While heap manager works with {{full chunk addresses (0x6037f0)}}

This design means:
- Programs don't {{accidentally modify heap metadata}}
- Programs only work with their {{allocated space (0x80)}}