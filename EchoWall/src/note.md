# GOT hijacking 

libc function call ---> plt (entry, look up table) ---> GOT / resolver ---> address retriving
Overwrite GOT's address to call shell 

What needs to be satisfied for GOT hijacking:

1. Not Full RELRO (load all addresses and make GOT read_only)
2. defeat PIE, GOT is in code section. Address leak in code / data section is required 
3. Get arbirary write 
4. overwrite GOT entry

```c
printf(user_input);  // Classic format string vulnerability
```
Exploit approach:

- Use %n to write arbitrary values
- Common pattern: %<number>c%<index>$n
- Can write to GOT entries to redirect function calls



###### ~ Yea
yep, for those content you really haven't know much about, you need to first focus on reading

1. read notes, gpt's teaching, google, wikipedia 
2. take notes, refine them 
3. start easier exercises, explore with curiosity and keep learning, take notes, etc.
4. journal even on doing the easiest exercises, learn and write writeups
5. move on to new topics



it's always like this, when you are stressed about progress you are not likely to go faster.
You wanted to fast forward progress and now you are a bit afraid of learning week 7/8 stuff i.e. format string. Why tho. When you move on from firebird challenges, there are much more techniques to learn and you got to focus on learning and absorb better! 

priority:
1. skill, concept learning (python, pwntools, ghidra, gdb, pwn techniques, memory layout understanding etc.)
2. don't try to like prove yourself by finishing a challenge, prove yourself by making progress on actually learning, building up knowledge in your brain and being able to easily write writeups for the challenges.



# GOT entry

it means something like `0x404018` which contains function's address in libc and it is also what which plt would jump to when the function is called in program 
```
GOT table example:
0x404018 -> puts@got    # Address where puts' real address is stored
0x404020 -> printf@got  # Address where printf's real address is stored
0x404028 -> strlen@got  # Address where strlen's real address is stored
```
When you do elf.got['puts'], you get the address WHERE the address of puts() is stored (e.g., `0x404018`) in the program 

## Redirecting functions 
```py
# If you have arbitrary write vulnerability:
write_to_address(elf.got['strlen'], libc.symbols['system'])

# If format string:
target = elf.got['strlen']
system = libc.symbols['system']

# Often need to write byte by byte:
for i in range(8):  # For 64-bit address
    byte = (system >> (i*8)) & 0xff
    write_byte_to_address(target + i, byte)
```
The key is: you're not assigning values in Python - you need to actually write to process memory using your vulnerability. The GOT entry is just a memory address that needs to be overwritten with your target function's address.