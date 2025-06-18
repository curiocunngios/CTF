# Memory Hero 
Author: "quote"  
Reverse  
Description  
Solves 6  

Fai is trying to tell you a flag, but he got drunk! Can you recover the flag from his brain?  

Note: The challenge has much fewer instructions not taught in lectures, as actual assembly is used to produce the executables. It is difficult in a way different from the last homework...  

[fai](./program)  
fai.exe  
[fai_check.py](./fai_check.py)

## Solution
First, in terminal of kali linux, run command `objdump -d program  -M intel > assembly`
Second, convert the objdump to simpler assembly.s file with `convert.py` and output the file:  
`Usage: python convert.py <objdump_file> <output_file>"`  
Third, run `solve.py` on the assembly file and output it:    
`Usage: python solve.py <assembly> <output_file>"`  
Forth, final output file contains a bunch of possible flags. With staring and some `ctrl`+`f`, look for the readable strings in the final output file to find words that make sense.
### `convert.py`
```py
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
```
### `solve.py` 
```py
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
```

## Observations


the assembly dump from objdump contains so many different functions named `node0`, `node1`, `node2`, etc.   
Inside each node. They seem to be waiting for inputs and comparing them. Depending on the inputs, we jump to different other nodes. But eventually it always has `<fail_node>` function call at the end which leads to exiting the program 
```as
0000000000001130 <main>:
1130:	55                   	push   rbp
1131:	48 89 e5             	mov    rbp,rsp
1134:	48 83 ec 10          	sub    rsp,0x10
1138:	48 8d 3d da 9e 00 00 	lea    rdi,[rip+0x9eda]        # b019 <intro>
113f:	31 c0                	xor    eax,eax
1141:	ff 15 79 9e 00 00    	call   QWORD PTR [rip+0x9e79]        # afc0 <printf@GLIBC_2.2.5>
1147:	48 31 db             	xor    rbx,rbx

000000000000114a <node0>:
114a:	48 8d 05 7f 9f 00 00 	lea    rax,[rip+0x9f7f]        # b0d0 <__TMC_END__>
1151:	c6 04 18 66          	mov    BYTE PTR [rax+rbx*1],0x66
1155:	48 ff c3             	inc    rbx
1158:	48 8d 3d b1 9e 00 00 	lea    rdi,[rip+0x9eb1]        # b010 <scanf_format>
115f:	48 89 e6             	mov    rsi,rsp
1162:	31 c0                	xor    eax,eax
1164:	ff 15 66 9e 00 00    	call   QWORD PTR [rip+0x9e66]        # afd0 <scanf@GLIBC_2.2.5>
116a:	48 8b 04 24          	mov    rax,QWORD PTR [rsp]
116e:	48 3d 85 00 00 00    	cmp    rax,0x85
1174:	0f 84 2d 22 00 00    	je     33a7 <node133>
117a:	48 83 f8 3c          	cmp    rax,0x3c
117e:	0f 84 08 10 00 00    	je     218c <node60>
1184:	48 3d dc 00 00 00    	cmp    rax,0xdc
118a:	0f 84 a2 3c 00 00    	je     4e32 <node220>
1190:	e9 b8 7c 00 00       	jmp    8e4d <fail_code>

00000000000033a7 <node133>:
33a7:	48 8d 05 22 7d 00 00 	lea    rax,[rip+0x7d22]        # b0d0 <__TMC_END__>
33ae:	c6 04 18 7b          	mov    BYTE PTR [rax+rbx*1],0x7b
33b2:	48 ff c3             	inc    rbx
33b5:	48 8d 3d 54 7c 00 00 	lea    rdi,[rip+0x7c54]        # b010 <scanf_format>
33bc:	48 89 e6             	mov    rsi,rsp
33bf:	31 c0                	xor    eax,eax
33c1:	ff 15 09 7c 00 00    	call   QWORD PTR [rip+0x7c09]        # afd0 <scanf@GLIBC_2.2.5>
33c7:	48 8b 04 24          	mov    rax,QWORD PTR [rsp]
33cb:	48 3d b8 00 00 00    	cmp    rax,0xb8
33d1:	0f 84 17 0f 00 00    	je     42ee <node184>
33d7:	48 3d e2 00 00 00    	cmp    rax,0xe2
33dd:	0f 84 dd 1b 00 00    	je     4fc0 <node226>
33e3:	48 3d 92 00 00 00    	cmp    rax,0x92
33e9:	0f 84 2f 04 00 00    	je     381e <node146>
33ef:	48 3d 8c 01 00 00    	cmp    rax,0x18c
33f5:	0f 84 fb 4b 00 00    	je     7ff6 <node396>
33fb:	48 3d 60 01 00 00    	cmp    rax,0x160
3401:	0f 84 89 3f 00 00    	je     7390 <node352>
3407:	48 3d 82 01 00 00    	cmp    rax,0x182
340d:	0f 84 e7 48 00 00    	je     7cfa <node386>
3413:	48 3d b8 01 00 00    	cmp    rax,0x1b8
3419:	0f 84 23 56 00 00    	je     8a42 <node440>
341f:	48 83 f8 47          	cmp    rax,0x47
3423:	0f 84 06 f0 ff ff    	je     242f <node71>
3429:	48 3d a3 01 00 00    	cmp    rax,0x1a3
342f:	0f 84 e6 51 00 00    	je     861b <node419>
3435:	e9 13 5a 00 00       	jmp    8e4d <fail_code>

000000000000218c <node60>:
218c:	48 8d 05 3d 8f 00 00 	lea    rax,[rip+0x8f3d]        # b0d0 <__TMC_END__>
2193:	c6 04 18 79          	mov    BYTE PTR [rax+rbx*1],0x79
2197:	48 ff c3             	inc    rbx
219a:	48 8d 3d 6f 8e 00 00 	lea    rdi,[rip+0x8e6f]        # b010 <scanf_format>
21a1:	48 89 e6             	mov    rsi,rsp
21a4:	31 c0                	xor    eax,eax
21a6:	ff 15 24 8e 00 00    	call   QWORD PTR [rip+0x8e24]        # afd0 <scanf@GLIBC_2.2.5>
21ac:	48 8b 04 24          	mov    rax,QWORD PTR [rsp]
21b0:	48 3d 24 01 00 00    	cmp    rax,0x124
21b6:	0f 84 48 42 00 00    	je     6404 <node292>
21bc:	48 83 f8 33          	cmp    rax,0x33
21c0:	0f 84 3d fd ff ff    	je     1f03 <node51>
21c6:	48 3d 9d 01 00 00    	cmp    rax,0x19d
21cc:	0f 84 b3 62 00 00    	je     8485 <node413>
21d2:	48 83 f8 27          	cmp    rax,0x27
21d6:	0f 84 bf fa ff ff    	je     1c9b <node39>
21dc:	e9 6c 6c 00 00       	jmp    8e4d <fail_code>

0000000000008e4d <fail_code>:
8e4d:	48 8d 3d 23 22 00 00 	lea    rdi,[rip+0x2223]        # b077 <fail>
8e54:	31 c0                	xor    eax,eax
8e56:	ff 15 64 21 00 00    	call   QWORD PTR [rip+0x2164]        # afc0 <printf@GLIBC_2.2.5>
```


