import re
from dataclasses import dataclass
from typing import List, Dict, Set
import sys

@dataclass
class Node:
    # what is this syntax: `name : str`. 
    # I have never seen something like this in python `
    name: str
    writes_byte: int = None     
    jumps_to: List[str] = None  
    address: int = None         
    cmp_values: List[int] = None

    def __post_init__(self):
        if self.jumps_to is None:
            self.jumps_to = []
        if self.cmp_values is None:
            self.cmp_values = []

def is_valid_char(c: int) -> bool:
    return ((c >= 0x30 and c <= 0x39) or  
            (c >= 0x41 and c <= 0x5a) or  
            (c >= 0x61 and c <= 0x7a) or  
            c in {0x5f, 0x2d, 0x7b, 0x7d})

def find_paths_to_close_brace(nodes: Dict[str, Node], start_node: str = "node0") -> List[List[str]]:
    valid_paths = []
    FLAG_START = [0x66, 0x6c, 0x61, 0x67, 0x7b]  # "flag{"
    visited = set()
    
    def is_valid_flag_structure(buffer: List[int]) -> bool:
        open_braces = buffer.count(0x7b)
        close_braces = buffer.count(0x7d)
        if open_braces > 1 or close_braces > 1:
            return False
        if 0x7d in buffer and buffer[-1] != 0x7d:
            return False
        return True
    
    def dfs(node_name: str, buffer: List[int], path: List[str], depth: int = 0):
        if depth > 100 or node_name in visited:
            return
            
        visited.add(node_name)
        
        if len(buffer) <= len(FLAG_START):
            if len(buffer) > 0 and buffer != FLAG_START[:len(buffer)]:
                visited.remove(node_name)
                return
        else:
            if not is_valid_flag_structure(buffer) or not is_valid_char(buffer[-1]):
                visited.remove(node_name)
                return
        
        node = nodes[node_name]
        path.append(node_name)
        
        if node.writes_byte is not None:
            buffer.append(node.writes_byte)
        
        if buffer and buffer[-1] == 0x7d:
            if len(buffer) >= 6 and buffer[:5] == FLAG_START and is_valid_flag_structure(buffer):
                flag = ''.join(chr(x) for x in buffer)
                print(f"\nPotential flag: {flag}")
                print(f"Path: {' -> '.join(path)}")
                print(f"Required inputs: {[hex(x) for x in nodes[path[0]].cmp_values]}")
                valid_paths.append(path[:])
        
        for next_node in node.jumps_to:
            if next_node in nodes:
                dfs(next_node, buffer[:], path[:], depth + 1)
        
        visited.remove(node_name)
    
    dfs(start_node, [], [], 0)
    return valid_paths

def parse_assembly(filename: str) -> Dict[str, Node]:
    nodes = {}
    current_node = None
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            
            if match := re.match(r'[0-9a-f]+ <(node\d+)>:', line):
                node_name = match.group(1)
                current_node = Node(name=node_name)
                nodes[node_name] = current_node
                current_node.address = int(line.split()[0], 16)
                
            if not current_node:
                continue
                
            if match := re.search(r'mov\s+BYTE PTR\s+\[.*\],\s*0x([0-9a-f]+)', line):
                value = int(match.group(1), 16)
                current_node.writes_byte = value
                
            if match := re.search(r'cmp\s+rax,\s*0x([0-9a-f]+)', line):
                value = int(match.group(1), 16)
                current_node.cmp_values.append(value)
                
            if 'je' in line:
                if match := re.search(r'je\s+([0-9a-f]+)\s+<(node\d+|fail_code)>', line):
                    target = match.group(2)
                    if target != 'fail_code':
                        current_node.jumps_to.append(target)
                
    return nodes

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <assembly_file>")
        sys.exit(1)
        
    nodes = parse_assembly(sys.argv[1])
    find_paths_to_close_brace(nodes)

if __name__ == "__main__":
    main()