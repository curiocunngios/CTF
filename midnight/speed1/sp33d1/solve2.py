from pwn import *

# Set up debugging
#context.terminal = ['gnome-terminal', '-e']
context.arch = 'powerpc'  # Set architecture to PowerPC

# Modify to debug the binary directly, not the shell script
binary = './sp33d1'
p = process(['qemu-ppc', binary])

# Set breakpoint
s = '''
'''

gdb.attach(p, s)


p.sendline(b"A" * 0x30)
p.interactive()
