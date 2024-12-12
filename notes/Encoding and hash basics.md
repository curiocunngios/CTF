---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - Encryption
  - Encoding 
  - hash
  - basic
tags:
  - flashcard/active/ctf/hi
  - function/index
  - language/in/English
---

# Encoding and Hash Basics

Base64 decode command ::: base64 -d or base64 --decode

Encoding is a process of transforming data (especially binary data) into a format that is  
??  
1. Readable/transmittable through specific systems
2. Reversible back to original data
3. Compliant with specific protocols/standards
## Different types of encoding for "Firebird"   
??  
- ASCII: Firebird :)
- Base64: RmlyZWJpcmQgOik=
- Base32: IZUXEZLCNFZGIIB2FE======
- Hex: 46 69 72 65 62 69 72 64 20 3A 29

## difference between encoding and encryption  
??  
- Encoding: Reversible transformation for data representation
- Encryption: Scrambles data using a key, only reversible with the correct key

hash ::: A one-way function that converts any data to a fixed-length digest that cannot be mathematically reversed <!--SR:!2024-12-02,1,230!2000-01-01,1,250-->

Properties of hash functions   
??
- Easy to compute
- Irreversible
- Hard to find collisions
- Small input change causes large output change (avalanche effect)


## Encoding Types  
- ASCII ::: Basic text encoding
- Base64 ::: Binary-to-text encoding
- UTF-8 ::: Unicode encoding
- Hex ::: Base16 encoding

## Hashing Types
- MD5 ::: Fast but insecure
- SHA-1 ::: Better but still breakable <!--SR:!2024-12-02,1,230!2000-01-01,1,250-->
- SHA-256 ::: Currently secure
- SHA-512 ::: Very secure, longer hash <!--SR:!2024-12-02,1,230!2000-01-01,1,250-->

## Basic Commands
```bash
# Base64 encode
echo "hello" | base64
# Base64 decode
echo "aGVsbG8=" | base64 -d
# Calculate MD5
echo "hello" | md5sum
```