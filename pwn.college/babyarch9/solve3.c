#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>

int fd;
volatile char *shared_buffer;

void test_minimal_syscall() {
    printf("\n=== Minimal Syscall Test ===\n");
    
    uint32_t magic = 0x595055;
    memset((void*)shared_buffer, 0, 0x100000);

    uint32_t *header = (uint32_t*)shared_buffer;
    header[0] = magic;
    header[1] = 0x10;  // Starting instruction pointer

    uint8_t *code = (uint8_t*)(shared_buffer + 0x10);
    memset(code, 0, 0x100);
    
    // Put syscall instruction FIRST, exactly like the working version
    code[0] = 0x00;
    code[1] = 0x08;
    code[2] = 0x04;
    code[3] = 0xFF;  // termination
    code[4] = 0xFF;
    code[5] = 0xFF;
    
    printf("Syscall instruction at start: 0x%02x 0x%02x 0x%02x\n", code[0], code[1], code[2]);
    
    errno = 0;
    int result = ioctl(fd, 0x539, 0);
    printf("Result: %d, errno: %d\n", result, errno);
}

int main() {
    printf("Y85 Minimal Syscall Test\n");
    printf("========================\n");

    fd = open("/proc/ypu", O_RDWR);
    if (fd < 0) {
        perror("open /proc/ypu");
        return 1;
    }

    shared_buffer = mmap(NULL, 256 * 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (shared_buffer == MAP_FAILED) {
        perror("mmap");
        close(fd);
        return 1;
    }

    printf("Mapped shared buffer at %p\n", shared_buffer);
    
    test_minimal_syscall();

    munmap((void*)shared_buffer, 256 * 0x1000);
    close(fd);
    return 0;
}
