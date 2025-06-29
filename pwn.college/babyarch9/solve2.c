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

void test_incremental_build() {
    printf("\n=== Incremental Syscall Build ===\n");
    
    uint32_t magic = 0x595055;
    memset((void*)shared_buffer, 0, 0x100000);

    // Write "/flag" string to memory first
    char *flag_path = (char*)(shared_buffer + 0x1000 + 0x50);
    strcpy(flag_path, "/flag");
    printf("Flag path written: '%s' at data offset 0x50\n", flag_path);

    uint32_t *header = (uint32_t*)shared_buffer;
    header[0] = magic;
    header[1] = 0x10;  // Starting instruction pointer

    uint8_t *code = (uint8_t*)(shared_buffer + 0x10);
    
    printf("\n--- Test 1: Just syscall (known working) ---\n");
    memset(code, 0, 0x100);
    code[0] = 0x00;
    code[1] = 0x08;
    code[2] = 0x04;
    code[3] = 0xFF;
    code[4] = 0xFF;
    code[5] = 0xFF;
    
    errno = 0;
    int result = ioctl(fd, 0x539, 0);
    printf("Result: %d, errno: %d (should reach sys_open)\n", result, errno);
    
  
    printf("\n--- Test 3: Two IMM + syscall ---\n");
    memset(code, 0, 0x100);
    int pc = 0;
    
    // Two IMM instructions
    code[pc++] = 0x20;  // IMM A, 0x50
    code[pc++] = 0x00;
    code[pc++] = 0x50;
    
    code[pc++] = 0x20;  // IMM B, 0
    code[pc++] = 0x01;
    code[pc++] = 0x00;
    
    // Syscall
    code[pc++] = 0x00;
    code[pc++] = 0x08;
    code[pc++] = 0x04;
    
    // Termination
    code[pc++] = 0xFF;
    code[pc++] = 0xFF;
    code[pc++] = 0xFF;
    
    printf("Instructions: IMM A,0x50; IMM B,0; then syscall\n");
    errno = 0;
    result = ioctl(fd, 0x539, 0);
    printf("Result: %d, errno: %d\n", result, errno);
    
    printf("\n--- Test 4: Three IMM + syscall ---\n");
    memset(code, 0, 0x100);
    pc = 0;
    
    // Three IMM instructions
    code[pc++] = 0x20;  // IMM A, 0x50
    code[pc++] = 0x00;
    code[pc++] = 0x50;
    
    code[pc++] = 0x20;  // IMM B, 0
    code[pc++] = 0x01;
    code[pc++] = 0x00;
    
    code[pc++] = 0x20;  // IMM C, 0
    code[pc++] = 0x02;
    code[pc++] = 0x00;
    
    // Syscall
    code[pc++] = 0x00;
    code[pc++] = 0x08;
    code[pc++] = 0x04;
    
    // Termination
    code[pc++] = 0xFF;
    code[pc++] = 0xFF;
    code[pc++] = 0xFF;
    
    printf("Instructions: IMM A,0x50; IMM B,0; IMM C,0; then syscall\n");
    errno = 0;
    result = ioctl(fd, 0x539, 0);
    printf("Result: %d, errno: %d\n", result, errno);
    
    printf("\n--- Test 5: Check if it's the register values ---\n");
    memset(code, 0, 0x100);
    pc = 0;
    
    // Try different register values
    code[pc++] = 0x20;  // IMM A, 0  (instead of 0x50)
    code[pc++] = 0x00;
    code[pc++] = 0x00;
    
    code[pc++] = 0x20;  // IMM B, 0
    code[pc++] = 0x01;
    code[pc++] = 0x00;
    
    code[pc++] = 0x20;  // IMM C, 0
    code[pc++] = 0x02;
    code[pc++] = 0x00;
    
    // Syscall
    code[pc++] = 0x00;
    code[pc++] = 0x08;
    code[pc++] = 0x04;
    
    // Termination
    code[pc++] = 0xFF;
    code[pc++] = 0xFF;
    code[pc++] = 0xFF;
    
    printf("Instructions: IMM A,0; IMM B,0; IMM C,0; then syscall\n");
    errno = 0;
    result = ioctl(fd, 0x539, 0);
    printf("Result: %d, errno: %d\n", result, errno);
}

int main() {
    printf("Y85 Incremental Syscall Test\n");
    printf("============================\n");

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
    
    test_incremental_build();

    munmap((void*)shared_buffer, 256 * 0x1000);
    close(fd);
    return 0;
}
