import random
from random import randint

def generate_grid():
    random.seed(3211210)
    arr = ['j', 'b', 'c', 'd', '2', 'f', 'g', 'h', '1', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'y',
           'v', '3', '}', '{', '_']
    t = []
    for i in range(len(arr), 0, -1):
        l = randint(0, i-1)
        t.append(arr[l])
        arr.remove(arr[l])
        arr.reverse()
    return t

def decrypt(ciphertext, grid):
    plaintext = ""
    
    for k in range(0, len(ciphertext)-1, 2):
        q1 = grid.index(ciphertext[k])
        q2 = grid.index(ciphertext[k+1])
        
        # Same row
        if q1 // 5 == q2 // 5:
            plaintext += grid[(q1//5)*5 + ((q1-1)%5)]
            plaintext += grid[(q2//5)*5 + ((q2-1)%5)]
        # Same column
        elif q1 % 5 == q2 % 5:
            plaintext += grid[((q1//5 - 1) % 5 * 5) + (q1%5)]
            plaintext += grid[((q2//5 - 1) % 5 * 5) + (q2%5)]
        # Rectangle rule
        else:
            plaintext += grid[(q1//5)*5+(q2%5)]
            plaintext += grid[(q2//5)*5+(q1%5)]
    
    return plaintext

# Generate the grid
grid = generate_grid()

# Print the grid for reference
print("Grid:")
for i in range(5):
    print(grid[i*5:i*5+5])

# Decrypt the ciphertext
ciphertext = "yjp}b{k{_vog1pnb2j31dhs1bsptln"
flag = decrypt(ciphertext, grid)
print("\nDecrypted flag:", flag)
