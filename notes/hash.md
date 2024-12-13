---
aliases:
  - hash
  - hash function
tags:
  - flashcard/active/ctf
---

# Hash
hash is a **one-way function** that converts any data to a {{fixed-length digest}} that cannot be mathematically reversed <!--SR:!2024-12-14,1,230!2024-12-16,3,250-->

## Hash digests
Hash digests:
- should be {{easy to compute}}
- are {{irreversible * (can bruteforce)}}
- should be hard to find two different data with {{same digest}} <!--SR:!2024-12-14,1,230!2024-12-16,3,250!2024-12-16,3,250-->

![hash function](../linked%20images/hash.png)

The digest of hashing, the result of hashing, are called the {{hash value, hash code, or simply called hashes}} <!--SR:!2024-12-14,1,230-->

## Hash Types features
- MD5 :: Fast but insecure <!--SR:!2024-12-14,1,230-->
- SHA-1 :: Better but still breakable <!--SR:!2024-12-14,1,230-->
- SHA-256 :: Currently secure <!--SR:!2024-12-14,1,230-->
- SHA-512 :: Very secure, longer hash <!--SR:!2024-12-14,1,230-->





