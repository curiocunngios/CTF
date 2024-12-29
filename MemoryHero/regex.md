# `r'[0-9a-f]+ <(node\d+)>:'` 
This matches something like `000000000000114a <node0>:`  
Specifically,   
- `[0-9a-f]+` look for one or more **hexadecimal number**. Using the above assembly code as example : `000000000000114a`
- `<(node\d+)>:` look for node name enclosed with `<>` and ending with a `:`. `d+` means **one or more** digits

# `+`   
**one or more**
# `\d` 
**digits** 
# `\d+` 
**one or more digits**
# `[...]`   
creates a character class that **matches any characters in the brackets`[]`**