#define _GNU_SOURCE


#include <sys/stat.h>
#include <fcntl.h> 
#include <string.h>
#include <x86intrin.h>
#include <sys/mman.h>      // For mmap, PROT_READ, PROT_WRITE, MAP_SHARED
#include <unistd.h>        // For close()
#include <sched.h>         // For cpu_set_t, CPU_ZERO, CPU_SET, sched_setaffinity
#include <math.h>          // For sqrtf()
#include <stdio.h>         // For printf()


#define GUARDED_ARRAY_LENGTH 128

// globals 

struct {
	char guarded_array[GUARDED_ARRAY_LENGTH];
	char secret_value[256];
} priv_struct;
char *shared_memory;

//
// setup work
//


// for cache side channel to work. The processes needs to be accessing the same underlying physical memory (mapped to shared memory)
void *open_shared_mem() {
	int ret;
	int fd = shm_open("/shm_f", O_RDWR | O_CREAT, S_IRWXU | S_IRWXG | S_IRWXO);
	ret = ftruncate(fd, 0x1000 * 256);
	char *ptr = (char *) mmap(0, 255* 0x1000, PROT_WRITE | PROT_READ, MAP_SHARED, fd, 0);
	close(fd);
	return ptr;
}

void set_affinity() {
	cpu_set_t set;
	CPU_ZERO(&set);
	CPU_SET(2, &set);
	sched_setaffinity(0, sizeof(set), &set);

}

int main(int argc, char** argv) {
	volatile char buff[8];
	volatile int run, index, do_exit = 0;
	
	// Place secret value in memory 
	// pinning the process to a specific cpu core
	// we need to manipulate the branch predictor
	// which operates per physical core
	set_affinity(); // pinning the process to a specific cpu core
	
	// moving values into a guarded array and secret value
	strcpy(priv_struct.guarded_array, "Here is my guarded value.");
	strcpy(priv_struct.secret_value, "pwned");
	
	// challenge opens up a shared memory 
	// Shared memory is used to interact with this victim program
	shared_memory = open_shared_mem();
	
	// communication channels
	// 0 = run
	// 1 = index that determines what the challenge is going to do
	// 2 = flag to exit program
	((volatile int *) shared_memory)[0] = 0;
	((volatile int *) shared_memory)[1] = 0;
	((volatile int *) shared_memory)[2] = 0;
	
	// no synchronization
	while (!do_exit) {
	
		// a run value is checked
		run = ((volatile int*) shared_memory)[0];
		
		
		// a busy loop 
		while (!run) {
			run = ((volatile int *) shared_memory)[0];
			do_exit = ((volatile int *) shared_memory)[2];
			sched_yield();
		}
		
		// if `run` is set
		// clear run flag and index
		run = 0;
		index = 0;
		
		// get new index from shared memory 
		index = ((volatile int *) shared_memory)[1];
		
		
		// some slow operation so that CPU branch pedictor gets activated
		
		// because CPU would wait here, not knowing which branch to take below
		// thus speculate on that
		volatile double tmp = (volatile double) ((int)(sqrtf(index * index) * 2 / 2));
		
		// conditional check
		// check if index is less than 128
		// 128 is the size of guarded array
		// 
		// branch check that is being targetted for speculative execution
		if (tmp < 128) {
			// shared memory here and the one in exploit code 
			// both point to the same physical memory
			// then, cache side-channel attack is available
			buff[0] = shared_memory[priv_struct.guarded_array[index] * 0x1000];
		}
	}
	printf("exiting\n");
}
