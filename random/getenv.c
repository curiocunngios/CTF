//getenv.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    printf("0x%08x\n", (getenv("SHELLCODE")) - 1); // no + strlen(SHELLCODE=) probably because programs get updated and 'SHELLCODE=' is gone
    return 0;
}


// SHELLCODE= (shellcode)

// (shellcode)
