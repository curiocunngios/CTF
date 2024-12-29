---
aliases:
  - typical address
  - memory address range
  - address range
  - tbc 
tags:
  - flashcard/active/ctf/A
---
# `+`
- **one or more** of previous element <!--SR:!2024-12-30,1,224-->

# `\d`
- **digits** <!--SR:!2024-12-30,1,224-->

# `\d+`
- **one or more digits** <!--SR:!2024-12-30,1,224-->

# `[...]`
- creates a character class that **matches any single characters in the brackets`[]`** <!--SR:!2024-12-30,1,230-->

# ` <`
- just a {{literal space and literal `<`}} <!--SR:!2024-12-30,1,230-->

# `(...)`
- creates a capture group that {{can be extracted later}} <!--SR:!2024-12-30,1,230-->

# `>:`
- just a {{literal `>` and a literal `:`}} <!--SR:!2024-12-30,1,224--> 

# `\s`
- matches {{whitespace}}

# `*`
- **zero or more** <!--SR:!2024-12-30,1,218-->

# `.`
- **any character except newline**

# `?`
- mark the previous element {{non-greedy, stop as soon as next element matches even if previous also matches}}


# python regex  

## `r'...'`
- a **raw string**
- prevents python from reading `\` as **escape character** so that something like `\[` can get passed to {{regex engine which is independent from python}}. <!--SR:!2024-12-30,1,218!2024-12-30,1,218!2024-12-30,1,218-->

## `re.match`
- attempts to match pattern at the **beginning** of string <!--SR:!2024-12-30,1,218--> 

## `re.search`
- look for matches **anywhere** in the string <!--SR:!2024-12-30,1,218-->

# Examples
> ## `node_match = re.match(r'[0-9a-f]+ <(node\d+)>:', line)`
This matches something like `000000000000114a <node0>:`
- `[0-9a-f]+` look for one or more **hexadecimal number**. Using the above assembly code as example : `000000000000114a`
- `<(node\d+)>:` look for node name enclosed with `<>` and ending with a `:`. <!--SR:!2024-12-30,1,224-->

