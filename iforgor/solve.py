def rotate_left(arr, n):
    return arr[n:] + arr[:n]

def decrypt(hex_output):
    array1 = [0x06, 0x42, 0x09, 0xf2, 0xb4, 0xf7, 0xaa, 0x65,
              0xa6, 0xf5, 0x3c, 0x72, 0x67, 0xbd, 0xd4, 0xdf]

    array2 = [0x3d, 0xa4, 0xe5, 0x14, 0xc6, 0xf9, 0xc8, 0x23,
              0x9b, 0x9a, 0xc1, 0x20, 0x4e, 0x0d, 0x42, 0x2d]
    
    result = bytes.fromhex(hex_output)
    result_blocks = [result[i:i+16] for i in range(0, len(result), 16)]
    
    # First block
    input_block = []
    for i in range(16):
        input_block.append(result_blocks[0][i] ^ array1[i] ^ array2[i])
    
    # Subsequent blocks
    curr_array2 = array2.copy()
    for round in range(1, 4):
        curr_array2 = rotate_left(curr_array2, 3)
        
        for i in range(16):
            block_offset = round * 16
            # Use the previous round's result block
            input_byte = result_blocks[round][i] ^ result_blocks[round-1][i] ^ curr_array2[i]
            input_block.append(input_byte)
    
    return bytes(input_block)

print(decrypt("5d8a8d81094757190a07cc217683e0972713401648b0fdbb4116a20f2bd677009230db8c8990b3b6033b9fabcec2b1f908f1fbc284d29e8ba7de8b6d370a9262"))