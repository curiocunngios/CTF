---
aliases:
  - Segment registers
tags:
  - flashcard/active/ctf
---

# Segment registers
Segment registers are:
- Special registers (cs, ds, ss, es, fs, gs) {{used for memory segmentation}}
- Originally used in 16-bit era to access memory beyond 64KB (?)
- In modern x86_64:
  - Most (cs, ds, ss, es) aren't actively used for segmentation anymore
  - fs/gs are repurposed for thread-local storage and OS-specific data <!--SR:!2024-12-15,1,230-->

