Symbolic execution in the context of PWN (binary exploitation) in CTFs is a program analysis technique where instead of running a program with concrete values, variables are treated as symbolic values or expressions.


Example:
```python
import angr
import claripy

# Load binary
proj = angr.Project('./vulnerable_binary')

# Create symbolic input
flag_len = 20
flag = claripy.BVS('flag', flag_len * 8)

# Create initial state
state = proj.factory.entry_state(args=['./vulnerable_binary'], stdin=flag)

# Add constraints (example: input must be printable)
for byte in flag.chop(8):
    state.solver.add(byte >= 0x20)
    state.solver.add(byte <= 0x7f)

# Run symbolic execution
sim = proj.factory.simulation_manager(state)
sim.explore(find=0x400goals, avoid=0x400bad)

# If solution found, solve for concrete values
if sim.found:
    solution = sim.found[0].solver.eval(flag, cast_to=bytes)
    print("Found solution:", solution)
```

Would you like me to explain the code or elaborate on any specific aspect of symbolic execution?



I'll break down the key concepts from the PDF in a beginner-friendly way, focusing on symbolic execution using z3 and angr for binary exploitation.

1. Basic Concept First - What is Symbolic Execution?

Think of it like algebra, but for programs:
- Normal execution: x = 5, y = x + 3 (y becomes 8)
- Symbolic execution: x = SYMBOL, y = SYMBOL + 3 (y is stored as an expression)

2. Tools We'll Use:
- z3: A solver that helps find values that satisfy conditions
- angr: A framework that helps analyze programs symbolically (? what does it mean by analyzing programs symbolically lol)


1. Simple z3 Example:
Let's solve a basic equation: Find x where (x + 5) * 2 = 20

```python
from z3 import *

# Create a symbolic variable
x = Int('x')

# Create solver
s = Solver()

# Add our equation as a constraint
s.add((x + 5) * 2 == 20)

# Check if solvable and get solution
if s.check() == sat:
    model = s.model()
    print(f"x = {model[x]}")
```

4. Practical CTF Example with z3:
Let's solve a simple password checker:
```python
from z3 import *

# Create symbolic variables for a 4-char password
password = [BitVec(f'pass_{i}', 8) for i in range(4)]

# Create solver
s = Solver()

# Add constraints: Each char must be printable ASCII
for char in password:
    s.add(char >= 0x20)  # space
    s.add(char <= 0x7e)  # ~

# Add password checking constraints
s.add(password[0] + password[1] == 0xA3)  # First two chars add up to 0xA3
s.add(password[2] ^ password[3] == 0x31)  # XOR of last two chars is 0x31
s.add(password[1] * 2 == password[3])     # Third char is double of second

if s.check() == sat:
    model = s.model()
    result = ""
    for char in password:
        result += chr(model[char].as_long())
    print(f"Password found: {result}")
```

5. Simple angr Example:
Let's solve a basic crackme:
```python
import angr
import claripy

def solve_crackme():
    # Load the binary
    proj = angr.Project('./crackme')
    
    # Create symbolic input (8-char password)
    flag_chars = [claripy.BVS(f'flag_{i}', 8) for i in range(8)]
    flag = claripy.Concat(*flag_chars)
    
    # Create initial state
    state = proj.factory.entry_state(args=['./crackme'], stdin=flag)
    
    # Add constraints for printable chars
    for c in flag_chars:
        state.solver.add(c >= 0x20)
        state.solver.add(c <= 0x7e)
    
    # Create simulation manager
    simgr = proj.factory.simulation_manager(state)
    
    # Find path to success (0x400good) and avoid failure (0x400bad)
    simgr.explore(find=0x400good, avoid=0x400bad)
    
    if len(simgr.found) > 0:
        solution_state = simgr.found[0]
        solution = solution_state.solver.eval(flag, cast_to=bytes)
        return solution
    
    return None
```

Key Tips for Beginners:

1. Start Simple:
- Begin with z3 for simple equation solving
- Move to angr when you need to analyze actual binaries

2. Common Patterns:
- Always add constraints for printable characters when dealing with passwords/flags
- Use find/avoid in angr to target specific code paths

3. Debugging:
- Print states and constraints when things don't work
- Use smaller input sizes first when testing

