def ror(value, shift, bits=64):
    shift = shift & (bits - 1)  # Normalize shift count
    return ((value >> shift) | (value << (bits - shift))) & ((1 << bits) - 1)


rbp_0x8 = 0xd0f7ac93538ad5b5

rbp_0x8 = rbp_0x8 ^ 0xd5912ad9c3bee799 # reverse XOR


# reverse rol (ror)
rbp_0x8 = ror(rbp_0x8, 32)

# reverse add 
rbp_0x8 -= 0x7204bb56150aa739


# reverse rol (ror)
rbp_0x8 = ror(rbp_0x8, 32)

rbp_0x8 -= 0xbf272eb7a17bc158

# reverse rol (ror)
rbp_0x8 = ror(rbp_0x8, 32)

rbp_0x8 = rbp_0x8 ^ 0x29c4e0426e5ae53f

print(rbp_0x8.to_bytes(8, 'little'))