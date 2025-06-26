# influence caching 
# pinning cpu core

- sched_setaffinity

we want the programs that interact with each other, to be using the same cache layer

# timing 

- should be taken via __rdtsc. 

- it is the counter inside CPU, which is the most accurate one.

# _mm_clflush(addr)

why is there an address?

the cache is large. So we need to evict a specific value

- cache is aligned by 64 bytes. _mm_clflush(0x1005) still flushes `0x1000 to 0x1064`

- so if the value is larger than 64 bytes. We need to call _mm_clflush multiple times. For example, calling in a for loop (jump every 64 bytes)

# fences (influencing speculating)

when fence function is encountered, CPU stops speculating until something

- __mm_mfence - wait for all memory operations to be completed (might be slower)
- __mm_lfence - wait for all memory loads to be completed (stopping any CPU speculating when it is waiting for accessing memory)
- __mm_sfence - wait for all memory stores to be completed  (never gonna speculatively stores memory anywhere. All stored values will be REAL)


# using caching as a side channel

Requirements
- ability influence target execution 
- access to memory region used by target 
	- could be in-process
	- could be shared memory 
	- could be kernel memory


# challenges
## cache prefetching

when it detects a for loop, it fetch ahead of time. It puts things into cache to try to optimize the performance

solution: when looping through data, mangle the index to confuse the CPU so that it won't prefetch and load them in memory.


# code

```
void victim_function(size_t idx) {
	volatile char x = buffer[idx * CAHCE_LINE_SIZE];
}
void pre_work() {
	uint8_t *addr;
	// ensure that the virtual memory is backed by physical memory.
	// Ensure that it does exists. Since if it is not, it will cause page fault
	memset(buffer, 0, sizeof(buffer));  
	for (int j = 0; j < BUFF_SIZE * CACHE_LINE_SIZE; j++) {
		addr = buffer + j;
		_mm_clflush(addr); // every clflush flushes 64 bytes
	}

}

uint64_t time_access_no_flsuh(void *p) {
	uint64_t start, end;
	start = __rdtsc();
	volatile uint64_x = *(volatile uint64_t*)p;
	_mm_mfence();
	end = __rdtsc();
	
	return end - start;
}


void post_work_inner_work(int mix_i) {
	uint8_t *addr;
	size_t cache_hit_threshold = CACHE_HIT_THRESHOLD;
	index index;
	uint64_t t_no_flush;
	index = mix_i * CACHE_LINE_SIZE;
	addr = buffer + index;
	t_no_flush = time_access_no_flush(addr);
	if (t_no_flush <= cache_hit_threshold) {
		printf("cache hit: %u %lu\n", mix_i, t_no_flush);
	}
}

void post_work() {
	for (size_t i = 0; i < BUFFER_SIZE;i++) {
		// ensure that CPU does NOT prefetch and add entries to cache
		int mix_i = ((i * 167) + 13) & 255; 
		post_work_inner_work(mix_i);
	}	
}

int main(int argc, char **argv) {
	if (argc != 2) {
		exit(1);
	}
	int index = atoi(argv[1]);
	
	if (index > BUFF_SIZE) {
		exit(2);
	}
	
	pre_work();
	printf("Done with pre-work\n");
	
	victim_function(index);
	
	printf("Done with post-work\n");
	
	post_work();
	return 0;
}
```









