---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - pyhton
tags:
  - flashcard/active/ctf/hi
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
## How does try block work?

raise `Error` :: jumps to the error code 
except `Error`: <content> :: program reaches here if {{ error is raised}}
## EOFError  
EOFError ::: "End Of File" error, which happens when {{server closes connection}}, {{Connection is lost}} or when {{We try to read from a closed connection}}

pwntool raises EOFError when    
??  
- can't read more data 
- server disconnects 
- connection times out