I found this interesting function:  
`<maybe_success_code>`
```
0000000000008e26 <maybe_success_code>:
8e26:	48 8d 3d 58 22 00 00 	lea    rdi,[rip+0x2258]        # b085 <maybe_success>
8e2d:	31 c0                	xor    eax,eax
8e2f:	ff 15 8b 21 00 00    	call   QWORD PTR [rip+0x218b]        # afc0 <printf@GLIBC_2.2.5>
8e35:	48 8d 3d d9 21 00 00 	lea    rdi,[rip+0x21d9]        # b015 <output_format>
8e3c:	48 8d 35 8d 22 00 00 	lea    rsi,[rip+0x228d]        # b0d0 <__TMC_END__>
8e43:	31 c0                	xor    eax,eax
8e45:	ff 15 75 21 00 00    	call   QWORD PTR [rip+0x2175]        # afc0 <printf@GLIBC_2.2.5>
8e4b:	eb 0f                	jmp    8e5c <end_code>
```
And from the stuff I found in hexdump:
```
b010 256c6c64 0025730a 00466169 20697320  %lld.%s..Fai is 
b020 74727969 6e672074 6f207465 6c6c2079  trying to tell y
b030 6f752061 20666c61 672c2062 75742068  ou a flag, but h
b040 6520676f 74206472 756e6b21 2043616e  e got drunk! Can
b050 20796f75 20726563 6f766572 20746865   you recover the
b060 20666c61 67206672 6f6d2068 69732062   flag from his b
b070 7261696e 3f0a002a 626c6163 6b73206f  rain?..*blacks o
b080 75742a0a 00466169 20737564 64656e6c  ut*..Fai suddenl
b090 79207265 6d656d62 65727320 74686520  y remembers the 
b0a0 666c6167 2120486f 70656675 6c6c7920  flag! Hopefully 
b0b0 68652064 6f657320 6e6f7420 6d697372  he does not misr
b0c0 656d656d 6265722e 2e2e0a00           emember.....   
```
However, using `ctrl` + `f`, there is no other results of the string `maybe_success_code`
so there's perhaps no way to jump to that function? No, with the correct sequence of transverse in nodes, it will somehow go there. But I knew it when I got the flag, kinda useless information.

