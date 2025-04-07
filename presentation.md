# Start 

Hello everyone, I am LI Yat Fung, Alex. Today I will be sharing with you House of Einherjar. Before that, let me introduce myself a bit although nobody cares, because I care. I am currently 20 years old, male, my pronoun is he/him, I am single, Also I am pretty mentally ill, actually mentally ill. I am an actual OCD {{writes OCD}} 強迫症 patient. And one of my obsession is related to my information accuracy. I care soooo much about the accuracy of stuff I convey to you guys, so I think I would be most of the time speaking quite slowly. Which might be a little boring but it could also **be a good thing!**. Because it is probably easier for you guys to follow. Ok, that's enough for my introduction. Let's get into code of ethics!

# Code of ethics
Ok code of ethics. So please.... never hack stuff without permission, because what you do might harm the others, it might harm the privacy of the others. And you are likely to make some enemies if you just hack whatever you want. And if somebody is smarter than you, you are like done, it's over for you, it's gg dude cuz you'd probably be going to jail. Anyways, let's finally get into today's topic:fastbin dup

# House of Einherjar

First of all, I am not 100% sure how to pronouce this word (highlights Einherjar with your cursor), so if anyone of you are certain, please let me know how to pronouce. If not, I would just pronouce it as And-her-yea for the rest of this lesson.

First all of, let me first go through what we **need** for House of Einherjar. So what do we need to be able to do House of einherjar, the answer is very simple. We need a one byte overflow, also famously known as **off-by-one**. More specifically, we would need to use that one byte overflow to write a null-byte, which is also famously known as **off-by-null**. We have to write a null byte because, we want to clear a bit that is used as a flag that indicate whether the previous chunk is freed or not, I will let you know how and why, later.

Also, we need a heap address leak to create a fake chunk that **pretends** to be freed chunk, which I would also explain in details later. Now you only to know that we need these 2 things




Now let's take a look at the big picture of what we need to do

We need to first create 3 chunks, and the size of chunk C, has to be carefully chosen.

The size has to be greater or equal than 0x90 bytes, and at the same time, it has to be 0x100 bytes aligned. Which means, the sizes can only something like 0x100, 0x200, 0x300, 0x400, etc., (For the reason why, I would let you know later, if I forgot to explain later, please remind me or just ask me why at that time)

A good example of the sequences of the sizes would be, 0x40, 0x30, 0x100, which would look like this when we look at them with a debugger:

Second, we create a fake chunk inside chunk A, and the fake chunk pretends to be a freed chunk inside the fastbin.
Now let's have a look at how it looks like in pwndbg to have a more clear idea of what I mean by fake chunk.

You can see that 0x40, it's the exactly the size of chunk A
which means this specific slot that is 8 byte before it, is the starting point of chunk A.
Right after the size field of chunk A, we have 0 here, and after this slot, we manually write 0x60 on it, which is the size of our fake chunk. So this 0 (before 0x60) is the starting point of our fake chunk.

Similarly, this is starting point of chunk B (points to the slot before 0x30)

Please be reminded that these (highlight the fake chunk) are all the things we write manually onto the memory, just to make it look like a real chunk, that is freed and is in the fastbin.

**this** (point to 0x41) and **this** (point to 0x31) are actual size data written by the system.


Now what's circled is the fake chunk, since we specify the size of the fake chunk to be 0x60, it goes beyond the data field of chunk B. 

**Which means**, if we managed to trick the program to malloc at the fake chunk, we are able to overflow by a lot to chunk B and perform tcache poisoning. (I would explain what's tcache poisoning later so don't worry)


Ok let's move on to step 3 of the big picture. We need to start writing data from chunk B up to the last 8 bytes of chunk B, why last 8 bytes? Because the last 8 bytes of chunk 8 is a shared space, it is also the first 8 bytes of chunk C. When chunk B is in use, that space is used by chunk B. when chunk B is freed and the prev_in_use bit of chunk C is set to 0, then that space would becomes the size of chunk B.

When we successfully overwritten up to the last 8 bytes of chunk B, we can at the same time write a null byte onto the size field of chunk C using our one-byte overflow primitive	

Switching to how it looks like in debugger, we can see that from B, we overwrite a lot of A, which is 0x41, capital letter A 


count them....


Look here (highlight the null byte), this is the last byte, the null byte we overflew 


# notes for tmr, refine the powerpoint by fixing the positioning of the slides, *the big picture* should clearly explains the big idea behind

# but you have been going into details already (above)




