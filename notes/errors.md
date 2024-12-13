---
aliases:
  - error
tags:
  - flashcard/active/ctf
  - notes/tbc
---

# EOFError  
EOFError :: "End Of File" error, which happens when {{server closes connection}}, {{Connection is lost}} or when {{We try to read from a closed connection}} <!--SR:!2024-12-15,1,230-->

pwntool raises EOFError when:
- {{can't read}} more data
- server {{disconnects}}
- connection {{times out}} <!--SR:!2024-12-18,4,270!2024-12-18,4,270!2024-12-18,4,270--> 

## How does try block work?

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

raise `Error` :: jumps to the error code <!--SR:!2024-12-17,3,250-->
except `Error`: <content> :: program reaches here if error is raised <!--SR:!2024-12-18,4,270-->