### Assembly in depth
By looking intot he assembly in depth. ~~Or just ask gpt~~
```as
000000000000114a <node0>:
        114a:	48 8d 05 7f 9f 00 00 	lea    rax,[rip+0x9f7f]        # b0d0 <__TMC_END__>
        1151:	c6 04 18 66          	mov    BYTE PTR [rax+rbx*1],0x66
        1155:	48 ff c3             	inc    rbx
        1158:	48 8d 3d b1 9e 00 00 	lea    rdi,[rip+0x9eb1]        # b010 <scanf_format>
        115f:	48 89 e6             	mov    rsi,rsp
        1162:	31 c0                	xor    eax,eax
        1164:	ff 15 66 9e 00 00    	call   QWORD PTR [rip+0x9e66]        # afd0 <scanf@GLIBC_2.2.5>
        116a:	48 8b 04 24          	mov    rax,QWORD PTR [rsp]
        116e:	48 3d 85 00 00 00    	cmp    rax,0x85
        1174:	0f 84 2d 22 00 00    	je     33a7 <node133>
        117a:	48 83 f8 3c          	cmp    rax,0x3c
        117e:	0f 84 08 10 00 00    	je     218c <node60>
        1184:	48 3d dc 00 00 00    	cmp    rax,0xdc
        118a:	0f 84 a2 3c 00 00    	je     4e32 <node220>
        1190:	e9 b8 7c 00 00       	jmp    8e4d <fail_code>
```
> `lea    rax,[rip+0x9f7f]`    
> 
- points to seemingly where the flag would be written, which `rip+0x9f7f` is the base address of the array. `0x66` is just `f` what can be more obvious than that. (~~I didn't know at that time~~)    

> `mov    BYTE PTR [rax+rbx*1],0x66`  
> 
- accesses the array by one byte and write `0x66` i.e. `f` into it  
> `mov rsi rsp`
- `rsp` points to top of the stack, in other words, it stores the address of the top of the stack 
- this gets copied to `rsi` which would be passed in as 2nd argument when scanf function is called 
```as
mov    rax,QWORD PTR [rsp]
116e:	48 3d 85 00 00 00    	cmp    rax,0x85
```
- then we compare the value in `rsp` with `0x85`, which would determine which nodes we go in. And the hex number is exactly the number of the node we will go inside. For example, `0x85` is `133` in decimal, which means if we enter that, or just `133`, we go to `node133`  
> inc rbx  
> 
- this is is the index counter of the array i.e. `rbx*1` which persists in different nodes. It helps writing character to the array one by one
#### Memory layout:
```nasm
[rax]     -> First character
[rax+1]   -> Second character
[rax+2]   -> Third character
...

Stack:
[rsp]     -> Where input number is stored
```
#### More 
After exploring for a while , I realized that the challenge is not as easy as I thought  
I thought it was a simple assembly reading and there is just one path for us we follow, we read the characters written and would get us the flag   
But in fact, there are already 3 different paths in the first node  
```as
116e:	48 3d 85 00 00 00    	cmp    rax,0x85
1174:	0f 84 2d 22 00 00    	je     33a7 <node133>
117a:	48 83 f8 3c          	cmp    rax,0x3c
117e:	0f 84 08 10 00 00    	je     218c <node60>
1184:	48 3d dc 00 00 00    	cmp    rax,0xdc
118a:	0f 84 a2 3c 00 00    	je     4e32 <node220>
```
One more thing is that:
- that are some nodes. For example, 
```as
000000000000232f <node67>:
    232f:	48 8d 05 9a 8d 00 00 	lea    rax,[rip+0x8d9a]        # b0d0 <__TMC_END__>
    2336:	c6 04 18 4d          	mov    BYTE PTR [rax+rbx*1],0x4d
    233a:	48 ff c3             	inc    rbx
    233d:	e9 0b 6b 00 00       	jmp    8e4d <fail_code>
```
that writes a value and go straight to `<fail_code>`  
And turned out that these nodes are everywhere, all paths eventually leads to `fail_code`. Then I start thinking that they might be some typical "ending nodes" in the game that just write a character and ends everything. Then if we previously followed a correct path, we kind of end the game differently (going to `maybe_success_...`). 
But since I am not that familiar with binaries, I was thinking that there's a possibility that we are supposed to get into fail code and somehow go back, or right before going into fail code, there could be a mechanism to go to the success code.   
## Attack
In my sea of thoughts, one thing I am probably have guessed right is that the **last or second last node has to be writing the value `}`**  
Because flag is likely to be ending with `'}'`. Then, I tried out something manually:  
1. I have been doing `ctrl`+`f` in the entire assembly source code to go down the branches from node0 simply to all the other nodes.
2. whenever I end up with some nodes that entirely ends with `fail_code` while not writing `'}' `, I delete the node. Because they are probably incorrect ending nodes
3. whenever a node is deleted, it means that the node is certainly incorrect, then I delete all the others node's instruction that jumps into that specific deleted node. Just like deleting a wrong branch
4. When I keep doing this, there would be some nodes that has which branches are all wrong i.e. all gets deleted and becomes empty and go straight to fail_code, also delete them.
5. jump back to the previous node after deleting everything related to that nodek, which is the node itself and the branches that leads to it.
6. do not delete:  
- nodes that writes `0x7d` i.e. '}' to the array and go straight to `fail_code` while not jumping to any nodes ending with 
For example:
```
node370
node415
node454
node46 
```
1. repeat

Then, I started wondering whether the process can be written into a python script and be automated, since I gave up very doing it manually very quickly as there are too many nodes to check and delete.    
Well, then I copied my thought process above and asked chatgpt whether I can automate it, I got some scripts, ran and got a bunch of potential flags. With some staring contest with the file and some `ctrl` + `f` again, I found the flag! 

```
Potential flag: flag{6r4ph_pr0bl3m5_4r3_fun_1n_4553mbly}
Path: node0 -> node220 -> node76 -> node414 -> node110 -> node86 -> node113 -> node75 -> node260 -> node175 -> node20 -> node57 -> node265 -> node68 -> node330 -> node223 -> node203 -> node382 -> node207 -> node3 -> node317 -> node208 -> node441 -> node150 -> node379 -> node381 -> node399 -> node401 -> node49 -> node121 -> node245 -> node277 -> node397 -> node398 -> node211 -> node387 -> node323 -> node362 -> node420 -> node454
Input values needed: ['0x85', '0x3c', '0xdc']
```

### Script 
Welp, at least I know I am doing and I have learnt everything from the chatgpt script, let's break it down!   
The script is basically:  
1. parsing the assembly file 
2. searching  

### Each functions in details:
#### Parsing assembly 
the follwoing part of the code parses the assembly:
```py
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
```
Remember that a typical node look like the following?
```as
000000000000114a <node0>:
114a:	48 8d 05 7f 9f 00 00 	lea    rax,[rip+0x9f7f]        # b0d0 <__TMC_END__>
1151:	c6 04 18 66          	mov    BYTE PTR [rax+rbx*1],0x66
1155:	48 ff c3             	inc    rbx
1158:	48 8d 3d b1 9e 00 00 	lea    rdi,[rip+0x9eb1]        # b010 <scanf_format>
115f:	48 89 e6             	mov    rsi,rsp
1162:	31 c0                	xor    eax,eax
1164:	ff 15 66 9e 00 00    	call   QWORD PTR [rip+0x9e66]        # afd0 <scanf@GLIBC_2.2.5>
116a:	48 8b 04 24          	mov    rax,QWORD PTR [rsp]
116e:	48 3d 85 00 00 00    	cmp    rax,0x85
1174:	0f 84 2d 22 00 00    	je     33a7 <node133>
117a:	48 83 f8 3c          	cmp    rax,0x3c
117e:	0f 84 08 10 00 00    	je     218c <node60>
1184:	48 3d dc 00 00 00    	cmp    rax,0xdc
118a:	0f 84 a2 3c 00 00    	je     4e32 <node220>
1190:	e9 b8 7c 00 00       	jmp    8e4d <fail_code>
```
convert.py would convert them into a cleaner assembly file, something like:
```as
000000000000114a <node0>:
    lea    rax,[rip+0x9f7f]        # b0d0 <__TMC_END__>
    mov    BYTE PTR [rax+rbx*1],0x66
    inc    rbx
    lea    rdi,[rip+0x9eb1]        # b010 <scanf_format>
    mov    rsi,rsp
    xor    eax,eax
    call   QWORD PTR [rip+0x9e66]        # afd0 <scanf@GLIBC_2.2.5>
    mov    rax,QWORD PTR [rsp]
    cmp    rax,0x85
    je     33a7 <node133>
    cmp    rax,0x3c
    je     218c <node60>
    cmp    rax,0xdc
    je     4e32 <node220>
    jmp    8e4d <fail_code>
```
And the our python solve script's `parse_assembly` would parse the assembly code.  
First, it exacts the name of the node:
```py
node_match = re.match(r'[0-9a-f]+ <(node\d+)>:', line)
if node_match:
    node_name = node_match.group(1)
    current_node = Node(node_name)
    nodes[node_name] = current_node
    continue
```
> ##### `r'[0-9a-f]+ <(node\d+)>:'`

This matches something like `000000000000114a <node0>:`  
Specifically,   
- `[0-9a-f]+` look for one or more **hexadecimal number**. Using the above assembly code as example : `000000000000114a`
- `<(node\d+)>:` look for node name enclosed with `<>` and ending with a `:`. `d+` means **one or more** digits