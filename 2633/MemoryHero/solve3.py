# simple_flag_finder.py
import re

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
            line = line.strip()
            
            # Match node definition
            if match := re.match(r'[0-9a-f]+ <(node\d+)>:', line):
                node_name = match.group(1)
                current_node = Node(node_name)
                nodes[node_name] = current_node
                continue
            
            if not current_node:
                continue
            
            # Match byte writing
            if match := re.search(r'mov\s+BYTE PTR\s+\[.*\],\s*0x([0-9a-f]+)', line):
                current_node.writes_byte = int(match.group(1), 16)
            
            # Match comparisons
            if match := re.search(r'cmp\s+rax,\s*0x([0-9a-f]+)', line):
                current_node.cmp_values.append(int(match.group(1), 16))
            
            # Match jumps
            if 'je' in line:
                if match := re.search(r'je\s+[0-9a-f]+\s+<(node\d+)', line):
                    current_node.jumps_to.append(match.group(1))
    
    return nodes

def find_flags(nodes, start="node0"):
    FLAG_START = [0x66, 0x6c, 0x61, 0x67, 0x7b]  # "flag{"
    visited = set()
    
    def explore(node_name, buffer, path):
        if node_name in visited:
            return
        
        visited.add(node_name)
        node = nodes[node_name]
        path.append(node_name)
        
        if node.writes_byte is not None:
            buffer.append(node.writes_byte)
            
            # Check if we're building a valid flag
            if len(buffer) <= len(FLAG_START):
                if buffer != FLAG_START[:len(buffer)]:
                    visited.remove(node_name)
                    return
            
            # Check for complete flag
            if buffer[-1] == 0x7d and len(buffer) >= 6:
                if buffer[:5] == FLAG_START:
                    flag = ''.join(chr(x) for x in buffer)
                    print(f"\nFound potential flag: {flag}")
                    print(f"Path: {' -> '.join(path)}")
                    print(f"Required inputs: {[hex(x) for x in nodes[path[0]].cmp_values]}")
        
        # Explore next nodes
        for next_node in node.jumps_to:
            explore(next_node, buffer[:], path[:])
        
        visited.remove(node_name)

    explore(start, [], [])

def main(filename):
    nodes = parse_assembly(filename)
    find_flags(nodes)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <assembly_file>")
        sys.exit(1)
    main(sys.argv[1])