---
aliases:
  - html load order
tags:
  - flashcard/active/ctf
  - notes/tbc
---

# HTML code loading order
HTML loads {{top to bottom}}
- \<head\> loads first
  - {{Metadata (?)}}
  - CSS (style.css)
- \<body\> loads next
  - {{Visual elements}}
  - Scripts, which also {{execute in order from top to bottom}} <!--SR:!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250!2024-12-17,3,250-->
