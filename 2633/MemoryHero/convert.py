import re

def convert_objdump_to_simple_asm(objdump_file, output_file):
    with open(objdump_file, 'r') as f_in, open(output_file, 'w') as f_out:
        current_node = None
        
        for line in f_in:
            # Match node definition
            if match := re.match(r'\s*([0-9a-f]+)\s+<(node\d+)>:', line):
                addr, node_name = match.groups()
                f_out.write(f"{addr} <{node_name}>:\n")
                continue
            
            # Skip non-instruction lines
            if not re.match(r'\s*[0-9a-f]+:\s+', line):
                continue
                
            # Clean up instruction lines
            # Remove the address and hex bytes, keep only the instruction
            if match := re.search(r'[0-9a-f]+:\s+(?:[0-9a-f]{2}\s+)+\s*(.*?)$', line):
                instruction = match.group(1).strip()
                if instruction:  # Skip empty lines
                    f_out.write(f"    {instruction}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python convert.py <objdump_file> <output_file>")
        sys.exit(1)
        
    convert_objdump_to_simple_asm(sys.argv[1], sys.argv[2])