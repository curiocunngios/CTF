#!/usr/bin/python3
from pwn import *
import os

# Set terminal
#context.terminal = ['tmux', 'split-window', '-h']

# Enable debugging permissions
#os.system("echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope")

# Create gdb script
gdbscript = """
b 7
b 8
b 9
c
"""

try:
    # Start program in debug mode
    p = gdb.debug('./calc_tcache_idx', gdbscript)
    p.interactive()
except Exception as e:
    print(f"Failed to start debugger: {e}")
