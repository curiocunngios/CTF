Here's what each header provides:

**`#include <sys/ioctl.h>`**
Defines the `ioctl()` function and related constants. This is what lets you make ioctl system calls to communicate with device drivers using custom commands.

**`#include <fcntl.h>`** 
Provides file control operations, most importantly the `open()` function and flags like `O_RDWR` (open for read/write), `O_RDONLY`, etc. This is how you get file descriptors.

**`#include <unistd.h>`**
Contains various POSIX system calls including `close()`, `read()`, `write()`, and other fundamental Unix operations. It's often called the "unistd" (Unix standard) header.

So in your ioctl program: `fcntl.h` lets you open the device file, `sys/ioctl.h` lets you send commands to it, and `unistd.h` lets you close it when you're done.
