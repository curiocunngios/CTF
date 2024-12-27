```py
def activate_neurons(speech: str) -> list[int]:
    neuron_data = [ord(i) for i in speech]
    # data preprocessing in your brain!!
    for i in range(len(neuron_data) - 1):
        neuron_data[i] = neuron_data[i] ^ neuron_data[i + 1]
    return neuron_data
```

- takes character in `speech` aka `word_of_encouragement` or perhaps `flag` 
- convert each of them to their ASCII numeric value
- do between one character e.g `x[i]` and its next one, stores it in `x[i]` ]

```py
perfect_recipe = bake_pie(word_of_encouragement, stamina)
```
stamina here is random but can be known
```py
print(f"Setsuna wants to bake a cherry pie! She is {stamina}% energetic today.")
```


```py
def bake_pie(speech: str, stamina: int) -> list[int]:
    neuron_data = activate_neurons(speech)
    steps = []
    # how to design a pie:
    # Think: Makes sense? Have fun? Design is professional?
    for i, j in zip(neuron_data[stamina - 100:], neuron_data[stamina - 99: stamina - 99 + 128]):
        steps.append(i + j + stamina)
    return steps
```

```py
    for i, j in zip(neuron_data[stamina - 100:], neuron_data[stamina - 99: stamina - 99 + 128]):
        steps.append(i + j + stamina)
    return steps
```

just somehow encrypting it



```py
print("Let's start baking!")
for i, step in zip(range(len(your_recipe)), your_recipe):
    if step % 4 == 0:
        print(f"Setsuna: I love cherries! Let's add a cherry!")
        if step != perfect_recipe[i]:
            print("Your pie has the wrong number of cherries, it doesn't taste good at all...")
            exit(1)
    elif step % 4 == 1:
        print(f"Setsuna: Time to add some flour!")
        if step != perfect_recipe[i]:
            print("Your pie has the wrong amount of flour. The pastry doesn't even look like a pastry!")
            exit(2)
    elif step % 4 == 2:
        print(f"Setsuna: Rub some butter into the pastry...")
        if step != perfect_recipe[i]:
            print("Your pie has the wrong amount of butter. The whole pie doesn't really stick together...")
            exit(3)
    elif step % 4 == 3:
        print(f"Setsuna: I'm gonna knead the dough!")
        if step != perfect_recipe[i]:
            print("You aren't kneading the dough correctly! The pastry isn't flaky at all.")
            exit(4)
```
`step` can't be a numeric value? Nvm we also have this `step != perfect_recipe[i]:` that prevents us from exiting.

so we just need to input something that, after processing with stamina, would become the same thing in `perfect_recipe`

so just inputting the same thing? lol



```
print("Rina-chan has calculated the perfect cherry pie recipe for you.")
print("Perfect recipe:")
for i, step in zip(range(len(perfect_recipe)), perfect_recipe):
    if step % 4 == 0:
        print(f"{i+1}: Add {step} cherries")
    elif step % 4 == 1:
        print(f"{i+1}: Add {step} grams of flour")
    elif step % 4 == 2:
        print(f"{i+1}: Add {step} grams of butter")
    elif step % 4 == 3:
        print(f"{i+1}: Knead the dough {step} times")
```

# to do: 

- obtain stamina value `116%` 
- obtian the `step` output: e.g.
```
[120, 124, 191]
Rina-chan has calculated the perfect cherry pie recipe for you.
Perfect recipe:
1: Add 120 cherries
2: Add 124 cherries
3: Knead the dough 191 times
```
- reverse




