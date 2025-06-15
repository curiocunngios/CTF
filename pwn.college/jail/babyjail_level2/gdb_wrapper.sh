#!/bin/bash

# Create a temporary GDB init file
cat > /tmp/gdb_init_temp << EOF
source ~/.gdbinit
set follow-fork-mode child
break *0x1337000
EOF

# Run GDB as root with the temporary init file
exec gdb -x /tmp/gdb_init_temp "$@"
