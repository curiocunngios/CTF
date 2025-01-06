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

# your exploit continues here

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