```
┌──(kali㉿kali)-[~/Desktop/CTF/Cherry]
└─$ python solve.py
Collected stamina 198, total samples: 1
Collected stamina 120, total samples: 2
Collected stamina 130, total samples: 3
Collected stamina 165, total samples: 4
Collected stamina 129, total samples: 5
Collected stamina 110, total samples: 6
Collected stamina 114, total samples: 7
Collected stamina 141, total samples: 8
Collected stamina 137, total samples: 9
Collected stamina 153, total samples: 10
Collected stamina 154, total samples: 11
Collected stamina 189, total samples: 12
Collected stamina 160, total samples: 13
Collected stamina 121, total samples: 14
Collected stamina 177, total samples: 15
Collected stamina 147, total samples: 16
Collected stamina 175, total samples: 17
Collected stamina 139, total samples: 18
Collected stamina 118, total samples: 19
Collected stamina 172, total samples: 20
Collected stamina 181, total samples: 21
Collected stamina 119, total samples: 22
Collected stamina 178, total samples: 23
Collected stamina 146, total samples: 24
Collected stamina 199, total samples: 25
Collected stamina 179, total samples: 26
Collected stamina 157, total samples: 27
Collected stamina 155, total samples: 28
Collected stamina 161, total samples: 29
Collected stamina 173, total samples: 30
Collected stamina 176, total samples: 31
Collected stamina 193, total samples: 32
Collected stamina 111, total samples: 33
Collected stamina 116, total samples: 34
Collected stamina 124, total samples: 35
Collected stamina 100, total samples: 36
Collected stamina 134, total samples: 37
Collected stamina 162, total samples: 38
Collected stamina 144, total samples: 39
Collected stamina 196, total samples: 40
Collected stamina 190, total samples: 41
Collected stamina 127, total samples: 42
Collected stamina 115, total samples: 43
Collected stamina 135, total samples: 44
Collected stamina 168, total samples: 45
Collected stamina 136, total samples: 46
Collected stamina 166, total samples: 47
Collected stamina 103, total samples: 48
Collected stamina 163, total samples: 49
Collected stamina 138, total samples: 50
Found message: Uhhhh... Setsuna-san, I appreciate your love for cooking, but your cooking is errr... "a bit too original". You know what I mean? Like- your food tastes really, REALLY 'out of the world'. Let me help you make this cherry pie ok?
^Zzsh: suspended (signal)  python solve.py
                                                                                                                      
┌──(kali㉿kali)-[~/Desktop/CTF/Cherry]
└─$ nc chal.firebird.sh 35055
Setsuna wants to bake a cherry pie! She is 132% energetic today.

Rina-chan has calculated the perfect cherry pie recipe for you.
Perfect recipe:
1: Add 218 grams of butter
2: Add 290 grams of butter
3: Knead the dough 243 times
4: Add 180 cherries
5: Add 165 grams of flour
6: Add 221 grams of flour
7: Add 290 grams of butter
8: Knead the dough 211 times
9: Add 160 cherries
10: Add 176 cherries
11: Add 220 cherries
12: Knead the dough 271 times
13: Knead the dough 211 times
14: Add 170 grams of butter
15: Knead the dough 243 times
16: Add 281 grams of flour
17: Knead the dough 211 times
18: Add 144 cherries
19: Add 136 cherries
20: Add 138 grams of butter
21: Add 141 grams of flour
22: Add 148 cherries
23: Add 216 cherries
24: Knead the dough 219 times
25: Add 210 grams of butter
26: Add 221 grams of flour
27: Add 156 cherries
28: Add 217 grams of flour
29: Add 305 grams of flour
30: Knead the dough 243 times
31: Add 180 cherries
32: Add 165 grams of flour
33: Add 221 grams of flour
34: Add 281 grams of flour
35: Knead the dough 211 times
36: Add 144 cherries
37: Add 136 cherries
38: Add 138 grams of butter
39: Add 141 grams of flour
40: Add 148 cherries
41: Add 212 cherries
42: Add 276 cherries
43: Knead the dough 231 times
44: Add 241 grams of flour
45: Add 284 cherries
46: Add 224 cherries
47: Knead the dough 155 times
48: Add 132 cherries
49: Add 224 cherries
50: Add 224 cherries
51: Add 132 cherries
52: Add 146 grams of butter
53: Add 148 cherries
54: Add 201 grams of flour
55: Add 264 cherries
56: Knead the dough 263 times
57: Add 209 grams of flour
58: Add 172 cherries
59: Add 245 grams of flour
60: Add 300 cherries
61: Knead the dough 243 times
62: Knead the dough 159 times
63: Knead the dough 211 times
64: Add 290 grams of butter
65: Add 240 cherries
66: Add 188 cherries
67: Add 173 grams of flour
68: Add 160 cherries
69: Add 153 grams of flour
70: Add 154 grams of butter
71: Add 160 cherries
72: Knead the dough 223 times
73: Add 222 grams of butter
74: Add 158 grams of butter
75: Knead the dough 267 times
76: Knead the dough 307 times
77: Add 212 cherries
78: Knead the dough 243 times
79: Add 292 cherries
80: Add 212 cherries
81: Add 138 grams of butter
82: Add 157 grams of flour
83: Knead the dough 243 times
84: Add 306 grams of butter
85: Add 250 grams of butter
86: Add 172 cherries
87: Add 162 grams of butter
88: Add 237 grams of flour
89: Add 321 grams of flour
90: Add 342 grams of butter
91: Add 314 grams of butter
92: Add 217 grams of flour
93: Add 144 cherries
94: Knead the dough 151 times
95: Add 228 cherries
96: Add 244 cherries
97: Knead the dough 271 times
98: Add 277 grams of flour
99: Knead the dough 171 times
100: Add 148 cherries
101: Add 218 grams of butter
102: Add 217 grams of flour
103: Add 234 grams of butter
104: Knead the dough 243 times
105: Add 180 cherries
106: Add 165 grams of flour
107: Add 221 grams of flour
108: Add 284 cherries
109: Knead the dough 211 times
110: Add 141 grams of flour
111: Knead the dough 143 times
112: Knead the dough 211 times
113: Add 284 cherries
114: Add 237 grams of flour
115: Knead the dough 171 times
116: Add 157 grams of flour
117: Add 156 cherries
118: Knead the dough 171 times
119: Add 237 grams of flour
120: Add 297 grams of flour
121: Add 237 grams of flour
122: Knead the dough 159 times
123: Add 149 grams of flour
124: Add 145 grams of flour
125: Add 153 grams of flour
126: Add 238 grams of butter
127: Add 229 grams of flour
128: Add 258 grams of butter

(You: What even is this cursed recipe... Do I really have to follow this?)
(Rina: Pwease? *https://64.media.tumblr.com/61e089232161e2a093a510178edc2524/tumblr_inline_os8ojnK5CL1tiprmj_400.png*)
(You: Ok🥺)

Before baking the pie, you should probably give Setsuna some words of encouragement!
Uhhhh... Setsuna-san, I appreciate your love for cooking, but your cooking is errr... "a bit too original". You know what I mean? Like- your food tastes really, REALLY 'out of the world'. Let me help you make this cherry pie ok?

Let's start baking!
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
Setsuna: I'm gonna knead the dough!
Setsuna: Time to add some flour!
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: Rub some butter into the pastry...
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I'm gonna knead the dough!
Setsuna: Time to add some flour!
Setsuna: I'm gonna knead the dough!
Setsuna: I'm gonna knead the dough!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: Time to add some flour!
Setsuna: I'm gonna knead the dough!
Setsuna: Time to add some flour!
Setsuna: I love cherries! Let's add a cherry!
Setsuna: I'm gonna knead the dough!
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: I'm gonna knead the dough!
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: Time to add some flour!
Setsuna: Rub some butter into the pastry...
Setsuna: Time to add some flour!
Setsuna: Rub some butter into the pastry...

Wow, the pie looks gorgeous after baking!
You successfully made a perfect cherry pie!
After this precious experience, you learnt this valuable lesson:
flag{wh47_h4pp3n5_wh3n_y0u_l37_h3r_c00k:https://www.youtube.com/watch?v=A2Igz66sZSA}
```