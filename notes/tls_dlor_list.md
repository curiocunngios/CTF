---
aliases:
  - tls_dtor_list exploitation
  - thread local storage
tags:
  - flashcard/active/ctf/A
---

# TLS Destructor List Exploitation

## Basic Concepts

### TLS Destructor List
- Located at {{fs:[-0x58]}}. In `pwndbg`, its address and subsequent ones be viewed via {{`fsbase`, `tele fsbase`}}
- Is a {{linked list of destructors containing function pointers}}
- Gets accessed during {{program exit}}

## Execution Flow
Program exit follows this path:  
`exit()` → {{`__run_exit_handlers()`}} → {{`__call_tls_dtors()`}}


### Inside __call_tls_dtors()
Key operations:
1. {{Retrieves current destructor from tls_dtor_list}}
2. {{Demangles function pointer}}
3. {{Calls func(obj)}}
4. {{Moves to next destructor}}

## Pointer Protection

### PTR_DEMANGLE
Assembly implementation:
```nasm
ror rdx, 0x11
xor rdx, QWORD PTR fs:[0x30]
```
Mathematical expression:  
`PTR_DEMANGLE(ptr)` = {{`ptr` >> 0x11 ⊕ `fs:[0x30]`}}


### Critical Memory Locations
- Stack Canary: {{`fs:[0x28]`}}
- Pointer Guard: {{`fs:[0x30]`}}
- TLS Dtor List: {{`fs:[-0x58]`}}

## Exploitation Strategy

### Requirements for RCE
To achieve `system("/bin/sh")`:
1. Need to make {{PTR_DEMANGLE(`tls_dtor_list->func`) == &system}}
2. Therefore: {{`tls_dtor_list->func` = (&system ⊕ `fs:[0x30]`) << `0x11`}}
3. Need to set {{`tls_dtor_list->obj` = &`"/bin/sh"`}}

### Attack Chain
1. {{Overwrite fs:[-0x58] with controllable address}}. Like getting `tls_dtor_list->func`
2. Either {{leak or overwrite `fs:[0x30]` to 0}}
3. {{Set func = &system ⊕ fs:[0x30] << 0x11}}
4. {{Set obj = &"/bin/sh"}}
