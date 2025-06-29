from pwn import *
import re
import z3

def get_one_sample():
    # = remote('chal.firebird.sh', 35055)
    p = process(['python3', 'program'])
    data = p.recvuntil(b"encouragement!").decode()
    p.close()
    
    stamina = int(re.search(r"(\d+)%", data).group(1))
    recipe_steps = []
    
    for line in data.split('\n'):
        if 'Add' in line:
            number = re.search(r'Add (\d+)', line)

            recipe_steps.append(int(number.group(1)))
        elif 'Knead' in line:
            number = re.search(r'Knead.*?(\d+)', line)

            recipe_steps.append(int(number.group(1)))
    
    return stamina, recipe_steps


def find_message(samples):

    solver = z3.Solver()
    neuron_data = [z3.Int(f'c{i}') for i in range(228)]
    
    # char must be valid ASCII
    for c in neuron_data:
        solver.add(c >= 0)
        solver.add(c <= 255)
    
    # Add constraints from each sample
    
    for stamina, recipe in samples.items():
        for idx, (i, j) in zip(range(len(recipe)),
                            zip(neuron_data[stamina-100:stamina-100+len(recipe)], # here it is not 228 but len(recipe) is because we are starting from recipe 
                                neuron_data[stamina-99:stamina-99+len(recipe)])):
            solver.add(recipe[idx] == i + j + stamina)
    
    if solver.check() == z3.sat:
        model = solver.model()
        return [model[c].as_long() for c in neuron_data]
    return None

# XOR
def decode_message(encoded):

    message = [''] * len(encoded)
    message[-1] = chr(encoded[-1])
    
    for i in range(len(encoded)-2, -1, -1):
        message[i] = chr(encoded[i] ^ ord(message[i+1]))
    
    return ''.join(message)


    # 1. Collect samples
samples = {}  # stamina -> recipe_steps

for i in range(101):
    stamina, steps = get_one_sample()
    if stamina not in samples:
        samples[stamina] = steps

encoded = find_message(samples)


message = decode_message(encoded)
print(message)
    


