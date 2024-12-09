---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - pyhton
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---


```py
try:
    # Code that might cause errors goes in try block
    conn = remote("chal.firebird.sh", 35005)
    # ...
    # if something went wrong
    raise EOFError # jumps to the error code to close the connection
except EOFError:  # Handles connection errors
    conn.close()
    continue  # Goes back to start of while loop
```
## EOFError  
EOFError means "End Of File" error  

In networking, the error occurs when   
??  
- Server closes connection
- Connection is lost
- We try to read from a closed connection

pwntool raises EOFError when   
??  
- can't read more data 
- server disconnects 
- connection times out