4. Common Constraints for CTF:
```python
# Flag format constraints
state.solver.add(flag.startswith(b'flag{'))
state.solver.add(flag.endswith(b'}'))

# Printable ASCII
for char in flag_chars:
    state.solver.add(char >= 0x20)
    state.solver.add(char <= 0x7e)
```

Would you like me to explain any of these concepts in more detail or provide additional examples?




Let me break these down line by line:

1. `password = [BitVec(f'pass_{i}', 8) for i in range(4)]`
```python
# This creates a list of 4 symbolic variables for a 4-character password
# Breaking it down:
# - BitVec creates a symbolic variable of specific bit width
# - f'pass_{i}' creates names like 'pass_0', 'pass_1', 'pass_2', 'pass_3'
# - 8 means each variable is 8 bits (1 byte, perfect for ASCII characters)

# It's equivalent to:
password = []
password.append(BitVec('pass_0', 8))  # First character
password.append(BitVec('pass_1', 8))  # Second character
password.append(BitVec('pass_2', 8))  # Third character
password.append(BitVec('pass_3', 8))  # Fourth character
```

2. `flag_chars = [claripy.BVS(f'flag_{i}', 8) for i in range(8)]`
```python
# Similar to above, but using angr's claripy instead of z3
# BVS = Bit Vector Symbol
# Creates 8 symbolic variables for an 8-character flag
# Example usage:
flag_chars = []
flag_chars.append(claripy.BVS('flag_0', 8))  # First character
flag_chars.append(claripy.BVS('flag_1', 8))  # Second character
# ... and so on for 8 characters
```

3. `state = proj.factory.entry_state(args=['./crackme'], stdin=flag)`
```python
# This creates an initial program state:
# - args=['./crackme']: simulates running ./crackme from command line
# - stdin=flag: connects our symbolic input to program's stdin
# 
# It's like preparing to run a program:
# $ ./crackme
# And then typing our input when prompted

# Example with more options:
state = proj.factory.entry_state(
    args=['./crackme'],           # Program arguments
    stdin=flag,                   # Standard input
    env={"PATH": "/usr/bin"},     # Environment variables
    add_options={                 # Additional simulation options
        angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
        angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS
    }
)
```

4. `simgr = proj.factory.simulation_manager(state)`
```python
# Creates a simulation manager that will explore different paths
# Think of it as a controller that:
# - Manages different program states
# - Keeps track of which paths are:
#   * active (still exploring)
#   * found (reached target)
#   * avoided (hit bad paths)
#   * deadended (can't continue)

# Example of different stashes:
simgr.active    # States currently being explored
simgr.found     # States that reached our target
simgr.avoided   # States that hit paths we wanted to avoid
simgr.deadended # States that can't continue (program ended)
```

5. Final part:
```python
if len(simgr.found) > 0:  # Did we find any solutions?
    solution_state = simgr.found[0]  # Get first successful state
    # Convert symbolic solution to concrete bytes
    solution = solution_state.solver.eval(flag, cast_to=bytes)
    return solution

# Example with more error handling:
if len(simgr.found) > 0:
    solution_state = simgr.found[0]
    try:
        # Get solution and ensure it's printable
        solution = solution_state.solver.eval(flag, cast_to=bytes)
        if all(32 <= c <= 126 for c in solution):  # Check if printable ASCII
            return solution
        else:
            return None  # Solution contains non-printable characters
    except:
        return None  # Solver couldn't find concrete solution
return None  # No solutions found
```

Practical Example:
```python
import angr
import claripy

def solve_simple_crackme():
    # Load binary
    proj = angr.Project('./crackme')
    
    # Create 4-char symbolic password
    chars = [claripy.BVS(f'char_{i}', 8) for i in range(4)]
    password = claripy.Concat(*chars)  # Combine into one symbolic value
    
    # Create initial state
    state = proj.factory.entry_state(stdin=password)
    
    # Add constraints - only printable ASCII
    for char in chars:
        state.solver.add(char >= ord('!'))
        state.solver.add(char <= ord('~'))
    
    # Create simulation manager
    simgr = proj.factory.simulation_manager(state)
    
    # Find path to success message
    simgr.explore(find=0x400winner, avoid=0x400loser)
    
    if len(simgr.found) > 0:
        solution = simgr.found[0].solver.eval(password, cast_to=bytes)
        print(f"Password found: {solution.decode()}")
        return solution
    
    print("No solution found")
    return None
```

