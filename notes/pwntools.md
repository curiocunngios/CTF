---
aliases:
  - pwntools
tags:
  - flashcard/active/ctf
---

# Pwntools 
A Python library specifically designed for CTF challenges and exploit development.

### `remote`
Connecting to a {{remote server }}
```py
# Format: r = remote("server_address", port_number)
r = remote("chal.firebird.sh", 35008)
# Example of connecting to a CTF challenge running on port 35008
```
<!--SR:!2024-12-17,3,250-->

### `recv()`
`recv()` gets {{raw data}} from server
```py

data = r.recv()  
print(data)  # Might print: b'Welcome to the challenge!\n'

# Specify number of bytes to receive
first_4_bytes = r.recv(4)  # Only receive 4 bytes
```
<!--SR:!2024-12-17,3,250-->

### `recvline()`
`recvline()` {{receives data from server until it hits a newline}}
```py
line = r.recvline()  
print(line)  # Might print: b'Enter your name:\n'

# Real CTF example:
question = r.recvline()
print(question.decode())  # Convert bytes to string
```
<!--SR:!2024-12-17,3,250-->

### `recvuntil()`
`recvuntil()` receives data {{until it finds specific string}}
```py
response = r.recvuntil(b": ")  # Wait for ": "
print(response)  # Might print: b'Enter password: '

# Common CTF example:
r.recvuntil(b">>>")  # Wait for prompt
r.sendline(b"answer")  # Then send answer
```
<!--SR:!2024-12-17,3,250-->

### `send()` and `sendline()`
- `send()` {{sends raw data}}
- `sendline()` {{sends data with newline}}
```py
r.send(b"hello")  # Sends: hello

r.sendline(b"hello")  # Sends: hello\n

# Example difference:
r.send(b"123")     # Server receives: 123
r.sendline(b"123") # Server receives: 123\n
```
<!--SR:!2024-12-16,2,230!2024-12-17,3,250-->

### interactive()
`interactive()` lets you {{interact with server}} directly
```py
# Common pattern:
r = remote("chal.firebird.sh", 35008)
r.recvuntil(b"password: ")
r.sendline(b"secret123")
r.interactive()  # Now you can type commands directly
```
<!--SR:!2024-12-17,3,250-->