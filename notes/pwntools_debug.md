# Debugging in CTF/Pwntools Context

What is debugging in CTF  
??  
- Understanding what data server sends
- Figuring out why your script isn't working
- Learning how the challenge behaves
- Testing different inputs manually

Why use r.interactive()  
??  
- first see what server sends with your previous code  
- try different input by changing the script content manually
- Understand the challenge flow better
```python
# Example scenario: 
from pwn import *
r = remote('challenge.com', 1234)

# Your script isn't working, so add:
print("Debug: Checking server response...")
r.interactive()
```
