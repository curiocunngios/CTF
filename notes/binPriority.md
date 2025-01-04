---
aliases:
  - free list priority
tags:
  - flashcard/active/ctf/A
---

# Bin choosing priority
When it comes to the priority of which bins to choose when chunks get freed or reallocated:
## free()
1. `tcache` whenever {{chunk size is <= 410}} and it being not full
2. `fastbin` if {{chunk size is <= 80 and tcache is full}}
3. `unsortedbin` when the {{Top chunk or a freed chunk is not neighbour}}
## malloc()
1. `tcache` whenever {{chunk size is <= 408}} and it being not empty
2. `fastbin` if {{chunk size is <= 80 and is not empty}}
3. `unsortedbin` if {{there are no suitable chunk in small/ large bins.}} Return if size {{exactly match}}, if not then {{cut some and return}}