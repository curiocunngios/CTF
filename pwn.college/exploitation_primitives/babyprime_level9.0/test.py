from pwn import *

def main():
	binary = './babyprime_level9.0'
	p = process(binary)
	
	s = '''
	set $mybase = (unsigned long)&challenge - 0x1a64
	b * $mybase + 0x01db6
	b * $mybase + 0x01dfe
	
	'''
	r1 = remote("localhost", 1337)

	gdb.attach(p, s)

	r1.interactive()
	
	
	

if __name__ == "__main__":
	main()
