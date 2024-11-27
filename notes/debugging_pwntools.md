# Debugging in CTF/Pwntools Context

What is debugging in CTF context? :::
- Understanding what data server sends
- Figuring out why your script isn't working
- Learning how the challenge behaves
- Testing different inputs manually

Why use r.interactive() for debugging? :::
Example scenario:
```python
from pwn import *
r = remote('challenge.com', 1234)

# Your script isn't working, so add:
print("Debug: Checking server response...")
r.interactive()
```
Now we can:
- see what server sends 
- try different input by changing the script content manually
- Understand the challenge flow
#### Example of debugging in CTF challenges
```py
# Problem: Script not getting flag
from pwn import *
r = remote('challenge.com', 1234)

r.sendline(b"answer")
# Not sure what's happening next, so:
print("Debug: Server response after answer:")
r.interactive()

# You might see:
# > Please solve captcha first!
# Now you know you missed a step!
```


#### One more example 

```py
from pwn import *
r = remote('challenge.com', 1234)

# Debug: What's the initial prompt?
print("=== Initial server message ===")
r.interactive()

# Oh, it needs a username first!
r = remote('challenge.com', 1234)
r.sendline(b"username")

# Debug: What happens after username?
print("=== After sending username ===")
r.interactive()
```
