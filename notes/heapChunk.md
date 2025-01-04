---
aliases:
  - heap chunk structure
  - chunk memory layout
tags:
  - flashcard/active/ctf/A
---

# Dual Roles of Heap Chunk

### Allocated Chunk:
```
+------------------+  ← High address
|                  |
|      DATA        |
|                  |
|                  |
+------------------+
|     HEADER       |
+------------------+  ← Low address
```
The allocated chunk structure consists of:
- {{DATA section for user data}}
- {{HEADER containing metadata}}, i.e. data of previous chunk and the size of the current chunk with some bits representing crucial information <!--SR:!2025-01-05,1,230!2025-01-08,4,270-->

### Freed Chunk:
```
+------------------+  ← High address
|    NON_USE      |
+------------------+
| LARGE_BCK (8B)  |
+------------------+
| LARGE_FD  (8B)  |
+------------------+
|    BCK    (8B)  |
+------------------+
|    FD     (8B)  |
+------------------+
|    HEADER       |
+------------------+  ← Low address
```
The freed chunk structure repurposes memory as:
- {{First 32 bytes get used for fd/bck pointers}}, which are the pointers pointing to {{next/previous chunks for the list structure of the bins}}
- {{FD/BCK pointers form linked list connections}}
- {{LARGE_FD/BCK used for larger bin connections}} <!--SR:!2025-01-05,1,230!2025-01-05,1,230!2025-01-05,1,230!2025-01-05,1,230-->