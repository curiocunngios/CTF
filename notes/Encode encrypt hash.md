---
aliases:
  - encode 
  - encrypt
  - hash
tags:
  - flashcard/active/ctf
  - notes/tbc
---

# Encoding and Hash Basics

Encoding is a {{reversible transformation}} for {{data representation}} such that the data may be in a format that is
- {{Readable/transmittable}} through specific systems
- Reversible back to {{original data}}
- Compliant with specific {{protocols/standards}} <!--SR:!2024-12-13,1,221!2024-12-13,1,221!2024-12-13,1,221!2024-12-13,1,221!2024-12-13,1,221-->


Encryption {{scrambles data using a key}}, only reversible with {{the correct key.}}  


hash is a **one-way function** that converts any data to a {{fixed-length digest}} that cannot be mathematically reversed <!--SR:!2024-12-13,1,221!2024-12-13,1,221!2024-12-13,1,221!2024-12-13,1,221-->

## Examples - Different types of encoding for "Firebird"   
 
- ASCII: Firebird :)
- Base64: RmlyZWJpcmQgOik=
- Hex: 46 69 72 65 62 69 72 64 20 3A 29

## Hashing Types features
- MD5 :: Fast but insecure <!--SR:!2024-12-13,1,221!2024-12-13,1,221-->
- SHA-1 :: Better but still breakable <!--SR:!2024-12-13,1,210!2024-12-13,1,221-->
- SHA-256 :: Currently secure <!--SR:!2024-12-13,1,221!2024-12-13,1,221-->
- SHA-512 :: Very secure, longer hash <!--SR:!2024-12-13,1,210!2024-12-13,1,221-->

## Example shell commands for encoding, hashing
??
```bash
# Base64 encode
echo "hello" | base64
# Base64 decode
echo "aGVsbG8=" | base64 -d
# Calculate MD5
echo "hello" | md5sum
```
<!--SR:!2024-12-13,1,221-->