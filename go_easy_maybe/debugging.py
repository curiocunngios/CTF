def calculate_index(k):
    n = k + 0x24
    # Full 128-bit multiplication
    mul = n * 0xdd67c8a60dd67c8b
    
    # Split into RDX:RAX
    rdx = (mul >> 64) & 0xFFFFFFFFFFFFFFFF  # Upper 64 bits
    rax = mul & 0xFFFFFFFFFFFFFFFF          # Lower 64 bits
    
    # Debug prints
    print(f"\nDebug for k={k}:")
    print(f"n = {n}")
    print(f"Full multiplication = {hex(mul)}")
    print(f"RDX (upper 64) = {hex(rdx)}")
    print(f"RAX (lower 64) = {hex(rax)}")
    
    # Continue with the rest of the calculation
    rdx = rdx >> 5  # shr rdx,0x5
    print(f"After shift = {hex(rdx)}")
    
    # Calculate final index
    result = n - ((((rdx << 3) + rdx) << 2) + rdx)
    print(f"Final index = {result}")
    
    return result

# Test for first few values
for k in range(3):
    idx = calculate_index(k)
    print(f"k={k} -> idx={idx}")