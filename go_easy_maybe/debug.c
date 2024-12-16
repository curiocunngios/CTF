#include <stdio.h>
#include <stdint.h>

int calculate_index(int k)
{
    int n = k + 0x24;
    uint64_t const_val = 0xdd67c8a60dd67c8b;

    // Perform multiplication
    __int128 result = (__int128)n * const_val;

    // Split into high/low 64 bits
    uint64_t high = result >> 64;
    uint64_t low = result & (((__int128)1 << 64) - 1);

    printf("\nDebug for k=%d:\n", k);
    printf("n = %d\n", n);
    printf("Multiplication = 0x%016lx%016lx\n",
           (uint64_t)(result >> 64),
           (uint64_t)(result & 0xFFFFFFFFFFFFFFFF));
    printf("High 64 bits = 0x%lx\n", high);
    printf("Low 64 bits = 0x%lx\n", low);

    // Continue assembly calculation
    high = high >> 5;
    // Note: the Python version has operator precedence issue in this line:
    // (((high << 3) + high) << 2 + high)
    // Let's fix it to match assembly:
    int result_idx = n - ((((high << 3) + high) << 2) + high);

    printf("k=%d -> idx=%d\n", k, result_idx);
    return result_idx;
}

int main()
{
    for (int k = 0; k < 3; k++)
    {
        calculate_index(k);
    }
    return 0;
}