# Mindset
1. the key is to find vulnerabilities (BOF, UAF, format string, invalid free etc.)
2. And remember the tricks i.e. GOT hijacking, ret2libc, shellcode injection, ret2dlresolve, ret2XXXX, house of spirit
3. If you have no clue. You are obviously encoutering something new ( which the challenge might be easy). Be patient and just learn the everything about the program.
4. Once you get into the "game". Pay attention to the little details while debugging. E.g. the stuff on the stack, heap etc. 
# Strategy
Skim through the programs, by downloading the files one by one and briefing looking through the source.    
Until you find one that you feel familiar with, start with that first.  
For those that you are not familiar with, they might surprisingly be something easy. So just document the general behaviour of the program and you start later.
# Preparations:
1. practice skills, familarize yourself with the general pwn task flow and vulnerabilities regconition with firebird homeworks 
2. Use the same flow above to go through HKCERT CTF pwn challenges every year. Under one day, when the day ends just read the writeups and learn 
3. Mark down the key program codes and the vulnerability it associated with, together with explain and make it into flashcard
# When doing challenges
1. download all the files 
2. look into the source code 
3. if there is no source code, decompile + a bit reverse perhaps to get the source and look into it 
4. open a new note.md 
5. identify vulnerabilities and mark them down 
6. prepare your script:
```py
from pwn import * 

binary = "./program"
p = process(binary)
elf = ELF(binary)
context.binary = binary
context.log_level = 'debug'

s = '''
b * vuln
'''
gdb.attach(p, s)

p.interactive()
```
Or 

```py
from pwn import * 
from pwnlib.util.misc import run_in_new_terminal 

binary = './program'
context.binary = binary 
r = remote('localhost', 1337)
sleep(1)

pid = pidof('program')[0]
run_in_new_terminal(f'gdb -p {pid}')

r.interactive()

```
7. also write down a brief to-do list for your first attempt
8. be calm, patient and observant in the binaries. Keep your mind full focus on the challenge
9.  work? keep going. Doesn't work? figure out why and perhaps change strategy