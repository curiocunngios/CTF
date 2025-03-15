#!/bin/bash
gcc -g -no-pie -w -Wl,-z,relro -fno-stack-protector $1
patchelf --set-interpreter ./ld-linux-x86-64.so.2 a.out
patchelf --replace-needed libc.so.6 ./libc.so.6 a.out