Would you like me to elaborate on any of these concepts further or provide more examples?

























Let me clarify these concepts:

1. BitVec vs Python bytes:
```python
# Python bytes - concrete values
python_byte = b'A'  # This is actually just 0x41
print(python_byte[0])  # prints 65

# BitVec - symbolic values
from z3 import *
symbolic_byte = BitVec('x', 8)  # This is like saying "some unknown byte"
# You can do operations without knowing its actual value:
result = symbolic_byte + 1  # This creates an expression "x + 1"

# Example showing the difference:
concrete = 0x41 + 1  # = 0x42
symbolic = BitVec('x', 8) + 1  # = "x + 1" (expression, not a value)

# BitVec allows us to solve for values:
s = Solver()
s.add(symbolic == 0x42)  # We want "x + 1 = 0x42"
if s.check() == sat:
    print(s.model())  # Will show x = 0x41
```

2. Simulation Manager and explore():
```python
# Yes, simgr.explore() starts the actual path exploration
# Different ways to use explore():

# 1. Using addresses
simgr.explore(
    find=0x400789,    # Address of success message
    avoid=0x400123    # Address of failure message
)

# 2. Using functions
def is_success(state):
    # Check if register/memory contains specific value
    return state.regs.rax == 0x1337

simgr.explore(
    find=is_success,  # Call function to check state
    avoid=lambda state: state.regs.rax == 0
)

# 3. Multiple targets
simgr.explore(
    find=[0x400789, 0x400790],  # Multiple success addresses
    avoid=[0x400123, 0x400456]  # Multiple failure addresses
)
```

3. Multiple Solutions:
```python
# Yes, simgr.found contains all states that reached the target
# Example handling multiple solutions:

def get_all_solutions(simgr, flag):
    solutions = []
    
    # Check all found states
    for found_state in simgr.found:
        try:
            solution = found_state.solver.eval(flag, cast_to=bytes)
            solutions.append(solution)
        except:
            continue
    
    return solutions

# Usage example:
proj = angr.Project('./crackme')
flag = claripy.BVS('flag', 8 * 8)  # 8-char flag
state = proj.factory.entry_state(stdin=flag)
simgr = proj.factory.simulation_manager(state)

# Find all solutions
simgr.explore(find=0x400789, avoid=0x400123)
all_solutions = get_all_solutions(simgr, flag)

for i, sol in enumerate(all_solutions, 1):
    print(f"Solution {i}: {sol}")
```

Real CTF Example:
```python
import angr
import claripy

def solve_multiple_passwords():
    proj = angr.Project('./multi_password')
    
    # Create 4-char password
    chars = [claripy.BVS(f'c{i}', 8) for i in range(4)]
    password = claripy.Concat(*chars)
    
    # Setup initial state
    state = proj.factory.entry_state(stdin=password)
    
    # Add ASCII constraints
    for c in chars:
        state.solver.add(c >= ord('a'))
        state.solver.add(c <= ord('z'))
    
    # Create and explore
    simgr = proj.factory.simulation_manager(state)
    simgr.explore(find=0x400789)  # Success address
    
    # Get all solutions
    solutions = []
    for found in simgr.found:
        try:
            sol = found.solver.eval(password, cast_to=bytes)
            solutions.append(sol.decode())
        except:
            continue
    
    print(f"Found {len(solutions)} solutions:")
    for i, sol in enumerate(solutions, 1):
        print(f"Password {i}: {sol}")

# This might find multiple valid passwords like:
# Password 1: "pass"
# Password 2: "flag"
# Password 3: "key1"
```

The key difference between BitVec/BVS and regular bytes is that symbolic variables represent "unknown values that satisfy certain conditions" rather than specific, concrete values. This is what allows us to solve for values that make a program behave in certain ways!


































Great questions!

1. States and Solutions:
Think of a program's execution like a tree of possibilities:

```python
# Example program:
def check_password(pwd):
    if len(pwd) != 4:         # Branch 1
        return False
    if pwd[0] != 'A':         # Branch 2
        return False
    if pwd[1] + pwd[2] != 'X' # Branch 3
        return False
    return True               # Success!
```

