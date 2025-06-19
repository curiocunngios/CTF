//getenv.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    printf("0x%08x\n", (getenv("SHELLCODE")));
    return 0;
}
