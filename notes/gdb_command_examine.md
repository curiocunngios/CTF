---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - gdb
  - gdb commands
  - x/ command
  - examine command
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

# How x command work  
??  
```
x/s $rip+0xe3
^  ^ ^    ^
|  | |    └── offset (0xe3)
|  | └──────── rip register ($ means "register")
|  └────────── format specifier (s = string)
└─────────────── examine command
```

Common x formats:
x/s ::: examine as string
x/x ::: examine as hex
x/i ::: examine as instruction <!--SR:!2024-12-02,1,230!2000-01-01,1,250-->


(gdb) x/s $rip+0xe3    ::: View string
(gdb) x/x $rip+0xe3    ::: View hex value <!--SR:!2024-12-02,1,230!2000-01-01,1,250-->
(gdb) x/10i $rip       ::: View next 10 instructions