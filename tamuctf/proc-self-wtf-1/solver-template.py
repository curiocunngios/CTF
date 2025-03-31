from pwn import *

context.log_level = "debug"
io = remote("fuzzbox.addisoncrump.info", 1337)
io.interactive(prompt="")
