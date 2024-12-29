# Cherry Bomb
Author: ivanwong13768  
Reverse  
Description  
Solves 3  

Setsuna wants to make a cherry pie. Help her out!  

Uhhhh... who is Setsuna? Who let her cook?  

`nc chal.firebird.sh 35055`  

You and Rina's (kinda) epic plan (who is Rina???) (who are You??????????)  
Skeleton code  
Full solve script  

Hint: https://hackmd.io/@ivanwong13768/comp2633_hw10a_hints  

## Solution

```py
from pwn import *
import re
import z3

def get_one_sample():
    p = remote('chal.firebird.sh', 35055)
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
    chars = [z3.Int(f'c{i}') for i in range(228)]
    
    # char must be valid ASCII
    for c in chars:
        solver.add(c >= 0)
        solver.add(c <= 255)
    
    # Add constraints from each sample
    for stamina, recipe in samples.items():
        start = stamina - 100
        for i in range(len(recipe)):
            solver.add(recipe[i] == chars[start+i] + chars[start+i+1] + stamina)
    
    if solver.check() == z3.sat:
        model = solver.model()
        return [model[c].as_long() for c in chars]
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

for i in range(30):

    stamina, steps = get_one_sample()
    samples[stamina] = steps

encoded = find_message(samples)


message = decode_message(encoded)
print(message)
```
The above solution get you the message you need to get the flag from connecting to the remote.  

















































































