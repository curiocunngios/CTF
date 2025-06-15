from pwn import *

binary = './a.out'

# Set up the GDB script
gdbscript = '''
break main
continue
'''

# Launch the process with GDB attached
p = gdb.debug(binary, gdbscript)

# Give control to the user
p.interactive()
