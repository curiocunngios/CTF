---
aliases:
  - debugging .exe file
tags:
  - flashcard/active/ctf
  - notes/tbc
---

Here is how we can debug a `.exe` file 

# On linux

1. First, install the required packages if you haven't already:
```bash
sudo apt-get install wine gdb
```

1. There are two main approaches you can use:

Method 1 - Using winedbg directly:
```bash
winedbg --gdb stack-man_release_v3.exe
```

Method 2 - Using a more detailed approach:
```bash
# Start the program with wine in debug mode
wine stack-man_release_v3.exe &
# Get the Wine process ID
ps aux | grep stack-man_release_v3.exe
# Attach GDB to the process
gdb attach <process_id>
```

3. Alternative method using WINEDBG:
```bash
WINEDEBUG=+relay wine stack-man_release_v3.exe
```

If you're specifically trying to analyze the binary, you might also want to consider these alternatives:

1. Using Radare2:
```bash
r2 wine stack-man_release_v3.exe
```

2. Using Ghidra (for static analysis)

3. Or running the executable in a Windows VM with x64dbg or OllyDbg for better Windows debugging support.

Would you like me to explain more about any of these methods or provide additional debugging techniques?