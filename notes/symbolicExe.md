```markdown
---
aliases:
  - Symbolic Execution in CTF
tags:
  - flashcard/active/ctf/A
---
# Symbolic Execution in CTF

Symbolic execution is a technique where {{variables are treated as symbols/expressions rather than concrete values}}, used to {{find inputs that lead to specific program states}}.

## Angr

### Project Setup
```python
proj = angr.Project('./crackme')
```
This {{initializes angr to analyze the binary}}

### Symbolic Variable
```python
password = claripy.BVS('pass', 32) 
```
- This {{creates a symbolic variable (like an algebraic unknown)}} that we'll solve for later.
- `pass` is the {{variable name}}, 32 is the {{size, it means 32 bits, i.e. 4 bytes, which is likely an integer}}
- `BVS` stands for {{"Bit Vector Symbolic"}} - it's a function in claripy (a constraint solver used with angr, like z3) to {{create symbolic variables}}.
- claripy is built on top of Z3 and provides a more convenient interface specifically designed to work with angr
### Initial State
```python
state = proj.factory.entry_state(stdin=password)
```
This {{creates starting program state}} and {{connects our symbolic input to program's stdin}}

### Simulation Manager
```python
simgr = proj.factory.simulation_manager(state)
```
This {{creates a simulation controller}} that will {{explore different execution paths}}

### Path Exploration
```python
simgr.explore(find=0x400789)
```
This {{starts exploring program paths}} to {{find ones reaching our target address}}

### Solution Extraction
```python
solution = found_state.solver.eval(password, cast_to=bytes)
```
This {{converts symbolic solution to actual bytes}} that {{satisfy all constraints to reach our target}}

## Additional Notes
- Constraints can be added like {{state.solver.add(password > 0x20202020)}}
- The simulation manager tracks different paths in {{active, found, avoided, and deadended states}}
```