Visual representation of states/paths:
```
                    Start
                      |
          len(pwd) == 4?  (Branch 1)
            /           \
           Yes          No (Failed State)
            |
    pwd[0] == 'A'?  (Branch 2)
        /           \
      Yes           No (Failed State)
       |
pwd[1]+pwd[2]=='X'? (Branch 3)
    /           \
  Yes           No (Failed State)
   |
Success State
```

Each "state" contains:
- Program counter (where we are in code)
- Register values
- Memory contents
- Constraints collected along the path

Example with angr:
```python
import angr
import claripy

# Load binary
proj = angr.Project('./crackme')

# Create symbolic input
flag = claripy.BVS('flag', 32)  # 4 bytes

# Create initial state
state = proj.factory.entry_state(stdin=flag)

# Current state includes:
print(state.regs.rip)    # Program counter
print(state.regs.rax)    # Register values
print(state.memory.load) # Memory contents

simgr = proj.factory.simulation_manager(state)
simgr.explore(find=0x400789)  # Success address

# Each state in simgr.found reached the success point
# with different constraints/values
```

2. About `password` and eval:
The `password` variable is our symbolic input that was fed to stdin. When we eval it, we're asking "what value of this input leads to this successful state?"

Here's a clearer example:
```python
import angr
import claripy

def solve_crackme():
    proj = angr.Project('./crackme')
    
    # Create symbolic input
    password = claripy.BVS('pass', 32)  # 4 bytes
    
    # Feed it to program's stdin
    state = proj.factory.entry_state(stdin=password)
    
    # Explore paths
    simgr = proj.factory.simulation_manager(state)
    simgr.explore(find=0x400789)
    
    if len(simgr.found) > 0:
        found_state = simgr.found[0]
        
        # This converts symbolic password to concrete value
        # that satisfies all constraints in this state
        solution = found_state.solver.eval(password, cast_to=bytes)
        
        # We use 'password' because that's our symbolic variable
        # If we had multiple inputs, we'd eval each separately:
        # username = found_state.solver.eval(user_sym)
        # password = found_state.solver.eval(pass_sym)
        
        return solution

    return None
```

More detailed example showing states and constraints:
```python
import angr
import claripy

def detailed_solve():
    proj = angr.Project('./crackme')
    
    # Create symbolic input
    password = claripy.BVS('pass', 32)
    
    # Create initial state
    state = proj.factory.entry_state(stdin=password)
    
    # Add some basic constraints
    state.solver.add(password > 0x20202020)  # All chars > space
    
    simgr = proj.factory.simulation_manager(state)
    
    # Explore step by step
    while len(simgr.active) > 0:
        # Step one instruction
        simgr.step()
        
        # Print current states
        for active in simgr.active:
            print(f"At address: {active.regs.rip}")
            print("Constraints:")
            for constraint in active.solver.constraints:
                print(f"  {constraint}")
            
        # Check if we reached target
        if len(simgr.found) > 0:
            solution = simgr.found[0].solver.eval(password, cast_to=bytes)
            print(f"Found solution: {solution}")
            return solution
            
    return None
```

So when we do `solver.eval(password)`, we're saying:
- "Give me a concrete value for our symbolic input (password)"
- "That satisfies all constraints collected in this successful path"
- "And convert it to bytes so we can read it"

The stdin connection is just how we fed this symbolic value to the program - we still need to reference our original symbolic variable to get its solution!





`proj = angr.Project('./crackme')` initalizes the project 


`password = claripy.BVS('pass', 32)` create a BitVec symbol, to be added with contraints and look for the suitable input value of this that leads to flag

`state.solver.add(password > 0x20202020)` just some contraints, like `x < 10` and here we are finding x by exploring the program with angr 

`state = proj.factory.entry_state(stdin=password)` the initial state is generated

`simgr = proj.factory.simulation_manager(state)` creates a simulation of the program and going to start exploring to find input aka `password` that leads to things we want 

`simgr.explore(find=0x400789)` specifying the address the things we want find / reach  

`solution = found_state.solver.eval(password, cast_to=bytes)` casting the right solution, the correct input of `password` to be able to get to reach to where we wanna go 