def decode_instructions(content):
    value = 0
    memory = [0] * 100  # Program seems to use an array
    pointer = 0
    
    for char in content:
        if char == '⼭':
            pointer += 1
        elif char == '竹':
            memory[pointer] += 1
        elif char == '牛':
            memory[pointer] *= 2
        elif char == '肉':
            pointer = 0  # Reset pointer
            
    # Convert memory values to ASCII
    result = ''
    for val in memory:
        if 32 <= val <= 126:  # Printable ASCII range
            result += chr(val)
            
    return result

def main():
    with open('code.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        
    sections = content.split('⽜肉')
    print("Number of sections:", len(sections))
    
    # Process each section separately
    for i, section in enumerate(sections):
        if section:
            print(f"\nSection {i} result:")
            print(decode_instructions(section))

if __name__ == "__main__":
    main()