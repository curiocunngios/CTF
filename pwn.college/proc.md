`/proc/` is a **virtual filesystem** (called "procfs") that provides a window into the running kernel and system state. It doesn't contain real files on disk - everything is generated dynamically by the kernel.

## What makes /proc special:

**Not real files**: When you `cat /proc/cpuinfo`, you're not reading a file - the kernel generates that info on-the-fly.

```bash
/ # ls -la /proc/cpuinfo
-r--r--r--    1 root     root             0 Jan  1 00:01 /proc/cpuinfo
# Size shows 0, but it has content when you read it!
```

## Common /proc entries:

### System information:
```bash
/proc/cpuinfo      # CPU details
/proc/meminfo      # Memory usage
/proc/version      # Kernel version
/proc/uptime       # System uptime
/proc/loadavg      # System load
```

### Process information:
```bash
/proc/1/           # Process ID 1 (init)
/proc/1/cmdline    # Command line that started PID 1
/proc/1/maps       # Memory mappings for PID 1
/proc/self/        # Current process (shortcut)
```

### Kernel internals:
```bash
/proc/kallsyms     # Kernel symbol table (what we used!)
/proc/modules      # Loaded kernel modules
/proc/devices      # Device drivers
/proc/filesystems  # Supported filesystems
```

## Why it's crucial for kernel exploitation:

### 1. **Information gathering**:
```bash
/ # cat /proc/version
Linux version 5.4.0 (root@buildkite) (gcc version 7.5.0) #1 SMP
```

### 2. **Finding loaded modules**:
```bash
/ # cat /proc/modules
babykernel_level1_0 16384 0 - Live 0xffffffffc0000000 (O)
```

### 3. **Symbol resolution** (as we did):
```bash
/ # cat /proc/kallsyms | grep device_write
```

### 4. **Memory layout**:
```bash
/ # cat /proc/iomem        # Physical memory map
/ # cat /proc/self/maps    # Virtual memory map of current process
```

## The challenge device:

When you do `echo "password" > /proc/pwncollege`, you're:
1. **Writing to**: A special file created by the kernel module
2. **Not a real file**: It's a virtual entry that triggers `device_write()`
3. **Module creates it**: The babykernel module registered `/proc/pwncollege`

## How modules create /proc entries:

```c
// This is roughly what the module does:
proc_create("pwncollege", 0666, NULL, &file_operations);

// When you write to /proc/pwncollege, it calls:
static struct file_operations file_operations = {
    .write = device_write,     // Your echo triggers this!
    .read = device_read,
    .open = device_open,
    .release = device_release,
};
```

## Try exploring:

```bash
# See what the module created:
/ # ls -la /proc/pwn*

# See all loaded modules:
/ # cat /proc/modules

# See your process info:
/ # cat /proc/self/status
/ # cat /proc/self/maps

# See system state:
/ # cat /proc/meminfo
/ # cat /proc/cpuinfo
```

## Security implications:

Many exploits use `/proc/` to:
- **Leak information**: Kernel addresses, ASLR bypasses
- **Find gadgets**: Via `/proc/kallsyms`
- **Understand layout**: Memory mappings
- **Interact with drivers**: Custom `/proc` entries (like your challenge)

So `/proc/` is essentially the kernel's "API" for userspace to peek inside the running system!
