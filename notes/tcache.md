---
aliases:
  - tcache structure
  - tcache management
tags:
  - flashcard/active/ctf/heap/tcache
---

# Tcache Bins Structure

## Visual Layout
```
malloc_state (libc.so)
+------------------+
|       ...        |
+------------------+
|       top        |
+------------------+
|      tcache      |  ←--+
+------------------+     |
                         |
tcache_perthread_struct  |
+------------------+ <---+
| entry[0]         |--→ [chunk] → [chunk] → null
+------------------+
| entry[1]         |--→ [chunk] → null
+------------------+
| entry[2]         |--→ null
+------------------+
|      ...         |
+------------------+
| entry[63]        |
+------------------+
```

## Key Properties

### Basic Structure
- Located in {{first heap chunk of main arena}}
- Uses {{single linked list}} data structure
- Total length is {{64 bins, i.e. the entries that manages chunks of specific size}}

### Size Management
- Chunk sizes range from {{0x10 to 0x400}}
- Size increment (stride) is {{0x10 bytes}}
- Each entry can hold {{maximum 7 chunks}}

### Operation Characteristics
- Operates as {{First In Last Out (FILO)}}
- New chunks added via {{head insertion i.e. insert at the beginning}}. The "beginning" is not the entry pointing to null (the first entry)

### Implementation Details
```c
typedef struct tcache_entry {
    struct tcache_entry* next;  // Single linked list pointer
} tcache_entry;

typedef struct tcache_perthread_struct {
    char counts[TCACHE_MAX_BINS];  // Tracks number of chunks per bin
    tcache_entry* entries[TCACHE_MAX_BINS];  // Array of bin pointers
} tcache_perthread_struct;
```

### Historical Context
- Introduced in Glibc version 2.26
- Significantly improved allocation performance
- Changed heap exploitation techniques