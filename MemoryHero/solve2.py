import re
from pwn import *

class Node:
    def __init__(self, name):
        self.name = name
        self.writes_byte = None
        self.jumps_to = []
        self.cmp_values = []

def parse_assembly(filename):
    nodes = {}
    current_node = None
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip() # remove trialing whitespaces 
            
            # Match node definition
            node_match = re.match(r'[0-9a-f]+ <(node\d+)>:', line)
            if node_match:
                node_name = node_match.group(1)
                current_node = Node(node_name)
                nodes[node_name] = current_node
                continue
                
            if not current_node:
                continue
                
            # Match byte writing
            write_match = re.search(r'mov\s+BYTE PTR\s+\[.*\],\s*0x([0-9a-f]+)', line)
            if write_match:
                current_node.writes_byte = int(write_match.group(1), 16)
                
            # Match comparisons
            cmp_match = re.search(r'cmp\s+rax,\s*0x([0-9a-f]+)', line)
            if cmp_match:
                current_node.cmp_values.append(int(cmp_match.group(1), 16))
                
            # Match jumps
            jump_match = re.search(r'je\s+([0-9a-f]+)\s+<(node\d+)', line)
            if jump_match:
                current_node.jumps_to.append(jump_match.group(2))
    
    return nodes

def find_flag_paths(nodes, start="node0", max_depth=100):
    FLAG_START = b"flag{"
    visited = []
    
    def is_valid_char(c):
        return (ord('0') <= c <= ord('9') or
                ord('A') <= c <= ord('Z') or
                ord('a') <= c <= ord('z') or
                c in b"_-{}")
    
    def explore(node_name, buffer, path, depth=0):
        if depth > max_depth or node_name in visited:
            return
        
        # Add to visited list
        visited.append(node_name)
        
        node = nodes[node_name]
        path.append(node_name)
        
        # Add byte if node writes one
        if node.writes_byte is not None:
            buffer += bytes([node.writes_byte])
            
            # Check if we have a valid flag start
            if len(buffer) >= len(FLAG_START):
                if buffer.startswith(FLAG_START):
                    # Valid flag found
                    if buffer.endswith(b"}"):
                        print(f"\nPotential flag: {buffer.decode()}")
                        print(f"Path: {' -> '.join(path)}")
                        print(f"Input values needed: {[hex(x) for x in nodes[path[0]].cmp_values]}")
                    
                    # Check for valid characters
                    elif not all(is_valid_char(c) for c in buffer):
                        visited.remove(node_name)
                        return
        
        # Explore next nodes
        for next_node in node.jumps_to:
            explore(next_node, buffer, path[:], depth + 1)
        
        # Remove from visited when backtracking
        visited.remove(node_name)
    
    explore(start, b"", [])

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <assembly_file>")
        return
        
    log.info("Parsing assembly file...")
    nodes = parse_assembly(sys.argv[1])
    
    log.info("Searching for flag paths...")
    find_flag_paths(nodes)

if __name__ == "__main__":
    main()