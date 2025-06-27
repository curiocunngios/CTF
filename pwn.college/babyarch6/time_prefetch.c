#define _GNU_SOURCE

#include <sys/sendfile.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <x86intrin.h>
#include <sys/mman.h>


// timing side-channel on prefetch instruction 
int repeat_measure(void *ptr) {
	int sum;
	sum = 0;
	for (int i = 0;i < 10; i++) {
		sum += measure(ptr);
	}
	return sum;


}

// time the prefetch operation
int measure (void *ptr) {
	uint64_t start, end;
	start = __rdtsc();
	
	// lfences to prevent speculative execution
	_mm_mfence();
	_mm_prefetch(ptr, 2);
	_mm_mfence();	
	end = __rdtsc();
	return end - start;
}


int main() {

	// return virtual memory
	int *ptr = (int *) mmap(NULL, 0x1000, PROT_WRITE | PROT_READ, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
	// write to the memory to ensure that it is backed by physical address 
	*ptr = 0x1337;
	printf("mmap returned: %p\n", ptr);
	
	// start from 10 pages behind the ptr
	// if the memory address does not exists, prefetch takes longer
	// we can do this to search for valid 
	for (long i = ptr - (10 * 0x1000); i < ptr + (10 * 0x1000); i += 0x1000) {
		printf("addr: %p measurement: %d\n", i, repeat_measure(i));
	}
	printf("addr: %p measurement: %d\n", 0xdeaddeadbeefbeef, repeat_measure(0xdeaddeadbeefbeef));
	// block the program to inspect
	char buf[20];
	scanf("%1s", buf);

}

