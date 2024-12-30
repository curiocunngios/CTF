from pwn import * 
context.binary = "./program"
#context.terminal = ['tmux', 'split-window', '-h']  # or ['gnome-terminal', '-e'] depending on your terminal
context.arch = 'aarch64'
binary = "./program"
p = process(binary)
s = '''
b *main
continue
'''
###context.arch = 'aarch64'  # Set architecture
#context.binary = binary   # Set binary

gdb.attach(p, s)
p.recvuntil(b"0x")
leak = b'0x' + p.recvuntil(" （´◔ ₃ ◔`)", drop = True)
leak = int(leak, 16) # directly to int
#print(type(leak.decode()))# from byte to str
print(hex(leak))

p.recvuntil("Can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄")

payload = flat(


)
p.interactive()

p.sendline(b"no")

p.interactive()