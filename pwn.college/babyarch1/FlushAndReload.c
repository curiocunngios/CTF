#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <x86intrin.h>

#define BUFFER_SIZE 256
// bigger gaps between data in buffer 
// to prevent spatial prefetch from CPU
#define CACHE_LINE_SIZE 1024
#define CACHE_HIT_THRESHOLD 60

// Global buffer - needs to be large enough for all possible indices
char buffer[BUFFER_SIZE * CACHE_LINE_SIZE];

void victim_function(size_t idx) {
    _mm_mfence(); 
    volatile char x = buffer[idx * CACHE_LINE_SIZE];
    _mm_mfence(); 
}

void pre_work() {
	uint8_t *addr;
	// ensure that the virtual memory is backed by physical memory.
	// Ensure that it does exists. Since if it is not, it will cause page fault
	memset(buffer, 0, sizeof(buffer));  
	for (int j = 0; j < BUFFER_SIZE * CACHE_LINE_SIZE; j += CACHE_LINE_SIZE) {
		addr = buffer + j;
		_mm_clflush(addr); // every clflush flushes 64 bytes
	}
	_mm_mfence(); // ensure all flushes complete
}

uint64_t time_access_no_flush(void *p) {
	uint64_t start, end;

	// start the timer
	start = __rdtsc();

	// accessing the address p 
	// which is buffer at a certain index
	volatile uint64_t x = *(volatile uint64_t*)p;

	// ensure the memory load operation finishes
	_mm_mfence();

	// end the timer
	end = __rdtsc();

	return end - start;
}

void post_work_inner_work(int mix_i) {
	
	// just a pointer 
	uint8_t *addr;
	
	// just the threshold 
	size_t cache_hit_threshold = CACHE_HIT_THRESHOLD;
	
	// index used to access the buffer 
	size_t index;
	
	// time used to access the buffer
	uint64_t time;
	
	// index used to access the buffer 
	
	index = mix_i * CACHE_LINE_SIZE;
	addr = buffer + index;
	time = time_access_no_flush(addr);
	if (time <= cache_hit_threshold) {
		printf("cache hit: %u %lu\n", mix_i, time);
	}
}

void post_work() {
	for (size_t i = 0; i < BUFFER_SIZE; i++) {
		// mangle the index
		// accessing them in random order
		// prevent temporal prefetch
		// ensure that CPU does NOT prefetch and add entries to cache
		int mix_i = ((i * 167) + 13) & 255; 
		//int mix_i = i;
		//printf("mix_i: %u\n", mix_i);
		post_work_inner_work(mix_i);
	}
}

int main(int argc, char **argv) {
    if (argc != 2) {
        printf("Usage: %s <index>\n", argv[0]);
        exit(1);
    }
    int index = atoi(argv[1]);
    
    if (index >= BUFFER_SIZE) {
        printf("Index must be less than %d\n", BUFFER_SIZE);
        exit(2);
    }
    
    // flushes the cache
    // ensure that the cache does not contain any buffer[] data 
    pre_work();
    printf("Done with pre-work\n");
    
    
    // accesses buffer at the inputted index
    victim_function(index);
    printf("Done with victim function\n");
    //_mm_mfence();
    // search for all indecies to look for the one with fastest access 
    // which means it's in cache
    // which means it was the inputted index 
    post_work();
    printf("Done with post-work\n");
    
    return 0;
}
