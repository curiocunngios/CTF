---
aliases:
  - encode 
  - encrypt
  - hash
tags:
  - flashcard/active/ctf
  - notes/tbc
---

# Encoding and encryption Basics

Encoding is a {{reversible transformation}} for {{data representation}} such that the data may be in a format that is
- {{Readable/transmittable}} through specific systems
- Reversible back to {{original data}}
- Compliant with specific {{protocols/standards}} <!--SR:!2024-12-17,3,221!2024-12-17,3,221!2024-12-17,3,221!2024-12-17,3,221!2024-12-16,2,201-->

Encryption {{scrambles data using a key}}, only reversible with {{the correct key.}} <!--SR:!2024-12-17,3,257!2024-12-17,3,257-->  

## Examples - Different types of encoding for "Firebird"   
 
- ASCII: Firebird :)
- Base64: RmlyZWJpcmQgOik=
- Hex: 46 69 72 65 62 69 72 64 20 3A 29

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
<!--SR:!2024-12-17,3,221-->