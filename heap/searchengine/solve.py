from pwn import *

binary = './search-bf61fbb8fa7212c814b2607a81a84adf'
p = process(binary)
s = '''
b * 0x00400ad0
b * 0x00400c00
'''

gdb.attach(p, s)
def searchWord(size, sentence):
	p.sendlineafter(b"Quit\n", b"1")
	p.sendlineafter(b"size:\n", size)
	p.sendlineafter(b"word:\n", word)
def addsentence(size, sentence):
	p.sendlineafter(b"Quit\n", b"2")
	p.sendlineafter(b"size:\n", size)
	p.sendlineafter(b"sentence:\n", sentence)
	
	
addsentence(b"14", b"AAAA BBBB CCCC")

p.interactive()
