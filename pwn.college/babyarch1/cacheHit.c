#define _GNU_SOURCE
#include <stdio.h> 
#include <stdint.h>
#include <x86intrin.h> // x86 in transit we get _mm_clflush, _mm_mfence, __rdtsc
#include <string.h>


#define BUFF_SIZE 8

char buffer[BUFF_SIZE];

int main(int argc, char** argv) {
	uint64_t start, end;
	
	// setting the buffer array to all 0
	memset(buffer, 0, sizeof(buffer));
	
	// flush all buffer memory from cache, no matter whether it's in the cache or not.
	// ensure that it is not in the cpu cache
	_mm_clflush(buffer);
	_mm_mfence();
	
	// Get High resolution start time
	start = __rdtsc();
	
	// First access - Note the weird access pattern
	// ((buffer[0] + 4) ^ 1) ^ 1 is NECESSARY
	// basically putting a virtual memory address in x
	// volatile to prevent optimization
	volatile uint64_t x = buffer[((buffer[0] + 4) ^ 1) ^ 1];



	// Here it comes _mm_mfence()!
	// This stops the CPU until the memory loads (accessing buffer) finishes
	// without _mm_mfence(), CPU might optimizes the performance
	// by executing __rdtsc() first while waiting for the memory access (from RAM)
	// which is called reordering of instruction of the CPU, or speculation
	// So it is a good practice to put _mm_mfence() after memory loads (accessing something)
	_mm_mfence();
	
	// Get High resolution end time
	end = __rdtsc();
	
	printf("Access 1 took %ld cycles\n", end - start);
	
	/**********************************************************************************/
	
	// Flush cache between accesses 
//	_mm_clflush(buffer);
	
	/**********************************************************************************/
	
	// Get High resolution start time		
	start = __rdtsc();
	
	// second access
	x = buffer[((buffer[0] + 4) ^ 1) ^ 1];
	_mm_mfence();
	
	// Get High resolution end time
	end = __rdtsc();
	
	printf("Access 2 took %ld cycles\n", end - start);
	
	return 0;
}
