from pwn import * 

binary = "./heap_patched"
p = process(binary)
elf = ELF(binary)
context.binary = binary
context.log_level = 'debug'

s = '''
b * calloc
'''
gdb.attach(p, s)

# your exploit continues here

p.interactive()