# Start 

I have came back to this challenge after a one day break. And I really do have no idea on how to start. Because I did make a little progress but not much, more specifically, I kind of finished reading and "understanding" the source code. 

But now I kinda forgot about what's happening in this challenge, so it feels hard to start. 
Perhaps I should just go back to read the source code again, but this time, draw as well!


So earlier I got into the game by being patient and looking at the source once again. Now I am out of the game because I checked email, got my mind attached to enrolling the comp3633 course first. And attached to discord chat.

Now perhaps i should look into he source code again, try to write something on paper and develop a better understanding into it. Also, you play with the pwndbg to see what's actually happening inside the memory.

But now I am dehydrated, which is not good especially because I am taking Abilify.


ok... shit, I over ate (4 hardboiled eggs, 2 pieces of unknown bun, 1 bun with meat and vegetables, 3 egg siu mai) 
and slept for 2.5 hours




```
pwndbg> tele 0x16fb12a0 50 
00:0000│  0x16fb12a0 ◂— 0
01:0008│  0x16fb12a8 ◂— 0x21 /* '!' */
02:0010│  0x16fb12b0 ◂— 'AAAA BBBB CCCC'
03:0018│  0x16fb12b8 ◂— 0x434343432042 /* 'B CCCC' */
04:0020│  0x16fb12c0 ◂— 0
05:0028│  0x16fb12c8 ◂— 0x31 /* '1' */
06:0030│  0x16fb12d0 —▸ 0x16fb12b0 ◂— 'AAAA BBBB CCCC'
07:0038│  0x16fb12d8 ◂— 4
08:0040│  0x16fb12e0 —▸ 0x16fb12b0 ◂— 'AAAA BBBB CCCC'
09:0048│  0x16fb12e8 ◂— 0xe
0a:0050│  0x16fb12f0 ◂— 0
0b:0058│  0x16fb12f8 ◂— 0x31 /* '1' */
0c:0060│  0x16fb1300 —▸ 0x16fb12b5 ◂— 'BBBB CCCC'
0d:0068│  0x16fb1308 ◂— 4
0e:0070│  0x16fb1310 —▸ 0x16fb12b0 ◂— 'AAAA BBBB CCCC'
0f:0078│  0x16fb1318 ◂— 0xe
10:0080│  0x16fb1320 —▸ 0x16fb12d0 —▸ 0x16fb12b0 ◂— 'AAAA BBBB CCCC'
11:0088│  0x16fb1328 ◂— 0x31 /* '1' */
12:0090│  0x16fb1330 —▸ 0x16fb12ba ◂— 0x43434343 /* 'CCCC' */
13:0098│  0x16fb1338 ◂— 4
14:00a0│  0x16fb1340 —▸ 0x16fb12b0 ◂— 'AAAA BBBB CCCC'
15:00a8│  0x16fb1348 ◂— 0xe
16:00b0│  0x16fb1350 —▸ 0x16fb1300 —▸ 0x16fb12b5 ◂— 'BBBB CCCC'
17:00b8│  0x16fb1358 ◂— 0x1fcb1

```



```
pwndbg> heap
Allocated chunk | PREV_INUSE
Addr: 0xd89f000
Size: 0x290 (with flag bits: 0x291)

Allocated chunk | PREV_INUSE
Addr: 0xd89f290
Size: 0x1010 (with flag bits: 0x1011)

Free chunk (tcachebins) | PREV_INUSE
Addr: 0xd8a02a0
Size: 0x20 (with flag bits: 0x21)
fd: 0xd8a0

Allocated chunk | PREV_INUSE
Addr: 0xd8a02c0
Size: 0x30 (with flag bits: 0x31)

Allocated chunk | PREV_INUSE
Addr: 0xd8a02f0
Size: 0x30 (with flag bits: 0x31)

Allocated chunk | PREV_INUSE
Addr: 0xd8a0320
Size: 0x30 (with flag bits: 0x31)

Free chunk (tcachebins) | PREV_INUSE
Addr: 0xd8a0350
Size: 0x20 (with flag bits: 0x21)
fd: 0xd8ada10

Top chunk | PREV_INUSE
Addr: 0xd8a0370
Size: 0x1fc90 (with flag bits: 0x1fc91)
```
`0xd8a0350` is the search_word, the chunk created and used for search the word 
`0xd8a02a0` is the chunk used just for storing the original sentence, not a node

