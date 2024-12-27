import z3, re
from pwn import *

def collect_data(num_samples=50):
    values = {}
    while len(values) < num_samples:
        try:
            r = remote('chal.firebird.sh', 35055, level='error')
            output = r.recvuntil(b"encouragement!").decode("utf-8").split("\n")
            
            # Extract stamina
            stamina = int(re.search("[0-9][0-9][0-9]%", output[0]).group(0)[:-1])
            if stamina in values:
                r.close()
                continue
                
            # Extract recipe steps
            steps = []
            for line in output:
                if "Add" in line or "Knead" in line:
                    num = int(re.search(r'\d+', line.split(":")[1]).group())
                    steps.append(num)
            
            values[stamina] = steps
            r.close()
            print(f"Collected stamina {stamina}, total samples: {len(values)}")
            
        except Exception as e:
            print(f"Error: {e}")
            continue
            
    return values

def solve_neuron_data(values):
    solver = z3.Solver()
    neuron_data = [z3.Int(f'n{i}') for i in range(228)]
    
    # Add constraints for each stamina value
    for stamina, steps in values.items():
        start_idx = stamina - 100
        for i in range(128):
            # steps[i] = neuron_data[start_idx + i] + neuron_data[start_idx + i + 1] + stamina
            solver.add(steps[i] == neuron_data[start_idx + i] + neuron_data[start_idx + i + 1] + stamina)
    
    # Add constraint that values should be ASCII
    for n in neuron_data:
        solver.add(n >= 0)
        solver.add(n <= 255)
    
    if solver.check() == z3.sat:
        model = solver.model()
        result = [model[n].as_long() for n in neuron_data]
        return result
    return None

def reverse_xor(neuron_data):
    message = [''] * len(neuron_data)
    # Last character is unchanged
    message[-1] = chr(neuron_data[-1])
    
    # Work backwards to reverse XOR operations
    for i in range(len(neuron_data)-2, -1, -1):
        message[i] = chr(neuron_data[i] ^ ord(message[i+1]))
    
    return ''.join(message)

# Main solving process
values = collect_data(50)  # Collect 50 samples
neuron_data = solve_neuron_data(values)
if neuron_data:
    message = reverse_xor(neuron_data)
    print("Found message:", message)
    
    # Test the message
    r = remote('chal.firebird.sh', 35055, level='error')
    r.recvuntil(b"encouragement!")
    r.sendline(message.encode())
    print(r.recvall().decode())
    r.close()

