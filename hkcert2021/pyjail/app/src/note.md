```py
backup_eval = eval
backup_print = print
input = input()
if '[' in input or ']' in input:
	print('[You failed to break the jail]')
	exit(-1)
globals()['__builtins__'].__dict__.clear()
backup_print(backup_eval(input,{},{}))
```

This seems be to a python jail question ( I don't know what it is)

Since I am like 0 sik, so i am going to skip this pwn first lol! Let me come back perhaps if I encountered this in the interal CTF lol
