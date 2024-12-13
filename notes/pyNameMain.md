---
aliases:
  - main equal name
  - __name__ == "__main__"
tags:
  - flashcard/active/ctf
---
```py
if __name__ == "__main__":
```
- it is a python idiom used to {{check whether the script is being run inside another script}}
- if the script is run directly (alone), then {{name would be set to "__main__"}}
- if the script is run inside a script, {{then __name__ would be set to the name of the module.}} <!--SR:!2024-12-18,4,270!2024-12-18,4,270!2024-12-18,4,270-->

