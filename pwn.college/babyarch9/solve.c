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



void exploit() {
	printf("\n=== Testing Magic Number Formats ===\n");
    
	uint32_t magic_variants = 0x595055;   



	printf("Testing magic 0x%08x: ", magic_variants);

	memset((void*)shared_buffer, 0, 0x1000);

	uint32_t *header = (uint32_t*)shared_buffer;
	header[0] = magic_variants;
	header[1] = 0;

	// Minimal program: just HALT
	uint32_t *instructions = (uint32_t*)(shared_buffer + 8);
	instructions[0] = 0 // y85 shellcode starts here!

	errno = 0;
	int result = ioctl(fd, 0x539, 0);
	printf("result=%d, errno=%d\n", result, errno);
    
}




int main() {
	printf("Y85 VM Initialization Debug\n");
	printf("===========================\n\n");

	fd = open("/proc/ypu", O_RDWR);


	shared_buffer = mmap(NULL, 256 * 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);



	exploit();

	close(fd);
	return 0;
}
