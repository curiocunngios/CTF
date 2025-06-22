# load linux kernel with gdb:

- gdb linux-5.4/vmlinux

# attach to port that launch.sh (QEMU) opened with -s
- target remote :1234

## To find the actual function address:

```bash
/ # cat /proc/kallsyms | grep device_write
ffffffffc0000abc t device_write    [babykernel_level1_0]
```

## breaking at function start:
```
b * device_write
```
## breaking at specifc lines:
```
b * ffffffffc0000abc - <offset_to_function_start> + <offset_to_line>

b * ffffffffc00007cc - 0x80c + 0x868
```
