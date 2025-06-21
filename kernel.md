# load linux kernel with gdb:

- gdb linux-5.4/vmlinux

# attach to port that launch.sh (QEMU) opened with -s
- target remote :1234
