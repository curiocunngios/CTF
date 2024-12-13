---
aliases:
- Position-independent code
tags: 
- flashcard/active/ctf
---

# Position-independent code
Position-independent code is code that {{can run regardless of its absolute memory location}} <!--SR:!2024-12-17,3,245-->

## Usage of PIC
PIC is needed for:
- Security {{(ASLR)}}
- {{Shared libraries}}
- The code needs to know its current position to {{access data/functions (PIC) relative to itself}} <!--SR:!2024-12-17,3,242!2024-12-17,3,243!2024-12-17,3,248-->

### **Position Independent Code (PIC) Example:**
```c
// Non-PIC: Uses absolute addresses
int global_var = 42;
void func1() {
    printf("%d", global_var);  
}

// PIC: Uses relative addressing
int global_var = 42;
void func2() {
    printf("%d", global_var);
}
```
- func1() {{assumes global_var is always at specific address.}}
- func2() {{calculates global_var location relative to current position}} and uses {{GOT to find actual address}}. Specifically, it calculates the PIC address with {{GOT base address and proper offset to that particular PIC}}
### Example in assembly
```as
; Non-PIC
mov eax, [0x804c054]        ; Direct absolute address

; PIC
call get_pc_thunk           ; Get current position (specifically next next instruction address and put it in ebx)
add ebx, offset_to_GOT      ; Point to GOT
mov eax, [ebx + offset]     ; Access relative to GOT
```
<!--SR:!2024-12-17,3,240!2024-12-17,3,250!2024-12-17,3,240!2024-12-17,3,240!2024-12-17,3,240-->