# Pwntools Basics

What is pwntools? :::
A Python library specifically designed for CTF challenges and exploit development.
Installation: 
```bash
sudo python3 -m pip install --upgrade pwntools
```

Import pwntools ::: from pwn import *  # This imports all pwntools functions


Connecting to a remote CTF challenge server ::: 
```py
# Format: r = remote("server_address", port_number)
r = remote("chal.firebird.sh", 35008)
# Example of connecting to a CTF challenge running on port 35008
```

#flashcard r.recv()
```py
# r.recv() gets raw data from server
data = r.recv()  
print(data)  # Might print: b'Welcome to the challenge!\n'

# Specify number of bytes to receive
first_4_bytes = r.recv(4)  # Only receive 4 bytes
```

#flashcard r.recvline()
```py
# r.recvline() receives data until it hits a newline
line = r.recvline()  
print(line)  # Might print: b'Enter your name:\n'

# Real CTF example:
question = r.recvline()
print(question.decode())  # Convert bytes to string
```

#flashcard r.recvuntil()
```py
# r.recvuntil() receives data until it finds specific string
response = r.recvuntil(b": ")  # Wait for ": "
print(response)  # Might print: b'Enter password: '

# Common CTF example:
r.recvuntil(b">>>")  # Wait for prompt
r.sendline(b"answer")  # Then send answer
```

#flashcard r.send() and r.sendline()
```py
# r.send() - sends raw data
r.send(b"hello")  # Sends: hello

# r.sendline() - sends data with newline
r.sendline(b"hello")  # Sends: hello\n

# Example difference:
r.send(b"123")     # Server receives: 123
r.sendline(b"123") # Server receives: 123\n
```

#flashcard what r.interactive() and when to use it?

```py
# r.interactive() lets you interact with server directly
# Common pattern:
r = remote("chal.firebird.sh", 35008)
r.recvuntil(b"password: ")
r.sendline(b"secret123")
r.interactive()  # Now you can type commands directly

# Useful when:
# 1. You got shell access
# 2. You want to debug what server sends
# 3. Challenge requires manual interaction
```

Example of a CTF solve script
```py
#!/usr/bin/env python3
from pwn import *

# Connect to challenge server
r = remote("chal.firebird.sh", 35008)

# Receive initial prompt
welcome = r.recvline()
print(welcome.decode())  # Show what server sent

# Wait for specific prompt
r.recvuntil(b"name: ")

# Send our answer
r.sendline(b"Firebird")

# Get response
response = r.recvline()
print(response.decode())  # Should show flag or next prompt

# If we need to interact further
r.interactive()
```

Remember :::

-    Always use bytes (b"string") when sending/receiving data
-    Use .decode() to convert bytes to readable string
-    r.interactive() is your friend when debugging
-    Most CTF challenges follow pattern: receive prompt → send answer → get flag
