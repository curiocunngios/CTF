# 1. 
it takes longer to take stuff from RAM 

# whats happening in CPU while waiting

there's cache layer that might not even let the assembly instruction touch RAM at all

caching layer is super fast, super local memory

if CPU has accessed that data recently, it will be what that data is, in cache.


# whats happening in CPU while waiting 2
while waiting, typically during memory accesses

CPU might be predicting branches (speculating), assuming some values and jump to some branches

if the predication fails, just undo that 

But that value has already been accessed. It leaves a sort of "fingerprint" on the cache

how does CPU decide which branch to go

- the branch prediction unit

- need to influence the branch prediction unit


# flushing

when i flush something from the cache, I am flushing 64 bytes

_mm_clflush(0x1000) flushes addr 0x1000 to 0x1064

# cores

program needs to be running on the same core

