---
aliases:
  - GOT Overwrite using gets
tags:
  - flashcard/active/ctf/A
---
# GOT Overwrite using gets()
The gets() function can be used to overwrite GOT entries by manipulating where it writes input to. This technique often involves overwriting {{existing function entries}} (like puts) with system(). 

## How it Works
```py
pop_rdi_ret,
elf.got['puts'],
elf.plt['gets']
```
1. The pop_rdi_ret gadget is used to {{pop the address of puts@GOT into RDI register}}
2. When gets() is called, it will {{write input to wherever RDI is pointing to}} (in this case, puts@GOT)
3. By inputting the {{system() address}}, we effectively {{replace puts with system in the GOT}} 

## Key Components
- pop_rdi_ret: {{Assembly gadget that controls what gets loaded into RDI}}
- elf.got['puts']: {{Address where puts function is stored in GOT}}
- elf.plt['gets']: {{PLT entry for gets function that will do the writing}}

## Why This Works
The technique works because gets() writes to {{wherever RDI points to}}, and we can {{control RDI using pop_rdi_ret}}. This allows us to {{overwrite any GOT entry}} we want. 