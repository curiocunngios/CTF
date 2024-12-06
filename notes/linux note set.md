---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - Linux
tags:
  - flashcard/active/ctf/testing
  - function/index
  - language/in/English
---

#### Linux File System Structure  
Essential Directories :::  
??
- `/bin`: {{Essential command binaries}}
- `/sbin`: {{System binaries}}
- `/etc`: {{System configuration files}}
- `/lib`: {{Essential shared libraries}}
- `/usr`: {{User programs and data}}
- `/var`: {{Variable data (logs, temp files)}}
- `/tmp`: {{Temporary files (cleared on reboot)}}
- `/proc`: {{Process and kernel information}}
- `/dev`: {{Device files}}
- `/home`: {{User home directories}}
- `/root`: {{Root user's home directory}}

Important /proc Files :::  
??
- `/proc/self/maps`: {{Memory mappings of current process}}
- `/proc/self/mem`: {{Memory of current process}}
- `/proc/self/environ`: {{Environment variables}}
- `/proc/sys/kernel/randomize_va_space`: {{ASLR settings}}

#### File Permissions
Permission Format :: Understanding `ls -l` output (e.g., `-rwxr-xr-x`)
??
```text
Type: - (file), d (directory), l (link)
User:  rwx (read, write, execute)
Group: rwx (read, write, execute)
Other: rwx (read, write, execute)
```

Numeric Permissions ::: Converting between symbolic and octal    
??    
```text
r = 4
w = 2
x = 1

rwx = 7
rw- = 6
r-x = 5
r-- = 4
```

#### Essential Commands
File Operations :::   
??  
```bash
ls -la           # List all files with details
cp source dest   # Copy files
mv source dest   # Move/rename files
rm [-rf] file    # Remove files/directories
mkdir dir        # Create directory
chmod 755 file   # Change permissions
chown user file  # Change owner
```

File Analysis :::  
??  
```bash
file binary           # Determine file type
strings binary       # Print printable strings
hexdump -C file      # Hex dump with ASCII
xxd file            # Another hex dumper
diff file1 file2    # Compare files
```

Text Processing :::  
??  
```bash
cat file           # Print file content
less file          # Page through file
grep pattern file  # Search for pattern
sed 's/old/new/g'  # Stream editor
awk '{print $1}'   # Pattern processing
sort file          # Sort lines
uniq               # Remove duplicates
```

Process Management :::  
??  
```bash
ps aux            # List all processes
top               # Dynamic process view
kill pid          # Kill process
killall name      # Kill by name
fg                # Foreground job
bg                # Background job
jobs              # List jobs
```

Network Commands :::  
??  
```bash
netstat -tuln     # List listening ports
netcat -lvp port  # Listen on port
curl url          # HTTP requests
wget url          # Download files
ssh user@host     # Secure shell
scp file dest     # Secure copy
```

#### System Information
System Analysis :::  
??  
```bash
uname -a          # System information
lsb_release -a    # Distribution info
cat /etc/passwd   # User accounts
cat /etc/shadow   # Password hashes
env               # Environment vars
whoami            # Current user
id                # User/group IDs
```

Hardware Info :::  
??  
```bash
lscpu             # CPU information
free -h           # Memory usage
df -h             # Disk usage
lsusb             # USB devices
lspci             # PCI devices
```

#### Useful CTF Commands
File Transfer Methods :::  
??  
```bash
# Host server
python3 -m http.server 8000
php -S 0.0.0.0:8000
nc -lvp 1234 < file    # Send
nc host 1234 > file    # Receive

# Download files
wget http://host:8000/file
curl http://host:8000/file -o file
```

Binary Analysis :::  
??  
```bash
ldd binary         # List dependencies
readelf -a binary  # ELF file info
objdump -d binary  # Disassemble
strace ./binary    # Trace syscalls
ltrace ./binary    # Trace library calls
```

#### Shell Tips
Command Line Shortcuts :::  
??  

- Ctrl+C: {{Kill current process}}
- Ctrl+Z: {{Suspend process}}
- Ctrl+D: {{EOF (end of file/input)}}
- Ctrl+L: {{Clear screen}}
- Ctrl+R: {{Search command history}}
- Ctrl+A: {{Move to start of line}}
- Ctrl+E: {{Move to end of line}}

Shell Redirections :::  
??  
```bash
command > file     # Output to file
command >> file    # Append to file
command < file     # Input from file
command 2> file    # Error to file
command &> file    # Both output and error
command1 | command2 # Pipe output
```

#### Special Files
Device Files :::
??

- /dev/null: {{Discard output}}
- /dev/zero: {{Stream of zeros}}
- /dev/random: {{Blocking random}}
- /dev/urandom: {{Non-blocking random}}
- /dev/shm: {{Shared memory}}
- /dev/tcp/host/port: {{TCP connections}}
- Environment Variables

Common Variables :::  
??  
```bash
$PATH      # Command search path
$HOME      # User's home directory
$USER      # Current username
$PWD       # Current directory
$SHELL     # Current shell
$LD_PRELOAD # Library preloading
$LD_LIBRARY_PATH # Library search path
```
