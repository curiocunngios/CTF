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
- Gets accessed during {{program exit}} <!--SR:!2025-01-06,1,230!2025-01-06,1,230!2025-01-06,1,230!2025-01-06,1,230-->

## Execution Flow
Program exit follows this path:
`exit()` → {{`__run_exit_handlers()`}} → {{`__call_tls_dtors()`}} <!--SR:!2025-01-06,1,230!2025-01-06,1,230-->


### Inside __call_tls_dtors()
```
tls_dtor_list → [Destructor1] → [Destructor2] → [Destructor3] → null
                ↓
                contains:
                - func (function pointer)
                - obj (argument)
```
Key operations:
1. {{Retrieves current destructor from tls_dtor_list}}
2. {{Demangles function pointer extracted from the destructor node}}
3. {{Calls func(obj)}}
4. {{Moves to next destructor}
When __call_tls_dtors() runs: <!--SR:!2025-01-06,1,230!2025-01-06,1,230!2025-01-06,1,230-->

## Pointer Protection

### PTR_DEMANGLE
Assembly implementation:
```nasm
ror rdx, 0x11
xor rdx, QWORD PTR fs:[0x30]
```
Mathematical expression:
`PTR_DEMANGLE(ptr)` = {{`ptr` >> 0x11 ⊕ `fs:[0x30]`}} <!--SR:!2025-01-06,1,230-->


### Critical Memory Locations
- Stack Canary: {{`fs:[0x28]`}}
- Pointer Guard: {{`fs:[0x30]`}}
- TLS Dtor List: {{`fs:[-0x58]`}} <!--SR:!2025-01-06,1,230!2025-01-06,1,230!2025-01-06,1,230-->

## Exploitation Strategy

### Requirements for RCE
To achieve `system("/bin/sh")`:
1. Need to make {{PTR_DEMANGLE(`tls_dtor_list->func`) = &system}}
2. Therefore: {{`tls_dtor_list->func` = (&system ⊕ `fs:[0x30]`) << `0x11`}})
3. Need to set {{`tls_dtor_list->obj` = &`"/bin/sh"`}} <!--SR:!2025-01-06,1,230!2025-01-06,1,230!2025-01-06,1,230-->

### Attack Chain
1. {{Overwrite fs:[-0x58] with controllable address}} and forge the structure. Like getting `tls_dtor_list->func`
2. Either {{leak or overwrite `fs:[0x30]` to 0}}
3. Set func = {{&system ⊕ fs:[0x30] << 0x11}}
4. Set obj = {{&"/bin/sh"}} <!--SR:!2025-01-06,1,230!2025-01-06,1,230!2025-01-06,1,230!2025-01-06,1,230-->