```
┌──(kali㉿kali)-[~/Desktop/CTF/Cherry]
└─$ nc chal.firebird.sh 35055                                     
Setsuna wants to bake a cherry pie! She is 100% energetic today.

Rina-chan has calculated the perfect cherry pie recipe for you.
Perfect recipe:
1: Add 161 grams of flour
2: Add 100 cherries
3: Add 100 cherries
4: Add 170 grams of butter
5: Add 170 grams of butter
6: Add 100 cherries
7: Add 114 grams of butter
8: Add 229 grams of flour
9: Add 269 grams of flour
10: Knead the dough 171 times
11: Add 124 cherries
12: Add 113 grams of flour
13: Add 133 grams of flour
14: Add 142 grams of butter
15: Knead the dough 191 times
16: Add 270 grams of butter
17: Add 212 cherries
18: Add 133 grams of flour
19: Add 181 grams of flour
20: Add 178 grams of butter
21: Add 217 grams of flour
22: Add 310 grams of butter
23: Add 270 grams of butter
24: Add 182 grams of butter
25: Add 117 grams of flour
26: Add 102 grams of butter
27: Add 125 grams of flour
28: Add 129 grams of flour
29: Add 116 cherries
30: Add 118 grams of butter
31: Add 129 grams of flour
32: Add 138 grams of butter
33: Add 186 grams of butter
34: Add 258 grams of butter
35: Knead the dough 211 times
36: Add 148 cherries
37: Add 133 grams of flour
38: Add 189 grams of flour
39: Add 258 grams of butter
40: Knead the dough 179 times
41: Add 128 cherries
42: Add 144 cherries
43: Add 188 cherries
44: Knead the dough 239 times
45: Knead the dough 179 times
46: Add 138 grams of butter
47: Knead the dough 211 times
48: Add 249 grams of flour
49: Knead the dough 179 times
50: Add 112 cherries
51: Add 104 cherries
52: Add 106 grams of butter
53: Add 109 grams of flour
54: Add 116 cherries
55: Add 184 cherries
56: Knead the dough 187 times
57: Add 178 grams of butter
58: Add 189 grams of flour
59: Add 124 cherries
60: Add 185 grams of flour
61: Add 273 grams of flour
62: Knead the dough 211 times
63: Add 148 cherries
64: Add 133 grams of flour
65: Add 189 grams of flour
66: Add 249 grams of flour
67: Knead the dough 179 times
68: Add 112 cherries
69: Add 104 cherries
70: Add 106 grams of butter
71: Add 109 grams of flour
72: Add 116 cherries
73: Add 180 cherries
74: Add 244 cherries
75: Knead the dough 199 times
76: Add 209 grams of flour
77: Add 252 cherries
78: Add 192 cherries
79: Knead the dough 123 times
80: Add 100 cherries
81: Add 192 cherries
82: Add 192 cherries
83: Add 100 cherries
84: Add 114 grams of butter
85: Add 116 cherries
86: Add 169 grams of flour
87: Add 232 cherries
88: Knead the dough 231 times
89: Add 177 grams of flour
90: Add 140 cherries
91: Add 213 grams of flour
92: Add 268 cherries
93: Knead the dough 211 times
94: Knead the dough 127 times
95: Knead the dough 179 times
96: Add 258 grams of butter
97: Add 208 cherries
98: Add 156 cherries
99: Add 141 grams of flour
100: Add 128 cherries
101: Add 121 grams of flour
102: Add 122 grams of butter
103: Add 128 cherries
104: Knead the dough 191 times
105: Add 190 grams of butter
106: Add 126 grams of butter
107: Knead the dough 235 times
108: Knead the dough 275 times
109: Add 180 cherries
110: Knead the dough 211 times
111: Add 260 cherries
112: Add 180 cherries
113: Add 106 grams of butter
114: Add 125 grams of flour
115: Knead the dough 211 times
116: Add 274 grams of butter
117: Add 218 grams of butter
118: Add 140 cherries
119: Add 130 grams of butter
120: Add 205 grams of flour
121: Add 289 grams of flour
122: Add 310 grams of butter
123: Add 282 grams of butter
124: Add 185 grams of flour
125: Add 112 cherries
126: Knead the dough 119 times
127: Add 196 cherries
128: Add 212 cherries

(You: What even is this cursed recipe... Do I really have to follow this?)
(Rina: Pwease? *https://64.media.tumblr.com/61e089232161e2a093a510178edc2524/tumblr_inline_os8ojnK5CL1tiprmj_400.png*)
(You: Ok🥺)

Before baking the pie, you should probably give Setsuna some words of encouragement!
Uhhhh... Setsuna-san, I appreciate your love for cooking, but your cooking is errr... "a bit too original". You know what I mean? Like- your food tastes really, REALLY 'out of the world'. Let me help you make this cherry pie ok?

Let's start baking!
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Rub some butter into the pastry...
Setsuna: Rub some butter into the pastry...
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: Rub some butter into the pastry...
Setsuna: I'm gonna knead the dough!
Setsuna: Rub some butter into the pastry...
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: Rub some butter into the pastry...
Setsuna: Rub some butter into the pastry...
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: Rub some butter into the pastry...
Setsuna: Rub some butter into the pastry...
Setsuna: Rub some butter into the pastry...
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: Rub some butter into the pastry...
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I'm gonna knead the dough!
Setsuna: I'm gonna knead the dough!
Setsuna: Rub some butter into the pastry...
Setsuna: I'm gonna knead the dough!
Setsuna: Time to add some flour!
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I'm gonna knead the dough!
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I'm gonna knead the dough!
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Rub some butter into the pastry...
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I'm gonna knead the dough!
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I'm gonna knead the dough!
Setsuna: I'm gonna knead the dough!
Setsuna: I'm gonna knead the dough!
Setsuna: Rub some butter into the pastry...
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Time to add some flour!
Setsuna: Rub some butter into the pastry...
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I'm gonna knead the dough!
Setsuna: Rub some butter into the pastry...
Setsuna: Rub some butter into the pastry...
Setsuna: I'm gonna knead the dough!
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: I'm gonna knead the dough!
Setsuna: Rub some butter into the pastry...
Setsuna: Rub some butter into the pastry...
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: Rub some butter into the pastry...
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I love cherries! Let's add a cherry!

Wow, the pie looks gorgeous after baking!
You successfully made a perfect cherry pie!
After this precious experience, you learnt this valuable lesson:
flag{wh47_h4pp3n5_wh3n_y0u_l37_h3r_c00k:https://www.youtube.com/watch?v=A2Igz66sZSA}
```