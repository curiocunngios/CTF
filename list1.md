# 17/1/2025 
# Things that I wish to learn:

> heap exploitation

- 2/10. I do not know much about it at this moment. I only have a very brief big picture about the structuring of the heap, specifically ptmalloc2, that 

- tcachebins only stores 7 entries for each size.
- the very first chunk is tcachebin
- the bins seems to be implemented in C and I do not know how it works.
- size <= 80 goes to fastbin if tcachebin is full on that particular size.
- if size if >= 80 and that the chunk to be free is not near Top chunk. Then, it goes to unsortedbin. 
- About the structuring of chunks, theres the Header, occuping 0x20 bytes of size containing metadata i.e.:
1. data of the previous chunk
2. current chunk size. 
- Then after the metadata, the data of the chunk stores in order of how the dynamic struct/class in C was implemented.

I seem to be quite a lot about the structuring and details of the heap. But in fact, no, I know only the very basics and limited knowledge that was required for just one or two specific CTF challenges. For the rest of the knowledge about the heap, I know none of them because I did not want to invest time in investigating the C implementation code or reading some articles about it.

> control flow hijacking

- 0.5/10
- only tls_dlors_list hijacking and just a bit about it. For example, we 
1. find fsbase
2. overwrite fsbase + 0x30 to 0, or leak it for later calculation
3. overwrite fsbase - 0x58 (forgot what this is but probably the tls_dlors_list) to a controllable address
4. write tls_dlors_list-->function to something like (sys_addr ^ (fsbase + 0x30) > 11) -> becomes system
5. write tls_dlors_list-->obj to /bin/sh
6. seems like obj would somehow be put into func but I dont know why.

- __IO_cookie_jump (only know this existed, nothing else lol)

> Windows fundamentals

0.01/10

- literally near 0. I only know how to play video games and watch youtube videos on windows 11
- perhaps explored the file system a little little bit because of some errors I encountered but mostly I just follow some youtube guides to fix that particular errors. 

> windows exploitation

- 0.01/10. nearly 0 again. I don't know Windows fundamentals, how would I know how to exploit it.

> kernel exploitation

- 1/10. probably know nothing about kernel pwn but I do know a bit of pwn e.g. stack buffer overflow, overwriting return address, GOT hijacking, ROP, ret2libc, format string attack, stack migration etc. 

> Web stuff 

- 0.01/10. 0 again. I might have heard a bit about SQL injection and burpsuite in the past but I am sure I forgot the entirety of the content I heard.

> pentesting

- 0.01/10. I don't even have a clear idea of what it is. Maybe just kind of equivalent to the term "hacking"

> exploit development.

- 0.001/10. no idea what this is. Is writing a pwn script with python counted? lol

> scripting with python. 

- 0.1/10. I have very very limited knowledge about python and other programming languages. I have been using just claude-3.5-sonnet to help me parse stuff and learnt a little bit from that. like `p.recvuntil` 

> scripting with othe languages.

- 0.001/10. Similar as the above. I am not even familiar with python that "I" have been using all along. How would I know other programming languages for scripting. But since they might be necessary e.g. C programming for writing kernel and hypervisor exploits for EXP-401. So I also want to learn.


> bypassing epxloit mitigations.

- 0.1/10. I only know that we can bypass the protection of PIE and canary by leaking `.text` addresses and the canary itself lol. Pretty sure there are many more modern protections that I haven't even heard about. 

> assembly 

- 1/10. Only know a few instructions and still not familiar with them. For example, I still am not very sure what is the different between `lea` and `mov`. Instructions that I know a bit right now:
1. `push`
2. `leave`
3. `ret` 
4. `call` 
5. `jmp`
6. `mov`, `lea` 
7. `add`, `sub`, ...

# Next steps

1. HTB academy modules, together with chatgpt to learn (20%)
- fundamentals 
- OSCP related 
- web 
2. refine your knowledge on assembly and pwn by doing CTFs and learning(80%)
