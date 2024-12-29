from pwn import *
import z3

def solve_sudoku(instance):
    grid = [[z3.Int('grid_%s_%s' % (i+1, j+1)) for j in range(9)] for i in range(9)]
    s = z3.Solver() # to add constraints ( like equations)

    ## TODO ##
    # Add constraints for given numbers
    # Add constraints for given numbers
    for i in range(9):
        for j in range(9):
            if instance[i][j] != 0:
                s.add(grid[i][j] == instance[i][j])
    
    # All numbers should be between 1 and 9
    for i in range(9):
        for j in range(9):
            s.add(z3.And(grid[i][j] >= 1, grid[i][j] <= 9))
    
    # Each row should contain distinct numbers
    for i in range(9):
        s.add(z3.Distinct(grid[i]))
    
    # Each column should contain distinct numbers
    for j in range(9):
        column = [grid[i][j] for i in range(9)]
        s.add(z3.Distinct(column))
    
    # Each 3x3 box should contain distinct numbers
    for box_i in range(3):
        for box_j in range(3):
            box = []
            for i in range(3):
                for j in range(3):
                    box.append(grid[3*box_i + i][3*box_j + j])
            s.add(z3.Distinct(box))
    if s.check() == z3.sat:
        m = s.model()
        return [ [ m.evaluate(grid[i][j]) for j in range(9) ] for i in range(9) ]

def main():
    context.log_level = 'debug'
    r = process('./master')
    r = remote('chal.firebird.sh', 35054)
    instance = [[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]]
    for i in range(30):
        r.recvuntil(b':\n')
        for h in range(9):
            line = r.recvline()
            for k in range(9):
                char = chr(line[k*3])
                instance[h][k] = int(char) if char != '.' else 0
        print(type(instance))
        print(instance)
        solution = solve_sudoku(instance)
        r.recvuntil(b'Please enter the solution in one line: ')
        r.sendline(''.join([str(solution[i][j]) for i in range(9) for j in range(9)]))
    r.interactive()

    
if __name__ == "__main__":
    main()
    