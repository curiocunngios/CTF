def process_memory_to_passcodes(memory):
    result = [''] * 80  # Make it large enough
    a = 0
    b = 31
    c = 0
    
    # Process pairs from index 21 to 84
    for j in range(21, 85, 2):
        if (c & 3 == 0) or (c % 4 == 3):
            result[a + 48] = chr(memory[j])
            result[b] = chr(memory[j + 1])
        else:
            result[b] = chr(memory[j])
            result[a + 48] = chr(memory[j + 1])
        a += 1
        b -= 1
        c += 1
    
    # Split into two passcodes
    passcode1 = ''.join(result[48:])  # From index 48 onwards
    passcode2 = ''.join(result[:32])  # Up to index 31
    
    return passcode1, passcode2

def interpret_chinese_bf(code):
    memory = [0] * 100
    ptr = 0
    i = 0
    
    while i < len(code):
        char = code[i]
        
        if char == '⼭':
            ptr = (ptr + 101) % 100
        elif char == '牛':
            ptr = (ptr + 99) % 100
        elif char == '竹':
            memory[ptr] = (memory[ptr] + 1) & 0xFF
        elif char == '⽜':
            memory[ptr] = (memory[ptr] - 1) & 0xFF
        elif char == '山':
            memory[ptr] = ord('A')  # Simulate input for testing
        elif char == '⽵':
            if memory[ptr] == 0:
                bracket_count = 1
                while bracket_count > 0:
                    i += 1
                    if code[i] == '⽵':
                        bracket_count += 1
                    elif code[i] == '肉':
                        bracket_count -= 1
        elif char == '肉':
            if memory[ptr] != 0:
                bracket_count = 1
                while bracket_count > 0:
                    i -= 1
                    if code[i] == '⽵':
                        bracket_count -= 1
                    elif code[i] == '肉':
                        bracket_count += 1
                i -= 1
        i += 1
    
    return process_memory_to_passcodes(memory)

# Read and process code.txt
with open('code.txt', 'r', encoding='utf-8') as f:
    code = f.read()
    passcode1, passcode2 = interpret_chinese_bf(code)
    print("Passcode 1:", repr(passcode1))
    print("Passcode 2:", repr(passcode2))