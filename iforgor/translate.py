array1 = [0x06, 0x42, 0x09, 0xf2, 0xb4, 0xf7, 0xaa, 0x65,
            0xa6, 0xf5, 0x3c, 0x72, 0x67, 0xbd, 0xd4, 0xdf,
            0x3d, 0xa4, 0xe5, 0x14, 0xc6, 0xf9, 0xc8, 0x23,
            0x9b, 0x9a, 0xc1, 0x20, 0x4e, 0x0d, 0x42, 0x2d]

input = input()
input_copy = [0] * 64
result = [0] * 16
#"5d8a8d81094757190a07cc217683e0972713401648b0fdbb4116a20f2bd677009230db8c8990b3b6033b9fabcec2b1f908f1fbc284d29e8ba7de8b6d370a9262"
i = 0

length = len(input)
while (i < length):
    input_copy[i] = input[i]
    i = i + 1
for i in range (length, 0x40):
    input_copy[i] = 0


for i in range(0x10):
    result[i] = input_copy[i] ^ array1[i] ^ array1[i + 0x10]
    print(result[i])

for i in range(4):
    for j in range(0x10):
        local38 = array1[0x10]
        for k in range(10):
            array1[i - 1 + 0x10] = array1[ i + 10]

    for c in range(0x10):
        result[j] = input_copy[c + i * 0x10] ^ result[i] ^ array1[c + 0x10]