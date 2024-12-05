To actually input a null byte through terminal/stdin:

- You can't type it directly (null terminates the string)
- You need to use Python or another program to send the raw bytes

```py
from pwn import *
p = process('./program')
p.sendline(b'nothing\x00')  # This will actually send a null byte
```


or using a file 

```py
with open('input', 'wb') as f:
    f.write(b'nothing\x00')
```
