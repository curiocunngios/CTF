1. i have realizewd that in most the time, I waste my time and mental energy being frustrated on not knowing how to write sript i.e. python, so the follow would be my priority when it comes to making notes, flashcards, memorize and practicing for the competition:

- python: useufl functions, parsing, etc.(capture examples from concrete use cases in your AI-gen scripts)
- assembly 
- pwndbg commands 
- memory concepts 

I dont undertsand how 

pop_rdi_ret,
elf.got['puts'],
elf.plt['gets'] 
--> input system address 

work

more like I dont know how does `gets` work, why first inputting `puts` then input `system` using `gets` would overwrite puts 




1.    pop_rdi_ret gadget pops elf.got['puts'] into RDI register
2.    When gets is called, RDI contains the address of puts in GOT
3.    gets will read input and write it to wherever RDI points to
