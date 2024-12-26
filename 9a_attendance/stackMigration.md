# Stack migration 
migrate stack to some other location to continue ROP chain when buffer size is not enough

`buf` on .bss segment is just like `buf` locally but on some other places 

it makes use of the `function call`, `rbp`, `leave ; ret` mechanisms to not break the chain while "moving" to other location (which you already have written stuff there)

```
gets(buf)

or 

pop rdi,
buf,
gets
```
is basically the same thing, but the later you are just doing it during a ROP chain while not breaking the chain by smartly making use of `overwritten saved rbp (location of where you move to)` and how `leave ; ret` reacts with `rbp`, `rsp`

## Saved old rbp 
this needs to be written to the next buffer/payload/input address 
## `leave ; ret`
- at the end of payload of a frame 
- used to control rbp, move it to "restore" the nxt buffer address at the base of the frame
- used to contorl rsp at well, moving it to top of next frame. After `pop rbp`, `rsp` points back to something with `ret` and continue the ROP chain

## gets@plt
- before `leave ; ret`
- used to write another payload to the next buffer 

